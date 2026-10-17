import json,sys
FIELDS={"student.id":"s.student_id","student.name":"s.name","student.spi":"s.spi","course.id":"c.course_id","course.name":"c.name","registration.student_id":"r.student_id","registration.course_id":"r.course_id"}
OPS={"=","!=",">",">=","<","<=","LIKE"}
def build(x):
 cols=x.get("columns",["student.name","course.name"])
 if not cols:raise ValueError("columns cannot be empty")
 try:select=", ".join(FIELDS[c] for c in cols)
 except KeyError as e:raise ValueError("column not allowed: "+str(e))
 where=[];params=[]
 for f in x.get("filters",[]):
  if f["field"] not in FIELDS or f["op"] not in OPS:raise ValueError("unsafe field/operator")
  where.append(FIELDS[f["field"]]+" "+f["op"]+" %s");params.append(f["value"])
 order=x.get("order_by");order_sql=""
 if order:
  if order["field"] not in FIELDS or order.get("direction","ASC").upper() not in {"ASC","DESC"}:raise ValueError("invalid order")
  order_sql=" ORDER BY "+FIELDS[order["field"]]+" "+order.get("direction","ASC").upper()
 limit=x.get("limit",100)
 if type(limit)!=int or not 1<=limit<=1000:raise ValueError("limit must be 1..1000")
 sql="SELECT "+select+" FROM Student s JOIN CourseRegistration r ON r.student_id=s.student_id JOIN Course c ON c.course_id=r.course_id"
 if where:sql+=" WHERE "+" AND ".join(where)
 return sql+order_sql+" LIMIT %s",params+[limit]
if __name__=="__main__":
 try:
  sql,p=build(json.load(sys.stdin));print("SQL_OK");print(sql);print("PARAMS",json.dumps(p))
 except Exception as e:print("SQL_REJECTED:",e,file=sys.stderr);sys.exit(1)
