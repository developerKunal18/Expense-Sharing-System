from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

MEMBERS_FILE = DATA_DIR / "members.json"
EXPENSES_FILE = DATA_DIR / "expenses.json"

CURRENCY = "₹"
