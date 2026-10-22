from config import EXPENSES_FILE
from storage import read_data, write_data, get_next_id
from member_manager import list_members, find_member
from utils import (
    input_non_empty,
    input_integer,
    input_amount,
    current_timestamp,
    money,
    to_paise,
    from_paise,
)


def list_expenses():
    return read_data(EXPENSES_FILE)


def find_expense(expense_id):
    for expense in list_expenses():
        if expense["id"] == expense_id:
            return expense

    return None


def add_expense():
    members = list_members()

    print("\n--- Add Shared Expense ---")

    if len(members) < 2:
        print("Add at least two group members before creating an expense.")
        return

    print("\nMembers:")

    for member in members:
        print(f"{member['id']}. {member['name']}")

    paid_by_id = input_integer("\nEnter the ID of the person who paid: ")
    payer = find_member(paid_by_id)

    if not payer:
        print("The selected payer does not exist.")
        return

    description = input_non_empty("Expense description: ")
    amount = input_amount("Total expense amount: ")

    print("\nEnter the IDs of the members sharing this expense.")
    print("Separate multiple IDs with commas, for example: 1,2,3")
    print("The payer does not have to be included in the split.")

    raw_ids = input_non_empty("Participant IDs: ")

    try:
        participant_ids = [
            int(value.strip())
            for value in raw_ids.split(",")
        ]
    except ValueError:
        print("Invalid participant IDs.")
        return

    if len(participant_ids) != len(set(participant_ids)):
        print("A member cannot be listed more than once.")
        return

    if not participant_ids:
        print("Select at least one participant.")
        return

    existing_member_ids = {member["id"] for member in members}

    if any(member_id not in existing_member_ids for member_id in participant_ids):
        print("One or more participant IDs do not exist.")
        return

    total_paise = to_paise(amount)

    # Split the amount into integer paise to avoid rounding discrepancies.
    base_share, remainder = divmod(total_paise, len(participant_ids))

    shares = {}

    for index, member_id in enumerate(participant_ids):
        share_paise = base_share + (1 if index < remainder else 0)
        shares[str(member_id)] = from_paise(share_paise)

    expenses = list_expenses()

    expense = {
        "id": get_next_id(expenses),
        "description": description,
        "amount": from_paise(total_paise),
        "paid_by": payer["id"],
        "paid_by_name": payer["name"],
        "participant_ids": participant_ids,
        "shares": shares,
        "created_at": current_timestamp(),
    }

    expenses.append(expense)
    write_data(EXPENSES_FILE, expenses)

    print("\nExpense added successfully.")
    print(f"Expense ID : {expense['id']}")
    print(f"Description: {description}")
    print(f"Paid by    : {payer['name']}")
    print(f"Total      : {money(expense['amount'])}")
    print("\nSplit details:")

    for member_id in participant_ids:
        member = find_member(member_id)
        share = shares[str(member_id)]
        print(f"{member['name']}: {money(share)}")


def show_expenses():
    expenses = list_expenses()

    print("\n--- Expense History ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    members = {member["id"]: member["name"] for member in list_members()}

    for expense in sorted(expenses, key=lambda item: item["id"]):
        print("-" * 45)
        print(f"Expense ID : {expense['id']}")
        print(f"Description: {expense['description']}")
        print(f"Total      : {money(expense['amount'])}")
        print(f"Paid by    : {expense['paid_by_name']}")
        print(f"Date       : {expense['created_at'][:10]}")
        print("Participants:")

        for member_id in expense["participant_ids"]:
            name = members.get(member_id, f"Member #{member_id}")
            share = expense["shares"][str(member_id)]
            print(f"  {name}: {money(share)}")


def search_expenses():
    query = input_non_empty(
        "Search by description or expense ID: "
    ).lower()

    matches = [
        expense for expense in list_expenses()
        if query in expense["description"].lower()
        or query == str(expense["id"])
    ]

    if not matches:
        print("No matching expenses found.")
        return

    for expense in matches:
        print(
            f"ID: {expense['id']} | "
            f"{expense['description']} | "
            f"{money(expense['amount'])} | "
            f"Paid by: {expense['paid_by_name']}"
        )
