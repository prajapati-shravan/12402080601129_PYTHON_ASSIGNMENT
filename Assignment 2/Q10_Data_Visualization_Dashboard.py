import csv,math,sys
from pathlib import Path
def main(src,dst):
 import matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
 out=Path(dst);out.mkdir(parents=True,exist_ok=True)
 with open(src,newline="",encoding="utf-8-sig") as f:
  r=csv.DictReader(f)
  if not r.fieldnames or not {"enrollment","name"}<=set(r.fieldnames):raise ValueError("CSV needs enrollment,name and subject columns")
  subjects=[x for x in r.fieldnames if x not in {"enrollment","name"}];rows=[]
  for raw in r:
   item={"enrollment":raw["enrollment"],"name":raw["name"]}
   for s in subjects:
    try:
     v=float(raw[s])
     item[s]=f"{v:g}" if math.isfinite(v) and 0<=v<=100 else ""
    except (ValueError,TypeError):item[s]=""
   rows.append(item)
 with open(out/"cleaned_marks.csv","w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["enrollment","name"]+subjects);w.writeheader();w.writerows(rows)
 stats={s:[float(r[s]) for r in rows if r[s]!=""] for s in subjects}
 with open(out/"summary.csv","w",newline="",encoding="utf-8") as f:
  w=csv.writer(f);w.writerow(["subject","count","average","minimum","maximum"])
  for s,v in stats.items():w.writerow([s,len(v),f"{sum(v)/len(v):.2f}" if v else "0",min(v) if v else "",max(v) if v else ""])
 grades={"A":0,"B":0,"C":0,"D":0,"F":0}
 performers=[]
 for r in rows:
  vals=[float(r[s]) for s in subjects if r[s]!=""]
  if vals:
   avg=sum(vals)/len(vals);grades["A" if avg>=90 else "B" if avg>=80 else "C" if avg>=70 else "D" if avg>=60 else "F"]+=1;performers.append((avg,r["name"]))
 fig,ax=plt.subplots();ax.bar(list(grades),list(grades.values()));ax.set_title("Grade Distribution");fig.tight_layout();fig.savefig(out/"grade_distribution.png");plt.close(fig)
 fig,ax=plt.subplots();ax.bar(list(stats),[sum(v)/len(v) if v else 0 for v in stats.values()]);ax.set_title("Subject Average");ax.set_ylim(0,100);fig.tight_layout();fig.savefig(out/"subject_average.png");plt.close(fig)
 top=sorted(performers,reverse=True)[:10];fig,ax=plt.subplots();ax.barh([n for _,n in top],[v for v,_ in top]);ax.set_title("Top Performers");fig.tight_layout();fig.savefig(out/"top_performers.png");plt.close(fig)
 print("CLEANED_STUDENTS",len(rows));print("FILES cleaned_marks.csv summary.csv grade_distribution.png subject_average.png top_performers.png")
if __name__=="__main__":
 try:
  if len(sys.argv)!=3:raise ValueError("Usage: script marks.csv output_folder")
  main(*sys.argv[1:])
 except Exception as e:print("ERROR:",e,file=sys.stderr);sys.exit(1)
