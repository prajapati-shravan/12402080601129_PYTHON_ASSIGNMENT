import json,math,sys
def stream(path):
 with open(path,encoding="utf-8",errors="replace") as f:
  for line in f:
   try:
    x=json.loads(line);d=str(x["device_id"]).strip();t=float(x["temperature_c"]);h=float(x["humidity"])
    if not d or not math.isfinite(t) or not math.isfinite(h) or not 0<=h<=100:raise ValueError()
    yield d,t,False
   except (ValueError,KeyError,TypeError,json.JSONDecodeError):yield None,None,True
def main(path):
 stats={}
 for d,t,bad in stream(path):
  if bad:d="__CORRUPTED_GLOBAL__"
  s=stats.setdefault(d,{"n":0,"min":None,"max":None,"sum":0.0,"bad":0})
  if bad:s["bad"]+=1;continue
  s["n"]+=1;s["sum"]+=t;s["min"]=t if s["min"] is None else min(s["min"],t);s["max"]=t if s["max"] is None else max(s["max"],t)
 for d,s in sorted(stats.items()):print(f"{d} count={s['n']} min={s['min'] if s['min'] is not None else 'NA'} max={s['max'] if s['max'] is not None else 'NA'} avg={s['sum']/s['n'] if s['n'] else 0:.2f} corrupted={s['bad']}")
if __name__=="__main__":
 try:
  if len(sys.argv)!=2:raise ValueError("Usage: script file.jsonl")
  main(sys.argv[1])
 except Exception as e:print("ERROR:",e,file=sys.stderr);sys.exit(1)
