"""Q7: Interactive calculator with distinct custom exceptions."""
import re, sys

class FormulaError(Exception): pass
class InvalidFormatError(FormulaError): pass
class UnknownVariableError(FormulaError): pass
class DivisionByZeroError(FormulaError): pass
class UnsupportedOperatorError(FormulaError): pass

NUMBER = r"(?:\d+(?:\.\d*)?|\.\d+)"
OPERAND = rf"(?:{NUMBER}|[A-Za-z_]\w*)"
FORMULA = re.compile(rf"^\s*({OPERAND})\s*([^\s])\s*({OPERAND})\s*$")
ASSIGNMENT = re.compile(rf"^\s*([A-Za-z_]\w*)\s*=\s*({NUMBER})\s*$")

def number(token, variables):
    if re.fullmatch(NUMBER, token): return float(token)
    if token in variables: return variables[token]
    raise UnknownVariableError(f"unknown variable: {token}")

def evaluate(line, variables):
    assignment = ASSIGNMENT.fullmatch(line)
    if assignment:
        variables[assignment.group(1)] = float(assignment.group(2))
        return None
    match = FORMULA.fullmatch(line)
    if not match: raise InvalidFormatError("expected operand operator operand")
    left, op, right = match.groups()
    if op not in {"+", "-", "*", "/", "%"}:
        raise UnsupportedOperatorError(f"unsupported operator: {op}")
    a, b = number(left, variables), number(right, variables)
    if op in {"/", "%"} and b == 0: raise DivisionByZeroError("division or modulo by zero")
    return {"+": lambda: a+b, "-": lambda: a-b, "*": lambda: a*b,
            "/": lambda: a/b, "%": lambda: a%b}[op]()

def format_number(value):
    return str(int(value)) if value.is_integer() else str(value)

def main():
    variables = {}
    for line in sys.stdin:
        line = line.rstrip("\n")
        if line.strip().lower() == "quit": break
        if not line.strip(): continue
        try:
            result = evaluate(line, variables)
            if result is not None: print(format_number(result))
        except FormulaError as exc:
            print(f"{type(exc).__name__}: {exc}")
if __name__ == "__main__": main()
