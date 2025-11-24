lines = open("ledger_routes.py", "r", encoding="utf-8").readlines()
lines[70] = "        'title': f\"{transaction['transaction_type'].replace('_', ' ').title()} - {transaction['amount']}\",\n"
open("ledger_routes.py", "w", encoding="utf-8").writelines(lines)
print("Fixed ledger_routes.py syntax error")
