"""Q9: Deterministic multi-worker job scheduler simulation.

Priority is higher for larger numeric values. Jobs are selected among jobs that
have arrived; equal priorities use earlier arrival time and then input order.
The resources field is validated and reported as input metadata; worker slots
are the simulated execution capacity because the assignment gives no total
resource capacity for the system.
"""
import heapq, sys

def solve(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines: return ""
    w, n = map(int, lines[0].split())
    if w < 1 or n < 1: raise ValueError("w and n must be positive")
    jobs = []
    for idx, line in enumerate(lines[1:n+1]):
        arrival, job_id, priority, duration, resources = line.split()
        job = (int(arrival), idx, job_id, int(priority), int(duration), int(resources))
        if job[0] < 0 or job[3] < 0 or job[4] <= 0 or job[5] <= 0:
            raise ValueError("invalid job values")
        jobs.append(job)
    if len(jobs) != n: raise ValueError("not enough job records")
    jobs.sort()
    waiting = []
    worker_free = [(0, i+1) for i in range(w)]
    heapq.heapify(worker_free)
    result, waits = [], []
    i, now = 0, 0
    while i < n or waiting:
        if not waiting:
            # No ready job: jump directly to the next arrival, not an idle worker's time.
            now = max(now, jobs[i][0])
        else:
            # Ready jobs exist but all workers may be busy; jump to next completion.
            now = max(now, worker_free[0][0])
        while i < n and jobs[i][0] <= now:
            arrival, order, jid, priority, duration, resources = jobs[i]
            heapq.heappush(waiting, (-priority, arrival, order, jid, duration, resources))
            i += 1
        while waiting and worker_free[0][0] <= now:
            free_at, worker_id = heapq.heappop(worker_free)
            neg_priority, arrival, order, jid, duration, resources = heapq.heappop(waiting)
            start = max(now, free_at)
            finish = start + duration
            waits.append(start - arrival)
            result.append((order, f"{jid} W{worker_id} {start} {finish}"))
            heapq.heappush(worker_free, (finish, worker_id))
        if not waiting and i >= n:
            break
    result.sort()
    output = [line for _, line in result]
    output.append(f"AVG_WAIT {sum(waits)/len(waits):.2f}")
    return "\n".join(output)

if __name__ == "__main__":
    try: print(solve(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr); sys.exit(1)
