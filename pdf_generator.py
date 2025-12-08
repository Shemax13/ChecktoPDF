"""
Модуль для генерации PDF документов из HTML шаблонов с использованием Jinja2 и WeasyPrint.

Поддерживает пакетную генерацию, архивацию и открытие PDF файлов.
"""

from typing import List, Dict
import jinja2
import weasyprint
import os
import platform
import subprocess
import zipfile
from datetime import datetime


def list_templates() -> List[str]:
    """
    Возвращает список доступных HTML шаблонов из директории /templates.

    Returns:
        List[str]: Список имен файлов шаблонов (.html), отсортированных по алфавиту.
    """
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        return []
    files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
    return sorted(files)


def load_template(template_name: str) -> jinja2.Template:
    """
    Загружает HTML шаблон из файла.

    Args:
        template_name (str): Имя файла шаблона (без пути).

    Returns:
        jinja2.Template: Загруженный шаблон Jinja2.

    Raises:
        FileNotFoundError: Если шаблон не найден.
    """
    template_path = os.path.join('templates', template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} not found")
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return jinja2.Template(content)


def render_html(template: jinja2.Template, data: Dict) -> str:
    """
    Рендерит HTML из шаблона с данными.

    Args:
        template (jinja2.Template): Шаблон Jinja2.
        data (Dict): Данные для подстановки в шаблон.

    Returns:
        str: Рендеренный HTML код.
    """
    return template.render(**data)


def generate_pdf(html: str, output_path: str) -> bool:
    """
    Генерирует PDF из HTML строки и сохраняет в файл.

    Args:
        html (str): HTML код для конвертации.
        output_path (str): Путь для сохранения PDF файла.

    Returns:
        bool: True если генерация успешна, False в противном случае.
    """
    try:
        weasyprint.HTML(string=html).write_pdf(output_path)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


def generate_batch_pdf(invoice_ids: List[str], data, template: jinja2.Template) -> List[str]:
    """
    Генерирует PDF для нескольких счетов и возвращает список путей к файлам.

    Args:
        invoice_ids (List[str]): Список ID счетов для генерации.
        data: Данные (DataFrame или список словарей).
        template (jinja2.Template): Шаблон для рендеринга.

    Returns:
        List[str]: Список путей к сгенерированным PDF файлам.
    """
    from data_parser import get_invoice_data  # Импорт здесь для избежания циклических зависимостей

    output_files = []
    for invoice_id in invoice_ids:
        invoice_data = get_invoice_data(data, invoice_id)
        if not invoice_data:
            continue
        html = render_html(template, invoice_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{invoice_id}_{timestamp}.pdf"
        output_path = os.path.join('output', filename)
        if generate_pdf(html, output_path):
            output_files.append(output_path)
    return output_files


def create_zip_archive(pdf_files: List[str], output_path: str) -> str:
    """
    Создает ZIP архив из списка PDF файлов.

    Args:
        pdf_files (List[str]): Список путей к PDF файлам.
        output_path (str): Путь для сохранения ZIP архива.

    Returns:
        str: Путь к созданному ZIP файлу.
    """
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for pdf_file in pdf_files:
            zipf.write(pdf_file, os.path.basename(pdf_file))
    return output_path


def open_pdf(filepath: str) -> None:
    """
    Открывает PDF файл в системной программе просмотра.

    Args:
        filepath (str): Путь к PDF файлу.
    """
    system = platform.system()
    try:
        if system == 'Windows':
            os.startfile(filepath)
        elif system == 'Darwin':  # macOS
            subprocess.call(['open', filepath])
        else:  # Linux
            subprocess.call(['xdg-open', filepath])
    except Exception as e:
        print(f"Error opening PDF: {e}")
