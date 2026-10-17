import re,sys
from collections import defaultdict
PAT=re.compile(r"(?<![\w.+%-])([A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(?:com|edu|org))(?![A-Za-z0-9.-]))",re.I)
def main(path):
 d=defaultdict(set)
 with open(path,encoding="utf-8",errors="replace") as f:
  for line in f:
   for email,domain in PAT.findall(line): d[domain.lower()].add(email.lower())
 for domain in sorted(d): print(domain,len(d[domain]),min(d[domain]))
if __name__=="__main__":
 if len(sys.argv)!=2: print("Usage: python Q1_Regex_Email_Extractor.py textfile");sys.exit(2)
 try: main(sys.argv[1])
 except OSError as e: print("INPUT_ERROR:",e,file=sys.stderr);sys.exit(1)
