"""Q5: OOP bank engine with atomic batch rollback."""
import sys

class BankError(Exception): pass
class AccountNotFound(BankError): pass
class InvalidAmount(BankError): pass
class InsufficientFunds(BankError): pass

class Account:
    def __init__(self, account_id, balance=0):
        if balance < 0: raise InvalidAmount("initial balance cannot be negative")
        self.account_id = account_id
        self._balance = int(balance)
    @property
    def balance(self): return self._balance
    def _change(self, delta):
        new_balance = self._balance + delta
        if new_balance < 0: raise InsufficientFunds(f"insufficient funds in {self.account_id}")
        self._balance = new_balance

class Transaction:
    def __init__(self, kind, accounts, amount):
        self.kind, self.accounts, self.amount = kind, tuple(accounts), amount

class Bank:
    def __init__(self): self.accounts = {}; self.history = []; self.failed_batches = []
    def add_account(self, account_id, balance):
        if account_id in self.accounts: raise BankError(f"duplicate account {account_id}")
        self.accounts[account_id] = Account(account_id, balance)
    def account(self, account_id):
        if account_id not in self.accounts: raise AccountNotFound(f"unknown account {account_id}")
        return self.accounts[account_id]
    def apply(self, operation):
        parts = operation.split()
        if not parts: return
        kind = parts[0].upper()
        if kind in {"DEPOSIT", "WITHDRAW"} and len(parts) == 3:
            acc, amount = parts[1], int(parts[2])
            if amount <= 0: raise InvalidAmount("amount must be positive")
            account = self.account(acc)
            account._change(amount if kind == "DEPOSIT" else -amount)
            self.history.append(Transaction(kind, [acc], amount))
        elif kind == "TRANSFER" and len(parts) == 4:
            src, dst, amount = parts[1], parts[2], int(parts[3])
            if amount <= 0: raise InvalidAmount("amount must be positive")
            source, target = self.account(src), self.account(dst)
            if src == dst: raise BankError("source and destination must differ")
            source._change(-amount)
            target._change(amount)
            self.history.append(Transaction(kind, [src, dst], amount))
        else: raise BankError(f"invalid operation: {operation}")

def solve(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines: return ""
    pos = 0; count = int(lines[pos]); pos += 1
    bank = Bank()
    for _ in range(count):
        acc, balance = lines[pos].split(); pos += 1
        bank.add_account(acc, int(balance))
    q = int(lines[pos]); pos += 1
    operations = lines[pos:pos+q]
    if len(operations) != q: raise ValueError("not enough operations")
    batch = None; batch_number = 0
    for op in operations:
        if batch is not None and "__failed__" in batch and op.upper() != "BATCH_END":
            continue
        if op.upper() == "BATCH_BEGIN":
            if batch is not None: raise ValueError("nested batches are not supported")
            batch_number += 1
            batch = {key: acc.balance for key, acc in bank.accounts.items()}
        elif op.upper() == "BATCH_END":
            if batch is None: raise ValueError("BATCH_END without BATCH_BEGIN")
            batch = None
        else:
            try: bank.apply(op)
            except (BankError, ValueError):
                if batch is not None:
                    for key, balance in batch.items(): bank.accounts[key]._balance = balance
                    bank.failed_batches.append(batch_number)
                    # Ignore remaining operations until BATCH_END.
                    batch = {"__failed__": batch_number}
                # Outside a batch, invalid operations are reported and processing continues.
                else: pass
        if batch is not None and "__failed__" in batch and op.upper() == "BATCH_END":
            batch = None
    if batch is not None and "__failed__" not in batch:
        # An unterminated batch is rolled back.
        for key, balance in batch.items(): bank.accounts[key]._balance = balance
        bank.failed_batches.append(batch_number)
    output = [f"FAILED {number}" for number in bank.failed_batches]
    output += [f"{key} {bank.accounts[key].balance}" for key in sorted(bank.accounts)]
    return "\n".join(output)

if __name__ == "__main__":
    try: print(solve(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr); sys.exit(1)
