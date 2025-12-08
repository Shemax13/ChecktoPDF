"""
Скрипт для создания тестовых данных и шаблонов.

Создает директории и файлы с примерами CSV, JSON и HTML шаблонов.
"""

import os
import json

def create_directories():
    """Создает необходимые директории."""
    directories = ['data', 'templates', 'output']
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Создана директория: {dir_name}")

def create_csv_files():
    """Создает примеры CSV файлов."""
    # invoices_sample1.csv
    csv1_content = """invoice_id,customer_name,date,company_name,address,phone,email,item_1_name,item_1_qty,item_1_price,item_2_name,item_2_qty,item_2_price,item_3_name,item_3_qty,item_3_price
INV-2025-001,Иванов Петр Сергеевич,15.01.2025,ООО "ТехноСервис",г. Москва ул. Ленина д.10,+7-495-123-45-67,info@techservice.ru,Ноутбук Lenovo ThinkPad,2,85000,Мышь Logitech MX Master,2,7500,Клавиатура Keychron K8,1,12000
INV-2025-002,Петрова Анна Ивановна,16.01.2025,ИП Петрова А.И.,г. Санкт-Петербург пр. Невский д.25,+7-812-987-65-43,petrova@mail.ru,Монитор Dell 27",1,32000,Веб-камера Logitech C920,1,8500,Наушники Sony WH-1000XM4,1,25000
INV-2025-003,Сидоров Алексей Викторович,17.01.2025,ООО "ПроектСтрой",г. Рязань ул. Соборная д.5,+7-4912-55-44-33,sidorov@proekt.ru,Принтер HP LaserJet,1,45000,Бумага А4 (500 листов),10,350,Картриджи HP (комплект),2,8500
INV-2025-004,Козлова Мария Дмитриевна,18.01.2025,Фриланс,г. Казань ул. Баумана д.48,+7-843-222-33-44,kozlova.m@gmail.com,Планшет iPad Air,1,62000,Чехол для iPad,1,3500,Apple Pencil,1,11000
INV-2025-005,Морозов Игорь Андреевич,19.01.2025,ООО "КонсалтПлюс",г. Екатеринбург ул. Малышева д.15,+7-343-111-22-33,info@konsalt.ru,Роутер ASUS RT-AX88U,2,18000,Сетевой кабель CAT6 (50м),3,1200,Коммутатор TP-Link 8-port,1,4500"""

    with open('data/invoices_sample1.csv', 'w', encoding='utf-8') as f:
        f.write(csv1_content)
    print("✅ Создан файл: data/invoices_sample1.csv")

    # invoices_sample2.csv
    csv2_content = """invoice_id;customer_name;date;company_name;item_1_name;item_1_qty;item_1_price;item_2_name;item_2_qty;item_2_price
INV-2025-006;Новиков Дмитрий Олегович;20.01.2025;ИП Новиков;Смартфон Samsung Galaxy S24;1;89000;Защитное стекло;2;1500
INV-2025-007;Федорова Елена Сергеевна;21.01.2025;ООО "МедиаГрупп";Фотоаппарат Canon EOS R6;1;185000;Объектив Canon RF 24-105mm;1;95000
INV-2025-008;Волков Сергей Николаевич;22.01.2025;ИП Волков С.Н.;SSD диск Samsung 1TB;3;12000;Внешний HDD Seagate 4TB;1;8500"""

    with open('data/invoices_sample2.csv', 'w', encoding='utf-8') as f:
        f.write(csv2_content)
    print("✅ Создан файл: data/invoices_sample2.csv")

def create_json_files():
    """Создает примеры JSON файлов."""
    # orders_sample1.json
    json1_data = [
        {
            "invoice_id": "ORD-2025-101",
            "customer_name": "Соколов Владимир Петрович",
            "date": "23.01.2025",
            "company_name": "ООО 'ЭлектроТехника'",
            "address": "г. Новосибирск ул. Красный проспект д.77",
            "phone": "+7-383-555-66-77",
            "email": "sokolov@electro.ru",
            "items": [
                {"product_name": "Источник бесперебойного питания APC 1500VA", "quantity": 2, "price": 22000, "total": 44000},
                {"product_name": "Стабилизатор напряжения 5кВт", "quantity": 1, "price": 18000, "total": 18000},
                {"product_name": "Удлинитель сетевой 5м", "quantity": 5, "price": 850, "total": 4250}
            ],
            "grand_total": 66250
        },
        {
            "invoice_id": "ORD-2025-102",
            "customer_name": "Лебедева Ольга Викторовна",
            "date": "24.01.2025",
            "company_name": "ИП Лебедева О.В.",
            "address": "г. Краснодар ул. Красная д.120",
            "phone": "+7-861-444-55-66",
            "email": "lebedeva@yandex.ru",
            "items": [
                {"product_name": "Кондиционер Daikin 12000 BTU", "quantity": 1, "price": 45000, "total": 45000},
                {"product_name": "Монтаж и установка", "quantity": 1, "price": 8000, "total": 8000},
                {"product_name": "Медные трубы 5м", "quantity": 1, "price": 3500, "total": 3500}
            ],
            "grand_total": 56500
        },
        {
            "invoice_id": "ORD-2025-103",
            "customer_name": "Григорьев Андрей Максимович",
            "date": "25.01.2025",
            "company_name": "ООО 'АвтоЗапчасти'",
            "items": [
                {"product_name": "Моторное масло Shell 5W-40 4л", "quantity": 10, "price": 2200, "total": 22000},
                {"product_name": "Масляный фильтр Mann", "quantity": 10, "price": 450, "total": 4500},
                {"product_name": "Воздушный фильтр Bosch", "quantity": 8, "price": 650, "total": 5200}
            ],
            "grand_total": 31700
        }
    ]

    with open('data/orders_sample1.json', 'w', encoding='utf-8') as f:
        json.dump(json1_data, f, ensure_ascii=False, indent=2)
    print("✅ Создан файл: data/orders_sample1.json")

    # orders_sample2.json
    json2_data = {
        "orders": [
            {
                "invoice_id": "ORD-2025-104",
                "customer_name": "Захаров Николай Александрович",
                "date": "26.01.2025",
                "items": [
                    {"product_name": "Кофемашина DeLonghi", "quantity": 1, "price": 35000, "total": 35000},
                    {"product_name": "Кофе в зернах 1кг", "quantity": 3, "price": 1800, "total": 5400}
                ],
                "grand_total": 40400
            },
            {
                "invoice_id": "ORD-2025-105",
                "customer_name": "Романова Татьяна Игоревна",
                "date": "27.01.2025",
                "items": [
                    {"product_name": "Пылесос Dyson V15", "quantity": 1, "price": 52000, "total": 52000},
                    {"product_name": "Фильтр HEPA для Dyson", "quantity": 2, "price": 2500, "total": 5000}
                ],
                "grand_total": 57000
            }
        ]
    }

    with open('data/orders_sample2.json', 'w', encoding='utf-8') as f:
        json.dump(json2_data, f, ensure_ascii=False, indent=2)
    print("✅ Создан файл: data/orders_sample2.json")

