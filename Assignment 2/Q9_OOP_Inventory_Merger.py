import json,sys
class Product:
 def __init__(self,id,name,stock,purchase,selling):
  self.id=str(id);self.name=str(name);self.stock=int(stock);self.purchase=int(purchase);self.selling=int(selling)
  if min(self.stock,self.purchase,self.selling)<0:raise ValueError("negative product value")
class Inventory:
 def __init__(self,items=()):self.items={p.id:p for p in items}
 @classmethod
 def load(cls,path):
  data=json.load(open(path,encoding="utf-8"));return cls(Product(**{"id":x["id"],"name":x["name"],"stock":x["stock"],"purchase":x["purchase"],"selling":x["selling"]}) for x in data)
 def __add__(self,other):
  out=Inventory(self.items.values())
  for pid,p in other.items.items():
   if pid not in out.items:out.items[pid]=p
   else:
    q=out.items[pid]
    if q.name!=p.name:raise ValueError("conflicting product names")
    q.stock+=p.stock;q.purchase=min(q.purchase,p.purchase);q.selling=max(q.selling,p.selling)
  return out
 def value(self):return sum(p.stock*p.purchase for p in self.items.values())
 def save(self,path):json.dump([vars(p) for p in self.items.values()],open(path,"w",encoding="utf-8"),indent=2)
if __name__=="__main__":
 try:
  a,b=Inventory.load(sys.argv[1]),Inventory.load(sys.argv[2]);c=a+b
  if len(sys.argv)>3:c.save(sys.argv[3])
  for pid,p in sorted(c.items.items()):print(f"{pid} {p.name} stock={p.stock} purchase={p.purchase} selling={p.selling}")
  print("TOTAL_PURCHASE_VALUE",c.value())
 except Exception as e:print("ERROR:",e,file=sys.stderr);sys.exit(1)
