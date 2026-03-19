import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

def init_db():
    sql.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY
    )
    """)

    sql.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status TEXT
    )
    """)

    db.commit()

def add_user(user_id):
    sql.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    db.commit()

def add_payment(user_id):
    sql.execute(
        "INSERT INTO payments(user_id, status) VALUES(?, ?)",
        (user_id, "pending")
    )
    db.commit()

def get_users():
    sql.execute("SELECT user_id FROM users")
    return sql.fetchall()
