import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = PROJECT_ROOT / "data" / "seed" / "Sales.csv"
DB_PATH = PROJECT_ROOT / "data" / "source" / "stroopwafel.db"

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
        row["sales_timestamp"] = datetime.strptime(
            f'{row["date"]} {row["time"]}', "%Y-%m-%d %H:%M:%S"
        )
        print(row)
