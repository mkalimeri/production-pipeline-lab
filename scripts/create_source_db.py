import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "source" / "stroopwafel.db"

def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.Connection(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sales_id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                employee_id INTEGER NOT NULL,
                total_price INTEGER NOT NULL,
                total_discount INTEGER,
                weekday TEXT,
                payment_type TEXT,
                source_updated_at TEXT NOT NULL
            )
            """
        )

if __name__ == "__main__":
    create_database()
    print(f"Database created at {DB_PATH}")