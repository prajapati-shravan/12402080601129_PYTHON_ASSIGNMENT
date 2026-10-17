"""Q4: Validate transaction CSV and split credit/debit/error records."""
import csv, sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {"transaction_id", "account_id", "type", "amount", "timestamp"}

def process_csv(input_path, output_dir="."):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    balances, counts = {}, {"credit": 0, "debit": 0, "error": 0}
    with open(input_path, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
            raise ValueError("CSV header must contain transaction_id, account_id, type, amount, timestamp")
        with (output_dir/"credit.csv").open("w", newline="", encoding="utf-8") as cf, \
             (output_dir/"debit.csv").open("w", newline="", encoding="utf-8") as df, \
             (output_dir/"error.csv").open("w", newline="", encoding="utf-8") as ef:
            credit = csv.DictWriter(cf, fieldnames=reader.fieldnames); credit.writeheader()
            debit = csv.DictWriter(df, fieldnames=reader.fieldnames); debit.writeheader()
            error = csv.DictWriter(ef, fieldnames=list(reader.fieldnames)+["error_reason"]); error.writeheader()
            for row in reader:
                try:
                    if any(not (row.get(key) or "").strip() for key in REQUIRED):
                        raise ValueError("missing required field")
                    kind = row["type"].strip().upper()
                    if kind not in {"CREDIT", "DEBIT"}: raise ValueError("type must be CREDIT or DEBIT")
                    amount = Decimal(row["amount"])
                    if not amount.is_finite() or amount <= 0: raise ValueError("amount must be a positive number")
                    datetime.fromisoformat(row["timestamp"].strip())
                    row["type"] = kind
                    (credit if kind == "CREDIT" else debit).writerow(row)
                    delta = amount if kind == "CREDIT" else -amount
                    account = row["account_id"].strip()
                    balances[account] = balances.get(account, Decimal("0")) + delta
                    counts["credit" if kind == "CREDIT" else "debit"] += 1
                except (ValueError, InvalidOperation, TypeError) as exc:
                    error.writerow({**row, "error_reason": str(exc)})
                    counts["error"] += 1
    summary = sorted(balances.items(), key=lambda item: (-abs(item[1]), item[0]))
    return counts, summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Q4_Exception_Safe_CSV_Transaction_Splitter.py INPUT.csv [OUTPUT_DIR]")
        sys.exit(2)
    try:
        counts, summary = process_csv(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else ".")
        for account, amount in summary: print(f"{account} {amount:f}")
        print(f"FILES credit.csv debit.csv error.csv | CREDIT {counts['credit']} DEBIT {counts['debit']} ERROR {counts['error']}")
    except (OSError, ValueError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr); sys.exit(1)
