from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from config import CURRENCY


def money(amount):
    return f"{CURRENCY}{Decimal(amount):,.2f}"


def to_paise(amount):
    """Convert a decimal currency amount into integer paise."""
    value = Decimal(str(amount)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    return int(value * 100)


def from_paise(paise):
    return round(paise / 100, 2)


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def input_integer(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt).strip())

            if value < minimum:
                print(f"Enter a whole number of at least {minimum}.")
                continue

            return value

        except ValueError:
            print("Enter a valid whole number.")


def input_amount(prompt):
    while True:
        try:
            value = Decimal(input(prompt).strip())

            if not value.is_finite() or value <= 0:
                print("Enter an amount greater than zero.")
                continue

            value = value.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            if value <= 0:
                print("The amount must be at least ₹0.01.")
                continue

            return float(value)

        except (ValueError, InvalidOperation):
            print("Enter a valid amount, for example 250 or 250.50.")


def current_timestamp():
    return datetime.now().isoformat(timespec="seconds")


def pause():
    input("\nPress Enter to continue...")
