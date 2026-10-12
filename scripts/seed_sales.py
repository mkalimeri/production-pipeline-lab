import csv
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = PROJECT_ROOT / "data" / "seed" / "Sales.csv"
DB_PATH = PROJECT_ROOT / "data" / "source" / "stroopwafel.db"

import_timestamp: str = datetime.now(timezone.utc).isoformat()
with sqlite3.connect(DB_PATH) as conn:
    with open(SEED_PATH) as sales_file:
        reader = csv.DictReader(sales_file)
        for row in reader:
            row["total_price"] = int(
                (Decimal(row["total_price"]) * 100).quantize(
                    Decimal("1"), rounding=ROUND_HALF_UP
                )
            )
            row["total_discount"] = int(
                (Decimal(row["total_discount"]) * 100).quantize(
                    Decimal("1"), rounding=ROUND_HALF_UP
                )
            )
            row["source_updated_at"] = import_timestamp
            
            conn.execute(
                """
                INSERT INTO sales (
                    sales_id,
                    date,
                    time,
                    employee_id,
                    total_price,
                    total_discount,
                    weekday,
                    payment_type,
                    source_updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(sales_id) DO NOTHING
                """,
                (
                    row['sales_id'],
                    row['date'],
                    row['time'],
                    row['employee_id'],
                    row['total_price'],
                    row['total_discount'],
                    row['weekday'],
                    row['payment_type'],
                    row['source_updated_at']
                )
            )