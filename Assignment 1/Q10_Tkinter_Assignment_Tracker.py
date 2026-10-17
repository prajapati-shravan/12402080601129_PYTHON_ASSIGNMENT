"""Q10: Tkinter assignment tracker with JSON persistence and CSV export."""
import csv, json, tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

DATA_FILE = Path(__file__).with_name("assignments.json")
FIELDS = ["enrollment", "name", "assignment", "status", "marks", "remarks"]

class AssignmentTracker:
    def __init__(self, root):
        self.root = root; root.title("Assignment Tracker"); root.geometry("980x620")
        self.records = self.load_data()
        self.vars = {key: tk.StringVar() for key in FIELDS}
        self.vars["status"].set("Pending")
        self.build_ui(); self.refresh()

    def load_data(self):
        try:
            with DATA_FILE.open(encoding="utf-8") as f: data = json.load(f)
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError): return []

    def save_data(self):
        temporary = DATA_FILE.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.records, indent=2), encoding="utf-8")
        temporary.replace(DATA_FILE)

    def build_ui(self):
        form = ttk.LabelFrame(self.root, text="Submission details", padding=10); form.pack(fill="x", padx=12, pady=10)
        labels = [("enrollment","Enrollment"),("name","Student name"),("assignment","Assignment"),
                  ("status","Status"),("marks","Marks"),("remarks","Remarks")]
        for i, (key, label) in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i//3*2, column=i%3, sticky="w", padx=5, pady=(2,0))
            if key == "status":
                widget = ttk.Combobox(form, textvariable=self.vars[key], values=["Pending","Completed"], state="readonly")
            else:
                widget = ttk.Entry(form, textvariable=self.vars[key], width=28)
            widget.grid(row=i//3*2+1, column=i%3, sticky="ew", padx=5, pady=(0,6))
        for col in range(3): form.columnconfigure(col, weight=1)
        actions = ttk.Frame(self.root); actions.pack(fill="x", padx=12)
        ttk.Button(actions, text="Add / Update", command=self.add_record).pack(side="left", padx=3)
        ttk.Button(actions, text="Filter: All", command=lambda:self.refresh("All")).pack(side="left", padx=3)
        ttk.Button(actions, text="Pending", command=lambda:self.refresh("Pending")).pack(side="left", padx=3)
        ttk.Button(actions, text="Completed", command=lambda:self.refresh("Completed")).pack(side="left", padx=3)
        ttk.Button(actions, text="Export CSV", command=self.export_csv).pack(side="right", padx=3)
        self.tree = ttk.Treeview(self.root, columns=FIELDS, show="headings", height=16)
        for field in FIELDS:
            self.tree.heading(field, text=field.title()); self.tree.column(field, width=130 if field != "remarks" else 220)
        self.tree.pack(fill="both", expand=True, padx=12, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)
        self.status_label = ttk.Label(self.root, text="Records are saved locally in assignments.json")
        self.status_label.pack(anchor="w", padx=14, pady=(0,8))

    def add_record(self):
        record = {key: self.vars[key].get().strip() for key in FIELDS}
        if not record["enrollment"] or not record["name"] or not record["assignment"]:
            messagebox.showerror("Validation", "Enrollment, student name and assignment are required."); return
        if record["status"] not in {"Pending","Completed"}:
            messagebox.showerror("Validation", "Choose Pending or Completed."); return
        if record["marks"]:
            try: marks = float(record["marks"])
            except ValueError:
                messagebox.showerror("Validation", "Marks must be numeric."); return
            if marks < 0:
                messagebox.showerror("Validation", "Marks cannot be negative."); return
        else: record["marks"] = ""
        key = (record["enrollment"], record["assignment"])
        existing = next((i for i, r in enumerate(self.records)
                         if (r["enrollment"], r["assignment"]) == key), None)
        if existing is None: self.records.append(record)
        else: self.records[existing] = record
        self.save_data(); self.refresh(); self.status_label.config(text=f"Saved {len(self.records)} record(s).")

    def refresh(self, status="All"):
        for item in self.tree.get_children(): self.tree.delete(item)
        for record in self.records:
            if status == "All" or record["status"] == status:
                self.tree.insert("", "end", values=[record.get(k,"") for k in FIELDS])
        self.status_label.config(text=f"Showing {status.lower()} records. Total stored: {len(self.records)}")

    def select_record(self, _event=None):
        selection = self.tree.selection()
        if not selection: return
        values = self.tree.item(selection[0], "values")
        for key, value in zip(FIELDS, values): self.vars[key].set(value)

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path: return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS); writer.writeheader(); writer.writerows(self.records)
        messagebox.showinfo("Export complete", f"Exported {len(self.records)} records to {path}")

if __name__ == "__main__":
    root = tk.Tk(); AssignmentTracker(root); root.mainloop()
