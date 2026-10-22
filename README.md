# Expense Sharing System

A beginner-friendly Python console application that helps groups
record shared expenses, calculate individual balances, and plan
settlement payments.

## Features

- Add group members
- Search members
- Record shared expenses
- Split an expense equally among selected participants
- Select a different person as the payer
- View complete expense history
- Search expenses
- Calculate how much each member owes or should receive
- Generate suggested settlement payments
- Store records in JSON files
- Preserve data between application runs

## Technologies

- Python
- JSON
- Python standard library

## Project Structure

```text
ExpenseSharingSystem/
├── main.py
├── config.py
├── storage.py
├── member_manager.py
├── expense_manager.py
├── settlement_manager.py
├── utils.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    ├── members.json
    └── expenses.json
