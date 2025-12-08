"""
Основное приложение Streamlit для генерации PDF из данных.

Предоставляет web-интерфейс с вкладками для выбора файлов, шаблонов, генерации и истории.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

from data_parser import list_data_files, parse_csv, parse_json, get_invoice_ids, get_invoice_data, validate_data_structure
from pdf_generator import list_templates, load_template, render_html, generate_pdf, generate_batch_pdf, create_zip_archive, open_pdf
from database import init_database, add_generation_record, get_history, get_statistics, delete_record, clear_history

# Инициализация
init_database()
os.makedirs('data', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Боковая панель настроек
st.sidebar.title("⚙️ Настройки")
page_format = st.sidebar.selectbox("Формат страницы", ["A4", "Letter"], index=0)
orientation = st.sidebar.selectbox("Ориентация", ["Portrait", "Landscape"], index=0)

# Основные вкладки
tab_files, tab_templates, tab_generation, tab_history = st.tabs(["📄 Выбор файлов", "📊 Выбор шаблона", "🔧 Генерация PDF", "📜 История генераций"])

# Вкладка выбора файлов
with tab_files:
    st.header("📄 Выбор файла данных")

    # Список существующих файлов
    files = list_data_files()
    if files:
        selected_file = st.selectbox("Выберите файл данных", files, key="data_file_select")
        if selected_file:
            filepath = os.path.join('data', selected_file)
            try:
                if selected_file.endswith('.csv'):
                    data = parse_csv(filepath)
                else:
                    data = parse_json(filepath)

                valid, msg = validate_data_structure(data)
                if not valid:
                    st.error(f"❌ Ошибка в данных: {msg}")
                else:
                    st.success("✅ Файл загружен успешно")
                    # Предпросмотр
                    if isinstance(data, pd.DataFrame):
                        st.subheader("Предпросмотр данных (первые 10 строк)")
                        st.dataframe(data.head(10))
                    else:
                        st.subheader("Предпросмотр данных (первые 5 записей)")
                        st.json(data[:5])

                    # Сохраняем в session state
                    st.session_state['data'] = data
                    st.session_state['data_file'] = selected_file
            except Exception as e:
                st.error(f"❌ Ошибка загрузки файла: {e}")

    # Загрузка нового файла
    st.subheader("Загрузить новый файл")
    uploaded_file = st.file_uploader("Выберите CSV или JSON файл", type=['csv', 'json'], key="file_uploader")
    if uploaded_file:
        if uploaded_file.size > 50 * 1024 * 1024:  # 50MB
            st.error("❌ Файл слишком большой (макс. 50MB)")
        else:
            filepath = os.path.join('data', uploaded_file.name)
            with open(filepath, 'wb') as f:
                f.write(uploaded_file.getvalue())
            st.success("✅ Файл загружен успешно")
            st.rerun()

# Вкладка выбора шаблона
with tab_templates:
    st.header("📊 Выбор шаблона")

    # Список шаблонов
    templates = list_templates()
    if templates:
        selected_template = st.selectbox("Выберите шаблон", templates, key="template_select")
        if selected_template:
            template_path = os.path.join('templates', selected_template)
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                st.subheader("Предпросмотр шаблона")
                st.code(content[:500] + "..." if len(content) > 500 else content, language='html')
                st.session_state['template_name'] = selected_template
            except Exception as e:
                st.error(f"❌ Ошибка загрузки шаблона: {e}")

    # Редактирование шаблона
    if 'template_name' in st.session_state:
        st.subheader("Редактирование шаблона")
        if st.button("✏️ Редактировать шаблон", key="edit_template_btn"):
            st.session_state['edit_mode'] = True

        if st.session_state.get('edit_mode', False):
            template_path = os.path.join('templates', st.session_state['template_name'])
            with open(template_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            edited_content = st.text_area("HTML код шаблона", current_content, height=400, key="template_editor")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Сохранить изменения", key="save_template_btn"):
                    try:
                        with open(template_path, 'w', encoding='utf-8') as f:
                            f.write(edited_content)
                        st.success("✅ Шаблон сохранен")
                        st.session_state['edit_mode'] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Ошибка сохранения: {e}")
            with col2:
                if st.button("❌ Отмена", key="cancel_edit_btn"):
                    st.session_state['edit_mode'] = False
                    st.rerun()

    # Загрузка нового шаблона
    st.subheader("Загрузить новый шаблон")
    uploaded_template = st.file_uploader("Выберите HTML файл", type=['html'], key="template_uploader")
    if uploaded_template:
        if uploaded_template.size > 50 * 1024 * 1024:
            st.error("❌ Файл слишком большой (макс. 50MB)")
        else:
            filepath = os.path.join('templates', uploaded_template.name)
            with open(filepath, 'wb') as f:
                f.write(uploaded_template.getvalue())
            st.success("✅ Шаблон загружен успешно")
            st.rerun()

# Вкладка генерации PDF
with tab_generation:
    st.header("🔧 Генерация PDF")

    if 'data' not in st.session_state or 'template_name' not in st.session_state:
        st.warning("⚠️ Пожалуйста, выберите файл данных и шаблон на соответствующих вкладках")
    else:
        data = st.session_state['data']
        template_name = st.session_state['template_name']
        data_file = st.session_state['data_file']

        try:
            template = load_template(template_name)
            invoice_ids = get_invoice_ids(data)

            if not invoice_ids:
                st.error("❌ В данных не найдены ID счетов")
            else:
                # Одиночная генерация
                st.subheader("Одиночная генерация")
                search_term = st.text_input("Поиск по ID счета", key="single_search")
                filtered_ids = [id for id in invoice_ids if search_term.lower() in id.lower()] if search_term else invoice_ids
                selected_id = st.selectbox("Выберите ID счета", filtered_ids, key="single_select")

                if st.button("🚀 Сгенерировать PDF", key="generate_single_btn"):
                    with st.spinner("Генерация PDF..."):
                        invoice_data = get_invoice_data(data, selected_id)
                        if not invoice_data:
                            st.error("❌ Данные счета не найдены")
                        else:
                            html = render_html(template, invoice_data)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_filename = f"{selected_id}_{timestamp}.pdf"
                            output_path = os.path.join('output', output_filename)

                            success = generate_pdf(html, output_path)
                            if success:
                                st.success("✅ PDF сгенерирован успешно!")
                                add_generation_record(selected_id, invoice_data.get('customer_name', ''), data_file, template_name, output_path, 'success')

                                # Предпросмотр и скачивание
                                with open(output_path, 'rb') as f:
                                    pdf_bytes = f.read()
                                st.download_button("📥 Скачать PDF", pdf_bytes, file_name=output_filename, key="download_single")
                                if st.button("👀 Открыть PDF", key="open_single_btn"):
                                    open_pdf(output_path)
                            else:
                                st.error("❌ Ошибка генерации PDF")
                                add_generation_record(selected_id, '', data_file, template_name, '', 'error', 'Generation failed')

                # Пакетная генерация
                st.subheader("Пакетная генерация")
                selected_ids = st.multiselect("Выберите ID счетов для пакетной генерации", invoice_ids, key="batch_multiselect")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Выбрать все", key="select_all_btn"):
                        st.session_state['batch_ids'] = invoice_ids
                        st.rerun()
                with col2:
                    if st.button("❌ Очистить выбор", key="clear_selection_btn"):
                        st.session_state['batch_ids'] = []
                        st.rerun()

                if 'batch_ids' in st.session_state:
                    selected_ids = st.session_state['batch_ids']

                if selected_ids and st.button("🚀 Сгенерировать все выбранные PDF", key="generate_batch_btn"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    pdf_files = []

                    for i, invoice_id in enumerate(selected_ids):
                        status_text.text(f"Генерация {i+1}/{len(selected_ids)}: {invoice_id}")
                        invoice_data = get_invoice_data(data, invoice_id)
                        if invoice_data:
                            html = render_html(template, invoice_data)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_filename = f"{invoice_id}_{timestamp}.pdf"
                            output_path = os.path.join('output', output_filename)
                            success = generate_pdf(html, output_path)
                            if success:
                                pdf_files.append(output_path)
                                add_generation_record(invoice_id, invoice_data.get('customer_name', ''), data_file, template_name, output_path, 'success')
                        progress_bar.progress((i + 1) / len(selected_ids))

                    status_text.text("Завершено!")
                    if pdf_files:
                        zip_filename = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                        zip_path = os.path.join('output', zip_filename)
                        create_zip_archive(pdf_files, zip_path)
                        with open(zip_path, 'rb') as f:
                            zip_bytes = f.read()
                        st.download_button("📦 Скачать все как ZIP", zip_bytes, file_name=zip_filename, key="download_batch")
                        st.success(f"✅ Сгенерировано {len(pdf_files)} PDF файлов")
                    else:
                        st.error("❌ Не удалось сгенерировать ни одного PDF")
        except Exception as e:
            st.error(f"❌ Ошибка: {e}")

# Вкладка истории
with tab_history:
    st.header("📜 История генераций")

    # Статистика
    stats = get_statistics()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего генераций", stats['total'])
    with col2:
        st.metric("Сегодня", stats['today'])
    with col3:
        st.metric("За неделю", stats['week'])

    # Фильтры
    st.subheader("Фильтры")
    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input("Дата от", key="date_from")
        invoice_filter = st.text_input("Фильтр по ID счета", key="invoice_filter")
    with col2:
        date_to = st.date_input("Дата до", key="date_to")
        template_filter = st.text_input("Фильтр по шаблону", key="template_filter")

    filters = {}
    if date_from:
        filters['date_from'] = date_from.strftime('%Y-%m-%d')
    if date_to:
        filters['date_to'] = date_to.strftime('%Y-%m-%d')
    if invoice_filter:
        filters['invoice_id'] = invoice_filter
    if template_filter:
        filters['template_name'] = template_filter

    # Получение истории
    history = get_history(limit=100, filters=filters)
    if history:
        df_history = pd.DataFrame(history)
        df_history['timestamp'] = pd.to_datetime(df_history['timestamp']).dt.strftime('%d.%m.%Y %H:%M')
        st.dataframe(df_history[['timestamp', 'invoice_id', 'customer_name', 'data_file', 'template_name', 'status']], use_container_width=True)

        # Действия с записями
        st.subheader("Действия с записью")
        selected_record_id = st.selectbox("Выберите запись", df_history['id'].tolist(), key="record_select")

        if selected_record_id:
            record = df_history[df_history['id'] == selected_record_id].iloc[0]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if os.path.exists(record['output_file']) and st.button("📥 Скачать повторно", key="download_again_btn"):
                    with open(record['output_file'], 'rb') as f:
                        pdf_bytes = f.read()
                    st.download_button("Скачать PDF", pdf_bytes, file_name=os.path.basename(record['output_file']), key="download_record")
            with col2:
                if os.path.exists(record['output_file']) and st.button("👀 Открыть PDF", key="open_record_btn"):
                    open_pdf(record['output_file'])
            with col3:
                if st.button("🔄 Пересоздать PDF", key="regenerate_btn"):
                    # Логика пересоздания - упрощенная версия
                    st.info("Функция пересоздания будет реализована в следующей версии")
            with col4:
                if st.button("🗑️ Удалить запись", key="delete_record_btn"):
                    if delete_record(selected_record_id):
                        st.success("✅ Запись удалена")
                        st.rerun()
                    else:
                        st.error("❌ Ошибка удаления")

    # Очистка истории
    st.subheader("Управление историей")
    if st.button("🗑️ Очистить всю историю", key="clear_history_btn"):
        if st.checkbox("Подтвердить очистку истории"):
            clear_history()
            st.success("✅ История очищена")
            st.rerun()

# Футер
st.markdown("---")
st.markdown("**PDF Generator App** - Генерация PDF из CSV/JSON данных с HTML шаблонами")
