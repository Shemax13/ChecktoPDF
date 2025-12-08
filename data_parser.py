"""
Модуль для парсинга данных из CSV и JSON файлов.

Предоставляет функции для чтения, валидации и обработки данных счетов.
"""

from typing import List, Dict, Tuple
import pandas as pd
import json
import os


def list_data_files() -> List[str]:
    """
    Возвращает список доступных файлов данных (.csv и .json) из директории /data.

    Returns:
        List[str]: Список имен файлов, отсортированных по алфавиту.
    """
    data_dir = 'data'
    if not os.path.exists(data_dir):
        return []
    files = [f for f in os.listdir(data_dir) if f.endswith(('.csv', '.json'))]
    return sorted(files)


def parse_csv(filepath: str) -> pd.DataFrame:
    """
    Парсит CSV файл с автоматическим определением кодировки и разделителя.

    Args:
        filepath (str): Путь к CSV файлу.

    Returns:
        pd.DataFrame: DataFrame с данными из файла.

    Raises:
        ValueError: Если файл не удалось распарсить.
    """
    encodings = ['utf-8', 'cp1251']
    separators = [',', ';', '\t']
    df = None
    for enc in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(filepath, encoding=enc, sep=sep)
                break
            except Exception:
                continue
        if df is not None:
            break
    if df is None:
        raise ValueError("Cannot parse CSV file")
    return df


def parse_json(filepath: str) -> List[Dict]:
    """
    Парсит JSON файл, поддерживая различные структуры данных.

    Args:
        filepath (str): Путь к JSON файлу.

    Returns:
        List[Dict]: Список словарей с данными счетов.

    Raises:
        ValueError: Если структура JSON не поддерживается.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and 'orders' in data:
        return data['orders']
    else:
        raise ValueError("Invalid JSON structure")


def get_invoice_ids(data) -> List[str]:
    """
    Извлекает список ID счетов из данных.

    Args:
        data: DataFrame или список словарей с данными.

    Returns:
        List[str]: Список строковых ID счетов.
    """
    if isinstance(data, pd.DataFrame):
        if 'invoice_id' not in data.columns:
            return []
        return data['invoice_id'].astype(str).tolist()
    elif isinstance(data, list):
        ids = []
        for item in data:
            if 'invoice_id' in item:
                ids.append(str(item['invoice_id']))
        return ids
    return []


def get_invoice_data(data, invoice_id: str) -> Dict:
    """
    Получает полные данные конкретного счета по его ID.

    Args:
        data: DataFrame или список словарей с данными.
        invoice_id (str): ID счета для поиска.

    Returns:
        Dict: Словарь с данными счета, включая нормализованный список товаров.
    """
    if isinstance(data, pd.DataFrame):
        row = data[data['invoice_id'].astype(str) == invoice_id]
        if row.empty:
            return {}
        row = row.iloc[0]
        invoice_data = {
            'invoice_id': str(row['invoice_id']),
            'customer_name': str(row.get('customer_name', '')),
            'date': str(row.get('date', '')),
            'company_name': str(row.get('company_name', '')),
            'address': str(row.get('address', '')),
            'phone': str(row.get('phone', '')),
            'email': str(row.get('email', '')),
            'items': []
        }
        # Парсим товары из колонок вида item_1_name, item_1_qty, item_1_price
        item_cols = [col for col in row.index if col.startswith('item_')]
        items_dict = {}
        for col in item_cols:
            parts = col.split('_')
            if len(parts) >= 3:
                idx = parts[1]
                field = '_'.join(parts[2:])
                if idx not in items_dict:
                    items_dict[idx] = {}
                items_dict[idx][field] = row[col]
        for item in items_dict.values():
            quantity = item.get('qty', 0)
            price = item.get('price', 0)
            total = quantity * price if 'total' not in item else item.get('total', 0)
            invoice_data['items'].append({
                'product_name': item.get('name', ''),
                'quantity': quantity,
                'price': price,
                'total': total
            })
        grand_total = sum(item['total'] for item in invoice_data['items'])
        invoice_data['grand_total'] = grand_total
        return invoice_data
    elif isinstance(data, list):
        for item in data:
            if str(item.get('invoice_id', '')) == invoice_id:
                # Убеждаемся, что у товаров есть поле total
                for it in item.get('items', []):
                    if 'total' not in it:
                        it['total'] = it.get('quantity', 0) * it.get('price', 0)
                if 'grand_total' not in item:
                    item['grand_total'] = sum(it.get('total', 0) for it in item.get('items', []))
                return item
        return {}
    return {}


def validate_data_structure(data) -> Tuple[bool, str]:
    """
    Валидирует структуру данных на наличие обязательных полей.

    Args:
        data: DataFrame или список словарей для валидации.

    Returns:
        Tuple[bool, str]: Кортеж (валидно ли, сообщение об ошибке).
    """
    if isinstance(data, pd.DataFrame):
        required_cols = ['invoice_id', 'customer_name', 'date']
        missing = [col for col in required_cols if col not in data.columns]
        if missing:
            return False, f"Missing columns: {', '.join(missing)}"
        if data.empty:
            return False, "DataFrame is empty"
        return True, ""
    elif isinstance(data, list):
        if not data:
            return False, "Data list is empty"
        for item in data:
            if not isinstance(item, dict):
                return False, "Data items must be dictionaries"
            required_keys = ['invoice_id', 'customer_name', 'date', 'items']
            missing = [key for key in required_keys if key not in item]
            if missing:
                return False, f"Missing keys in item: {', '.join(missing)}"
            items = item.get('items', [])
            if not isinstance(items, list):
                return False, "Items must be a list"
            for it in items:
                if not isinstance(it, dict) or 'product_name' not in it or 'quantity' not in it or 'price' not in it:
                    return False, "Invalid item structure"
        return True, ""
    return False, "Invalid data type"
