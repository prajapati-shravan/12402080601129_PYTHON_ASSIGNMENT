import re,sys
from collections import defaultdict,deque
from datetime import datetime
PAT=re.compile(r"^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$")
def solve(data):
 lines=[x.strip() for x in data.splitlines() if x.strip()];x,t=map(int,lines[0].split());n=int(lines[1])
 if len(lines)!=n+2 or x<1 or t<1:raise ValueError("invalid input")
 failed=defaultdict(deque);found={}
 for line in lines[2:]:
  m=PAT.fullmatch(line)
  if not m:continue
  stamp,user,ip,status=m.groups();dt=datetime.strptime(stamp,"%H:%M");now=dt.hour*60+dt.minute;q=failed[user]
  while q and now-q[0][0]>t:q.popleft()
  if status=="FAIL":q.append((now,ip))
  elif len(q)>=x and any(oldip!=ip for _,oldip in q):found.setdefault(user,stamp)
 return "\n".join(f"{u} {found[u]}" for u in sorted(found))
if __name__=="__main__":
 try:print(solve(sys.stdin.read()))
 except Exception as e:print("INPUT_ERROR:",e,file=sys.stderr);sys.exit(1)
