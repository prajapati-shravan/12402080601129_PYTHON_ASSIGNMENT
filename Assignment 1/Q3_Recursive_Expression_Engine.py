"""Q3: Safe expression evaluator with variable memoization and cycle detection."""
import re, sys

TOKEN_RE = re.compile(r"\s*(\d+|[A-Za-z_]\w*|[()+*-])")

class InvalidExpression(Exception): pass
class CycleDetected(Exception): pass

def tokenize(text):
    tokens, pos = [], 0
    while pos < len(text):
        match = TOKEN_RE.match(text, pos)
        if not match:
            if text[pos:].strip() == "": break
            raise InvalidExpression("invalid token")
        tokens.append(match.group(1)); pos = match.end()
    return tokens

class Evaluator:
    def __init__(self, definitions):
        self.definitions = definitions
        self.memo = {}
        self.active = set()

    def variable(self, name):
        if name not in self.definitions: raise InvalidExpression(f"unknown variable: {name}")
        if name in self.memo: return self.memo[name]
        if name in self.active: raise CycleDetected()
        self.active.add(name)
        try:
            value = self.expression(self.definitions[name])
            self.memo[name] = value
            return value
        finally:
            self.active.remove(name)

    def expression(self, text):
        tokens = tokenize(text)
        if not tokens: raise InvalidExpression("empty expression")
        pos = 0
        def factor():
            nonlocal pos
            if pos >= len(tokens): raise InvalidExpression("expected operand")
            tok = tokens[pos]; pos += 1
            if tok == "(":
                value = add_sub()
                if pos >= len(tokens) or tokens[pos] != ")":
                    raise InvalidExpression("missing closing parenthesis")
                pos += 1
                return value
            if tok.isdigit(): return int(tok)
            if re.fullmatch(r"[A-Za-z_]\w*", tok): return self.variable(tok)
            raise InvalidExpression("expected operand")
        def mul():
            nonlocal pos
            value = factor()
            while pos < len(tokens) and tokens[pos] == "*":
                pos += 1; value *= factor()
            return value
        def add_sub():
            nonlocal pos
            value = mul()
            while pos < len(tokens) and tokens[pos] in ("+", "-"):
                op = tokens[pos]; pos += 1
                rhs = mul()
                value = value + rhs if op == "+" else value - rhs
            return value
        result = add_sub()
        if pos != len(tokens): raise InvalidExpression("unexpected token")
        if not -(2**63) <= result < 2**63: raise InvalidExpression("signed 64-bit overflow")
        return result

def solve(data):
    lines = data.splitlines()
    if not lines: return ""
    count = int(lines[0].strip())
    if len(lines) < count + 2: raise InvalidExpression("missing definitions or expression")
    definitions = {}
    for line in lines[1:count+1]:
        if "=" not in line: raise InvalidExpression("definition must use name = expression")
        name, expr = map(str.strip, line.split("=", 1))
        if not re.fullmatch(r"[A-Za-z_]\w*", name) or name in definitions:
            raise InvalidExpression("invalid or duplicate variable name")
        definitions[name] = expr
    evaluator = Evaluator(definitions)
    try: return str(evaluator.expression("\n".join(lines[count+1:])))
    except CycleDetected: return "CYCLE"
    except InvalidExpression: return "INVALID"

if __name__ == "__main__":
    try: print(solve(sys.stdin.read()))
    except (ValueError, IndexError): print("INVALID")
