lines = open("ledger_routes.py", "r", encoding="utf-8").readlines()
lines[120] = "        'message': f'Transaction recorded: {transaction_id}',\n"
open("ledger_routes.py", "w", encoding="utf-8").writelines(lines)
print("Fixed line 121")
