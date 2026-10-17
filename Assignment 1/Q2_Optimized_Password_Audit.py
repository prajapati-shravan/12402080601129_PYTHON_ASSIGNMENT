"""Q2: Password audit with Aho-Corasick matching for banned words."""
import sys
from collections import deque

SPECIAL = set("$#@")

class AhoCorasick:
    def __init__(self, words):
        self.next = [{}]
        self.fail = [0]
        self.output = [False]
        for word in words:
            node = 0
            for ch in word.lower():
                if ch not in self.next[node]:
                    self.next[node][ch] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.output.append(False)
                node = self.next[node][ch]
            self.output[node] = True
        queue = deque()
        for child in self.next[0].values():
            queue.append(child)
        while queue:
            node = queue.popleft()
            self.output[node] = self.output[node] or self.output[self.fail[node]]
            for ch, child in self.next[node].items():
                fallback = self.fail[node]
                while fallback and ch not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.next[fallback].get(ch, 0)
                queue.append(child)

    def contains_banned(self, text):
        node = 0
        for ch in text.lower():
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            if self.output[node]:
                return True
        return False

def classify(password, matcher):
    if not 6 <= len(password) <= 12:
        return "WEAK_LENGTH"
    if any(password[i] == password[i-1] == password[i-2] == password[i-3]
           for i in range(3, len(password))):
        return "WEAK_PATTERN"
    if matcher.contains_banned(password):
        return "COMPROMISED"
    if not (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in SPECIAL for c in password)):
        return "WEAK_PATTERN"
    return "STRONG"

def solve(data):
    lines = data.splitlines()
    if not lines:
        return ""
    pos = 0
    b = int(lines[pos].strip()); pos += 1
    if b < 1:
        raise ValueError("At least one banned word is required")
    banned = []
    for _ in range(b):
        if pos >= len(lines): raise ValueError("Missing banned word")
        banned.append(lines[pos].strip()); pos += 1
    if pos >= len(lines): raise ValueError("Missing password count")
    n = int(lines[pos].strip()); pos += 1
    passwords = lines[pos:pos+n]
    if len(passwords) != n: raise ValueError("Missing password lines")
    matcher = AhoCorasick(banned)
    return "\n".join(f"{i}: {classify(p.strip(), matcher)}"
                     for i, p in enumerate(passwords, 1))

if __name__ == "__main__":
    try: print(solve(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr); sys.exit(1)
