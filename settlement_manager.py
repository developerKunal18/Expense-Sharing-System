from member_manager import list_members
from expense_manager import list_expenses
from utils import money, to_paise, from_paise


def calculate_balances():
    members = list_members()
    expenses = list_expenses()

    # Positive balance means the member should receive money.
    # Negative balance means the member owes money.
    balances = {member["id"]: 0 for member in members}

    for expense in expenses:
        payer_id = expense["paid_by"]

        if payer_id in balances:
            balances[payer_id] += to_paise(expense["amount"])

        for member_id in expense["participant_ids"]:
            if member_id not in balances:
                continue

            share = expense["shares"].get(str(member_id), 0)
            balances[member_id] -= to_paise(share)

    return balances


def show_balances():
    members = list_members()

    if not members:
        print("No members found.")
        return

    balances = calculate_balances()
    names = {member["id"]: member["name"] for member in members}

    print("\n--- Member Balances ---")
    print("Positive = should receive money")
    print("Negative = owes money")

    for member in members:
        balance = balances[member["id"]]
        print(f"{member['name']}: {money(from_paise(balance))}")


def suggest_settlements():
    members = list_members()

    if not members:
        print("No members found.")
        return

    balances = calculate_balances()
    names = {member["id"]: member["name"] for member in members}

    creditors = [
        [member_id, balance]
        for member_id, balance in balances.items()
        if balance > 0
    ]

    debtors = [
        [member_id, -balance]
        for member_id, balance in balances.items()
        if balance < 0
    ]

    # Largest amounts first can produce a simple settlement plan.
    creditors.sort(key=lambda item: item[1], reverse=True)
    debtors.sort(key=lambda item: item[1], reverse=True)

    print("\n--- Suggested Settlements ---")

    if not creditors and not debtors:
        print("All expenses are balanced. No payments are needed.")
        return

    i = 0
    j = 0
    transfers = []

    while i < len(debtors) and j < len(creditors):
        debtor_id, amount_owed = debtors[i]
        creditor_id, amount_to_receive = creditors[j]

        transfer_amount = min(amount_owed, amount_to_receive)

        if transfer_amount > 0:
            transfers.append(
                (
                    debtor_id,
                    creditor_id,
                    transfer_amount,
                )
            )

        debtors[i][1] -= transfer_amount
        creditors[j][1] -= transfer_amount

        if debtors[i][1] == 0:
            i += 1

        if creditors[j][1] == 0:
            j += 1

    if not transfers:
        print("No settlement payments are required.")
        return

    for debtor_id, creditor_id, amount in transfers:
        print(
            f"{names[debtor_id]} pays "
            f"{names[creditor_id]}: "
            f"{money(from_paise(amount))}"
        )

    print(f"\nSuggested transfers: {len(transfers)}")