def create_html_templates():
    """Создает HTML шаблоны."""
    # invoice_template.html
    invoice_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {
            font-family: 'DejaVu Sans';
            src: url('https://cdn.jsdelivr.net/npm/dejavu-sans@1.0.0/ttf/DejaVuSans.ttf');
        }
        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            margin: 40px;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 15px;
        }
        .info {
            margin-bottom: 20px;
            line-height: 1.8;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        .total {
            text-align: right;
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>СЧЁТ № {{ invoice_id }}</h1>
        <p>от {{ date }}</p>
    </div>

    <div class="info">
        <p><strong>Покупатель:</strong> {{ customer_name }}</p>
        {% if company_name %}<p><strong>Компания:</strong> {{ company_name }}</p>{% endif %}
        {% if address %}<p><strong>Адрес:</strong> {{ address }}</p>{% endif %}
        {% if phone %}<p><strong>Телефон:</strong> {{ phone }}</p>{% endif %}
        {% if email %}<p><strong>Email:</strong> {{ email }}</p>{% endif %}
    </div>

    <table>
        <thead>
            <tr>
                <th>№</th>
                <th>Наименование товара</th>
                <th>Количество</th>
                <th>Цена</th>
                <th>Сумма</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ item.product_name }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.price }} ₽</td>
                <td>{{ item.total }} ₽</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="total">
        <p>ИТОГО: {{ grand_total }} ₽</p>
    </div>
</body>
</html>"""

    with open('templates/invoice_template.html', 'w', encoding='utf-8') as f:
        f.write(invoice_html)
    print("✅ Создан файл: templates/invoice_template.html")

    # order_template.html
    order_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {
            font-family: 'Roboto';
            src: url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        }
        body { font-family: 'Roboto', sans-serif; margin: 30px; background: #f9f9f9; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        h1 { color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
        table { width: 100%; margin-top: 20px; }
        th { background: #2196F3; color: white; padding: 10px; }
        td { padding: 10px; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Заказ {{ invoice_id }}</h1>
        <p><strong>Клиент:</strong> {{ customer_name }}</p>
        <p><strong>Дата:</strong> {{ date }}</p>

        <table>
            <tr><th>Товар</th><th>Кол-во</th><th>Цена</th><th>Итого</th></tr>
            {% for item in items %}
            <tr>
                <td>{{ item.product_name }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.price }} ₽</td>
                <td><strong>{{ item.total }} ₽</strong></td>
            </tr>
            {% endfor %}
        </table>

        <h2 style="text-align: right; color: #2196F3;">Всего: {{ grand_total }} ₽</h2>
    </div>
</body>
</html>"""

    with open('templates/order_template.html', 'w', encoding='utf-8') as f:
        f.write(order_html)
    print("✅ Создан файл: templates/order_template.html")

    # report_template.html
    report_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'DejaVu Sans', Arial; margin: 25px; font-size: 11px; }
        .header { background: #333; color: white; padding: 15px; margin-bottom: 20px; }
        .data { display: flex; justify-content: space-between; margin-bottom: 15px; }
        table { width: 100%; font-size: 10px; }
        th { background: #666; color: white; padding: 8px; }
        td { padding: 6px; border-bottom: 1px solid #ccc; }
        .footer { margin-top: 20px; text-align: center; font-size: 9px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h2>ОТЧЁТ ПО ДОКУМЕНТУ {{ invoice_id }}</h2>
    </div>

    <div class="data">
        <div><strong>Контрагент:</strong> {{ customer_name }}</div>
        <div><strong>Дата формирования:</strong> {{ date }}</div>
    </div>

    <table>
        <tr><th>Позиция</th><th>Количество</th><th>Стоимость</th></tr>
        {% for item in items %}
        <tr><td>{{ item.product_name }}</td><td>{{ item.quantity }}</td><td>{{ item.total }} ₽</td></tr>
        {% endfor %}
    </table>

    <div class="footer">
        <p>Документ сгенерирован автоматически | Итого: {{ grand_total }} ₽</p>
    </div>
</body>
</html>"""

    with open('templates/report_template.html', 'w', encoding='utf-8') as f:
        f.write(report_html)
    print("✅ Создан файл: templates/report_template.html")

if __name__ == "__main__":
    print("🚀 Создание тестовых данных...")
    create_directories()
    create_csv_files()
    create_json_files()
    create_html_templates()
    print("✅ Все тестовые файлы созданы успешно!")
