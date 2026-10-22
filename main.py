from storage import initialize_storage
from member_manager import add_member, show_members, search_members
from expense_manager import add_expense, show_expenses, search_expenses
from settlement_manager import show_balances, suggest_settlements
from utils import pause


def display_menu():
    print("\n" + "=" * 46)
    print("        EXPENSE SHARING SYSTEM")
    print("=" * 46)
    print("1. Add Group Member")
    print("2. View All Members")
    print("3. Search Members")
    print("4. Add Shared Expense")
    print("5. View Expense History")
    print("6. Search Expenses")
    print("7. View Member Balances")
    print("8. Suggest Settlements")
    print("0. Exit")
    print("=" * 46)


def main():
    initialize_storage()

    actions = {
        "1": add_member,
        "2": show_members,
        "3": search_members,
        "4": add_expense,
        "5": show_expenses,
        "6": search_expenses,
        "7": show_balances,
        "8": suggest_settlements,
    }

    print("Welcome to the Expense Sharing System!")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you for using the Expense Sharing System.")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid option. Please try again.")
            pause()
            continue

        try:
            action()
        except (ValueError, OSError, KeyError) as error:
            print(f"\nOperation failed: {error}")
            print("Check the data files and try again.")

        pause()


if __name__ == "__main__":
    main()
