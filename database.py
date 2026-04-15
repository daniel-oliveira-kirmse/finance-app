import sqlite3
import hashlib

DB_NAME = "financeiro.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def hash_password(password: str) -> str:
    salt = "FINANCEIRO_APP_SALT_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- USERS ----------------

def create_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    """, (username, password_hash))

    conn.commit()
    conn.close()


def authenticate_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        SELECT id, username FROM users
        WHERE username = ? AND password_hash = ?
    """, (username, password_hash))

    user = cursor.fetchone()
    conn.close()

    return user


def user_exists(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


# ---------------- TRANSACTIONS ----------------

def insert_transaction(user_id, tipo, valor, categoria, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (user_id, tipo, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, tipo, valor, categoria, data))

    conn.commit()
    conn.close()


def update_transaction(transaction_id, user_id, tipo, valor, categoria, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET tipo = ?, valor = ?, categoria = ?, data = ?
        WHERE id = ? AND user_id = ?
    """, (tipo, valor, categoria, data, transaction_id, user_id))

    conn.commit()
    conn.close()


def fetch_transactions(user_id, categoria=None, data_inicio=None, data_fim=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, tipo, valor, categoria, data
        FROM transactions
        WHERE user_id = ?
    """
    params = [user_id]

    if categoria and categoria != "Todas":
        query += " AND categoria = ?"
        params.append(categoria)

    if data_inicio:
        query += " AND data >= ?"
        params.append(data_inicio)

    if data_fim:
        query += " AND data <= ?"
        params.append(data_fim)

    query += " ORDER BY data DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results


def delete_transaction(user_id, transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ? AND user_id = ?
    """, (transaction_id, user_id))

    conn.commit()
    conn.close()


def fetch_categories(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT categoria
        FROM transactions
        WHERE user_id = ?
        ORDER BY categoria ASC
    """, (user_id,))

    categories = [row[0] for row in cursor.fetchall()]

    conn.close()
    return categories


def fetch_summary(user_id, data_inicio=None, data_fim=None):
    conn = get_connection()
    cursor = conn.cursor()

    base_receita = "SELECT COALESCE(SUM(valor), 0) FROM transactions WHERE user_id = ? AND tipo = 'Receita'"
    base_despesa = "SELECT COALESCE(SUM(valor), 0) FROM transactions WHERE user_id = ? AND tipo = 'Despesa'"

    params = [user_id]
    filtro_data = ""

    if data_inicio:
        filtro_data += " AND data >= ?"
        params.append(data_inicio)

    if data_fim:
        filtro_data += " AND data <= ?"
        params.append(data_fim)

    cursor.execute(base_receita + filtro_data, params)
    total_receitas = cursor.fetchone()[0]

    cursor.execute(base_despesa + filtro_data, params)
    total_despesas = cursor.fetchone()[0]

    conn.close()

    saldo = total_receitas - total_despesas
    return total_receitas, total_despesas, saldo


def insert_mock_data(user_id):
    mock_data = [
        ("Receita", 3500.00, "Salário", "2026-04-01"),
        ("Despesa", 120.00, "Academia", "2026-04-02"),
        ("Despesa", 250.50, "Alimentação", "2026-04-03"),
        ("Despesa", 90.00, "Transporte", "2026-04-03"),
        ("Despesa", 80.00, "Lazer", "2026-04-05"),
        ("Receita", 400.00, "Freelance", "2026-04-06"),
        ("Despesa", 180.00, "Alimentação", "2026-04-07"),
        ("Despesa", 60.00, "Transporte", "2026-04-07"),
        ("Despesa", 45.00, "Saúde", "2026-04-08"),
    ]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO transactions (user_id, tipo, valor, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, [(user_id, *row) for row in mock_data])

    conn.commit()
    conn.close()