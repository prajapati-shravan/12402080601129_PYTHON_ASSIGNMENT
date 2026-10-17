"""Q6: Lexicographically smallest topological order or a detected cycle."""
import heapq, sys

def solve(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines: return ""
    n, e = map(int, lines[0].split())
    if len(lines) < n + e + 1: raise ValueError("missing module names or dependency edges")
    modules = lines[1:n+1]
    if len(set(modules)) != n: raise ValueError("module names must be unique")
    graph = {m: [] for m in modules}; indegree = {m: 0 for m in modules}
    for line in lines[n+1:n+e+1]:
        parts = line.split()
        if len(parts) != 3 or parts[1] != "imports": raise ValueError("edge format: module_a imports module_b")
        importer, dependency = parts[0], parts[2]
        if importer not in graph or dependency not in graph: raise ValueError("edge references unknown module")
        # dependency must load before importer
        if importer not in graph[dependency]:
            graph[dependency].append(importer); indegree[importer] += 1
    heap = [m for m in modules if indegree[m] == 0]; heapq.heapify(heap)
    order = []
    while heap:
        module = heapq.heappop(heap); order.append(module)
        for nxt in graph[module]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0: heapq.heappush(heap, nxt)
    if len(order) == n: return " ".join(order)
    remaining = {m for m in modules if indegree[m] > 0}
    color = {}; parent = {}
    def dfs(node):
        color[node] = 1
        for nxt in graph[node]:
            if nxt not in remaining: continue
            if color.get(nxt, 0) == 0:
                parent[nxt] = node
                found = dfs(nxt)
                if found: return found
            elif color.get(nxt) == 1:
                cycle = [nxt]; cur = node
                while cur != nxt:
                    cycle.append(cur); cur = parent[cur]
                cycle.append(nxt); cycle.reverse()
                return cycle
        color[node] = 2
        return None
    for module in sorted(remaining):
        if color.get(module, 0) == 0:
            cycle = dfs(module)
            if cycle: return "CYCLE\n" + " -> ".join(cycle)
    return "CYCLE"
if __name__ == "__main__":
    try: print(solve(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr); sys.exit(1)
