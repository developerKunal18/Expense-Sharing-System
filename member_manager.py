from config import MEMBERS_FILE
from storage import read_data, write_data, get_next_id
from utils import input_non_empty, current_timestamp


def list_members():
    return read_data(MEMBERS_FILE)


def find_member(member_id):
    for member in list_members():
        if member["id"] == member_id:
            return member

    return None


def add_member():
    members = list_members()

    print("\n--- Add Group Member ---")

    name = input_non_empty("Enter member name: ")
    email = input("Enter email address (optional): ").strip()

    if email and any(
        member["email"].lower() == email.lower()
        for member in members
        if member.get("email")
    ):
        print("A member with this email already exists.")
        return

    member = {
        "id": get_next_id(members),
        "name": name,
        "email": email,
        "created_at": current_timestamp(),
    }

    members.append(member)
    write_data(MEMBERS_FILE, members)

    print(f"Member added successfully. Member ID: {member['id']}")


def show_members():
    members = list_members()

    print("\n--- Group Members ---")

    if not members:
        print("No members added yet.")
        return

    for member in members:
        print("-" * 35)
        print(f"ID    : {member['id']}")
        print(f"Name  : {member['name']}")
        print(f"Email : {member.get('email') or '-'}")


def search_members():
    query = input_non_empty("Search by member name or ID: ").lower()

    matches = [
        member
        for member in list_members()
        if query in member["name"].lower()
        or query == str(member["id"])
    ]

    if not matches:
        print("No matching members found.")
        return

    for member in matches:
        print(
            f"ID: {member['id']} | "
            f"Name: {member['name']} | "
            f"Email: {member.get('email') or '-'}"
        )
