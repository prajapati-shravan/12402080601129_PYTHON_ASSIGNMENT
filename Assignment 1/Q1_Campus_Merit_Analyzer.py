"""Q1: Campus Merit Analyzer using lists, tuples and dictionaries."""
import sys
from collections import defaultdict

def solve(data: str) -> str:
    tokens = iter(data.split())
    try:
        n, k, m = int(next(tokens)), int(next(tokens)), int(next(tokens))
    except StopIteration:
        return ""
    if not (1 <= n <= 100000 and 1 <= k <= 50 and 1 <= m <= 12):
        raise ValueError("Expected 1<=n<=100000, 1<=k<=50 and 1<=m<=12")

    students = []
    by_semester = defaultdict(list)
    subject_top = [[] for _ in range(m)]
    subject_max = [-1] * m

    for _ in range(n):
        enrollment, name = next(tokens), next(tokens)
        semester, cpi = int(next(tokens)), float(next(tokens))
        marks = tuple(int(next(tokens)) for _ in range(m))
        if not 1 <= semester <= 8 or not 0 <= cpi <= 10 or any(x < 0 or x > 100 for x in marks):
            raise ValueError("Student record contains out-of-range data")
        avg = sum(marks) / m
        student = {"enrollment": enrollment, "name": name, "semester": semester,
                   "cpi": cpi, "marks": marks, "average": avg}
        students.append(student)
        by_semester[semester].append(student)
        for j, mark in enumerate(marks):
            if mark > subject_max[j]:
                subject_max[j] = mark
                subject_top[j] = [enrollment]
            elif mark == subject_max[j]:
                subject_top[j].append(enrollment)

    output = []
    for sem in sorted(by_semester):
        ranked = sorted(by_semester[sem],
                        key=lambda s: (-s["cpi"], -s["average"], s["enrollment"]))
        output.append(f"Semester {sem}: " + " ".join(s["enrollment"] for s in ranked[:k]))
    for j, toppers in enumerate(subject_top, start=1):
        output.append(f"S{j}: " + " ".join(sorted(toppers)))
    return "\n".join(output)

if __name__ == "__main__":
    try:
        print(solve(sys.stdin.read()))
    except (ValueError, StopIteration) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
