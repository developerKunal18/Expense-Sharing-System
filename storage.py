import json
from config import DATA_DIR, MEMBERS_FILE, EXPENSES_FILE


def initialize_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in (MEMBERS_FILE, EXPENSES_FILE):
        if not file_path.exists():
            write_data(file_path, [])


def read_data(file_path):
    initialize_storage()

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"{file_path.name} must contain a JSON list.")

        return data

    except json.JSONDecodeError as error:
        raise ValueError(
            f"{file_path.name} contains invalid JSON. "
            "Restore a valid backup before continuing."
        ) from error


def write_data(file_path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_next_id(records):
    ids = []

    for record in records:
        try:
            ids.append(int(record["id"]))
        except (KeyError, TypeError, ValueError):
            continue

    return max(ids, default=0) + 1
