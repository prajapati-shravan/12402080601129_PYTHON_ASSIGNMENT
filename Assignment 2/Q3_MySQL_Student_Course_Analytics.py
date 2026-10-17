"""Install mysql-connector-python. Set MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE."""
import csv,os,sys
def rows(path,fields):
 with open(path,newline="",encoding="utf-8-sig") as f:
  r=csv.DictReader(f)
  if not r.fieldnames or not set(fields)<=set(r.fieldnames):raise ValueError(f"{path} needs columns {fields}")
  yield from r
def main(sc,rc,cid,threshold):
 import mysql.connector
 db=mysql.connector.connect(host=os.environ["MYSQL_HOST"],user=os.environ["MYSQL_USER"],password=os.environ["MYSQL_PASSWORD"],database=os.environ["MYSQL_DATABASE"],port=int(os.getenv("MYSQL_PORT","3306")))
 c=db.cursor()
 try:
  c.execute("CREATE TABLE IF NOT EXISTS Student(student_id VARCHAR(64) PRIMARY KEY,name VARCHAR(255) NOT NULL,spi DECIMAL(4,2) NOT NULL)")
  c.execute("CREATE TABLE IF NOT EXISTS CourseRegistration(student_id VARCHAR(64),course_id VARCHAR(64),PRIMARY KEY(student_id,course_id),INDEX idx_course(course_id),FOREIGN KEY(student_id) REFERENCES Student(student_id))");db.commit()
  for r in rows(sc,["student_id","name","spi"]):
   spi=float(r["spi"])
   if not 0<=spi<=10:raise ValueError("SPI out of range")
   c.execute("INSERT INTO Student VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name),spi=VALUES(spi)",(r["student_id"],r["name"],spi))
  for r in rows(rc,["student_id","course_id"]):c.execute("INSERT IGNORE INTO CourseRegistration VALUES(%s,%s)",(r["student_id"],r["course_id"]))
  db.commit();c.execute("SELECT s.student_id,s.name,s.spi,r.course_id FROM Student s JOIN CourseRegistration r ON s.student_id=r.student_id WHERE r.course_id=%s AND s.spi>%s ORDER BY s.spi DESC,s.student_id ASC",(cid,threshold))
  for row in c.fetchall():print(*row)
 finally:c.close();db.close()
if __name__=="__main__":
 try:
  if len(sys.argv)!=5:raise ValueError("Usage: script student.csv registration.csv COURSE_ID SPI_THRESHOLD")
  main(*sys.argv[1:4],float(sys.argv[4]))
 except Exception as e:print("ERROR:",e,file=sys.stderr);sys.exit(1)
