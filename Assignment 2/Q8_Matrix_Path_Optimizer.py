import sys
MOD=1000000007
def solve(data):
 lines=[x.split() for x in data.splitlines() if x.strip()]
 n,m=map(int,lines[0])
 if len(lines)!=n+1 or any(len(r)!=m for r in lines[1:]):raise ValueError("bad matrix")
 prev=[None]*m;ways=[0]*m
 for i in range(n):
  cur=[None]*m;cnt=[0]*m
  for j,x in enumerate(lines[i+1]):
   if x.upper()=="X":continue
   v=int(x)
   if i==j==0:cur[j]=v;cnt[j]=1;continue
   cand=[]
   if j and cur[j-1] is not None:cand.append((cur[j-1],cnt[j-1]))
   if prev[j] is not None:cand.append((prev[j],ways[j]))
   if j and prev[j-1] is not None:cand.append((prev[j-1],ways[j-1]))
   if cand:
    best=max(a for a,b in cand);cur[j]=best+v;cnt[j]=sum(b for a,b in cand if a==best)%MOD
  prev,ways=cur,cnt
 return "IMPOSSIBLE" if prev[-1] is None else f"{prev[-1]} {ways[-1]}"
if __name__=="__main__":
 try:print(solve(sys.stdin.read()))
 except Exception as e:print("INPUT_ERROR:",e,file=sys.stderr);sys.exit(1)
