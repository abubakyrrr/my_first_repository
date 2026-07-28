import sqlite3

DB_PATH = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            is_premium BOOLEAN DEFAULT 0,
            currencies TEXT DEFAULT '',
            cities TEXT DEFAULT ''
        )
    ''')

    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT is_premium, currencies, cities FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "is_premium": bool(row[0]),
            "currencies": row[1].split(",") if row[1] else [],
            "cities": row[2].split(",") if row[2] else []
        }
    return None

def add_user(user_id: int):
    if not get_user(user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()

def set_premium(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_premium = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user_selection(user_id: int, currencies: list, cities: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    curr_str = ",".join(currencies)
    cities_str = ",".join(cities)
    cursor.execute(
        "UPDATE users SET currencies = ?, cities = ? WHERE user_id = ?",
        (curr_str, cities_str, user_id)
    )
    conn.commit()
    conn.close()