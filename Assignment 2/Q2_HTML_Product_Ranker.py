import sys,re
from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self): super().__init__();self.items=[];self.cur=None
 def handle_starttag(self,t,a):
  d=dict(a)
  if "data-name" in d and "data-price" in d and "data-rating" in d:self.items.append((d["data-name"],d["data-price"],d["data-rating"]))
def parse(path):
 p=P();p.feed(Path(path).read_text(encoding="utf-8",errors="replace"));out=[]
 for n,price,rating in p.items:
  try:
   price=float(re.sub(r"[^0-9.]","",price));rating=float(rating)
   if n.strip() and price>=0 and 0<=rating<=5:out.append((n.strip(),price,rating))
  except ValueError:pass
 return out
def main():
 try:
  p,k=map(int,sys.stdin.readline().split()); paths=[sys.stdin.readline().strip() for _ in range(p)]
  if not 1<=p<=5000 or not 1<=k<=1000 or any(not x for x in paths):raise ValueError("invalid p/k/path")
  unique={}
  for path in paths:
   for n,pr,r in parse(path):
    key=n.casefold()
    if key not in unique or (-r,pr,key)<(-unique[key][2],unique[key][1],key):unique[key]=(n,pr,r)
  for n,pr,r in sorted(unique.values(),key=lambda x:(-x[2],x[1],x[0].casefold()))[:k]:print(f"{n} {pr:g} {r:g}")
 except Exception as e:print("INPUT_ERROR:",e,file=sys.stderr);sys.exit(1)
if __name__=="__main__":main()
