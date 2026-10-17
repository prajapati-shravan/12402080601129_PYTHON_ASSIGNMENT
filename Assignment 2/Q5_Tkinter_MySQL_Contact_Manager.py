"""Install mysql-connector-python and configure MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE."""
import os,re,tkinter as tk
from tkinter import ttk,messagebox
EMAIL=re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
class App:
 def __init__(self,r):
  import mysql.connector
  self.db=mysql.connector.connect(host=os.environ["MYSQL_HOST"],user=os.environ["MYSQL_USER"],password=os.environ["MYSQL_PASSWORD"],database=os.environ["MYSQL_DATABASE"])
  self.db.cursor().execute("CREATE TABLE IF NOT EXISTS Contact(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,email VARCHAR(255) UNIQUE NOT NULL,phone VARCHAR(50),category VARCHAR(100),notes TEXT,INDEX(name),INDEX(phone))");self.db.commit()
  r.title("Contact Manager");r.geometry("900x580");self.v={k:tk.StringVar() for k in ["id","name","email","phone","category","search"]}
  form=ttk.Frame(r);form.pack(fill="x")
  for i,k in enumerate(["name","email","phone","category"]):ttk.Label(form,text=k.title()).grid(row=0,column=i);ttk.Entry(form,textvariable=self.v[k]).grid(row=1,column=i)
  self.notes=tk.Text(form,height=3);self.notes.grid(row=2,column=0,columnspan=4,sticky="ew")
  bar=ttk.Frame(r);bar.pack(fill="x")
  for label,fn in [("Add",self.add),("Update",self.update),("Delete",self.delete),("Refresh",self.refresh)]:ttk.Button(bar,text=label,command=fn).pack(side="left")
  ttk.Entry(bar,textvariable=self.v["search"]).pack(side="left");ttk.Button(bar,text="Search",command=self.search).pack(side="left")
  self.tree=ttk.Treeview(r,columns=("id","name","email","phone","category","notes"),show="headings"); 
  for c in self.tree["columns"]:self.tree.heading(c,text=c.title())
  self.tree.pack(fill="both",expand=True);self.tree.bind("<<TreeviewSelect>>",self.select);self.refresh()
 def data(self):
  n=self.v["name"].get().strip();e=self.v["email"].get().strip()
  if not n or not EMAIL.fullmatch(e):raise ValueError("Name and valid email required")
  return n,e,self.v["phone"].get(),self.v["category"].get(),self.notes.get("1.0","end").strip()
 def add(self):
  try:
   c=self.db.cursor();c.execute("INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",self.data());self.db.commit();self.refresh()
  except Exception as e:messagebox.showerror("Add",str(e))
 def update(self):
  try:
   if not self.v["id"].get():raise ValueError("Select contact")
   c=self.db.cursor();c.execute("UPDATE Contact SET name=%s,email=%s,phone=%s,category=%s,notes=%s WHERE id=%s",self.data()+(self.v["id"].get(),));self.db.commit();self.refresh()
  except Exception as e:messagebox.showerror("Update",str(e))
 def delete(self):
  try:
   c=self.db.cursor();c.execute("DELETE FROM Contact WHERE id=%s",(self.v["id"].get(),));self.db.commit();self.refresh()
  except Exception as e:messagebox.showerror("Delete",str(e))
 def show(self,rows):
  self.tree.delete(*self.tree.get_children())
  for row in rows:self.tree.insert("","end",values=row)
 def refresh(self):
  c=self.db.cursor();c.execute("SELECT id,name,email,phone,category,notes FROM Contact ORDER BY name");self.show(c.fetchall())
 def search(self):
  term="%"+self.v["search"].get()+"%";c=self.db.cursor();c.execute("SELECT id,name,email,phone,category,notes FROM Contact WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s ORDER BY name",(term,term,term));self.show(c.fetchall())
 def select(self,_=None):
  sel=self.tree.selection()
  if not sel:return
  row=self.tree.item(sel[0],"values");self.v["id"].set(row[0])
  for k,val in zip(["name","email","phone","category"],row[1:5]):self.v[k].set(val)
  self.notes.delete("1.0","end");self.notes.insert("1.0",row[5] or "")
if __name__=="__main__":
 try:App(tk.Tk()).__class__
 except Exception as e:print("Startup error:",e)
