"""
Модуль для работы с базой данных истории генераций PDF.

Использует SQLite для хранения записей о сгенерированных документах.
"""

import sqlite3
import os
from typing import List, Dict
from datetime import datetime, timedelta


DB_FILE = 'history.db'


def init_database() -> None:
    """
    Инициализирует базу данных, создавая таблицу generation_history если она не существует.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            invoice_id TEXT NOT NULL,
            customer_name TEXT,
            data_file TEXT NOT NULL,
            template_name TEXT NOT NULL,
            output_file TEXT NOT NULL,
            status TEXT NOT NULL,
            error_message TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_generation_record(invoice_id: str, customer_name: str, data_file: str, template_name: str, output_file: str, status: str, error_msg: str = None) -> int:
    """
    Добавляет запись о генерации PDF в базу данных.

    Args:
        invoice_id (str): ID счета.
        customer_name (str): Имя покупателя.
        data_file (str): Имя файла данных.
        template_name (str): Имя шаблона.
        output_file (str): Путь к выходному файлу.
        status (str): Статус ('success' или 'error').
        error_msg (str, optional): Сообщение об ошибке.

    Returns:
        int: ID добавленной записи.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO generation_history (invoice_id, customer_name, data_file, template_name, output_file, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (invoice_id, customer_name, data_file, template_name, output_file, status, error_msg))
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id


def get_history(limit: int = 100, filters: Dict = None) -> List[Dict]:
    """
    Получает историю генераций с возможными фильтрами.

    Args:
        limit (int): Максимальное количество записей.
        filters (Dict, optional): Словарь фильтров (date_from, date_to, invoice_id, template_name).

    Returns:
        List[Dict]: Список записей истории.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM generation_history WHERE 1=1"
    params = []
    if filters:
        if 'date_from' in filters:
            query += " AND date(timestamp) >= ?"
            params.append(filters['date_from'])
        if 'date_to' in filters:
            query += " AND date(timestamp) <= ?"
            params.append(filters['date_to'])
        if 'invoice_id' in filters:
            query += " AND invoice_id LIKE ?"
            params.append(f"%{filters['invoice_id']}%")
        if 'template_name' in filters:
            query += " AND template_name LIKE ?"
            params.append(f"%{filters['template_name']}%")
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return results


def get_statistics() -> Dict:
    """
    Получает статистику генераций.

    Returns:
        Dict: Словарь со статистикой (total, today, week).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Общее количество
    cursor.execute("SELECT COUNT(*) FROM generation_history")
    total = cursor.fetchone()[0]
    # Сегодня
    cursor.execute("SELECT COUNT(*) FROM generation_history WHERE date(timestamp) = date('now')")
    today = cursor.fetchone()[0]
    # За неделю
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM generation_history WHERE date(timestamp) >= ?", (week_ago,))
    week = cursor.fetchone()[0]
    conn.close()
    return {
        'total': total,
        'today': today,
        'week': week
    }


def delete_record(record_id: int) -> bool:
    """
    Удаляет запись из истории по ID.

    Args:
        record_id (int): ID записи для удаления.

    Returns:
        bool: True если удаление успешно, False в противном случае.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM generation_history WHERE id = ?", (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def clear_history() -> bool:
    """
    Очищает всю историю генераций.

    Returns:
        bool: True если очистка успешна.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM generation_history")
    conn.commit()
    conn.close()
    return True
