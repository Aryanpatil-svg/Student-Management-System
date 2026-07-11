import tkinter as tk
from tkinter import messagebox, ttk
from manager import StudentManager
from student import Student

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Premium Student Dashboard")
        self.root.geometry("920x550")
        self.root.configure(bg="#11111b") # Cyberpunk / Dark Theme

        self.manager = StudentManager()
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # --- Top Header & Stats Bar ---
        self.header_frame = tk.Frame(self.root, bg="#1e1e2e", height=60)
        self.header_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        title_lbl = tk.Label(self.header_frame, text="🎓 STUDENT MANAGEMENT SYSTEM", bg="#1e1e2e", fg="#cba6f7", font=("Arial", 14, "bold"))
        title_lbl.pack(side="left", padx=15, pady=15)

        self.stats_lbl = tk.Label(self.header_frame, text="📊 Total Students: 0", bg="#313244", fg="#a6e3a1", font=("Arial", 11, "bold"), padx=15, pady=5)
        self.stats_lbl.pack(side="right", padx=15, pady=12)

        # --- Middle Search Bar ---
        search_frame = tk.Frame(self.root, bg="#11111b")
        search_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(search_frame, text="🔍 Search:", bg="#11111b", fg="#cdd6f4", font=("Arial", 11)).pack(side="left", padx=(5, 5))
        self.ent_search = tk.Entry(search_frame, font=("Arial", 11), bg="#1e1e2e", fg="white", insertbackground="white", bd=1, relief="solid")
        self.ent_search.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
        self.ent_search.bind("<KeyRelease>", self.handle_search)

        # --- Main Layout (Left: Form, Right: Table View) ---
        main_content = tk.Frame(self.root, bg="#11111b")
        main_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Left Panel (Inputs Frame)
        form_frame = tk.LabelFrame(main_content, text=" Enter Details ", bg="#1e1e2e", fg="#cba6f7", font=("Arial", 10, "bold"), padx=15, pady=10, width=280)
        form_frame.pack(side="left", fill="y")
        form_frame.pack_propagate(False)

        tk.Label(form_frame, text="Student ID (Unique):", bg="#1e1e2e", fg="#bac2de", font=("Arial", 10)).pack(anchor="w", pady=(5,2))
        self.ent_id = tk.Entry(form_frame, font=("Arial", 11), bg="#313244", fg="white", insertbackground="white", bd=0)
        self.ent_id.pack(fill="x", pady=5, ipady=4)

        tk.Label(form_frame, text="Full Name:", bg="#1e1e2e", fg="#bac2de", font=("Arial", 10)).pack(anchor="w", pady=(10,2))
        self.ent_name = tk.Entry(form_frame, font=("Arial", 11), bg="#313244", fg="white", insertbackground="white", bd=0)
        self.ent_name.pack(fill="x", pady=5, ipady=4)

        tk.Label(form_frame, text="Grade:", bg="#1e1e2e", fg="#bac2de", font=("Arial", 10)).pack(anchor="w", pady=(10,2))
        self.ent_grade = tk.Entry(form_frame, font=("Arial", 11), bg="#313244", fg="white", insertbackground="white", bd=0)
        self.ent_grade.pack(fill="x", pady=(5, 20), ipady=4)

        # Action Buttons
        tk.Button(form_frame, text="➕ Add New Student", bg="#a6e3a1", fg="#11111b", font=("Arial", 10, "bold"), bd=0, cursor="hand2", command=self.handle_add).pack(fill="x", pady=5, ipady=5)
        tk.Button(form_frame, text="✏️ Update Details", bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), bd=0, cursor="hand2", command=self.handle_update).pack(fill="x", pady=5, ipady=5)
        tk.Button(form_frame, text="❌ Delete Record", bg="#f38ba8", fg="#11111b", font=("Arial", 10, "bold"), bd=0, cursor="hand2", command=self.handle_delete).pack(fill="x", pady=5, ipady=5)
        
        tk.Frame(form_frame, height=2, bg="#313244").pack(fill="x", pady=10)
        
        tk.Button(form_frame, text="📋 View All / Refresh", bg="#45475a", fg="white", font=("Arial", 10), bd=0, cursor="hand2", command=self.reset_view).pack(fill="x", pady=4, ipady=4)
        tk.Button(form_frame, text="🧹 Clear Form", bg="#45475a", fg="white", font=("Arial", 10), bd=0, cursor="hand2", command=self.clear_form).pack(fill="x", pady=4, ipady=4)

        # Right Panel (Spreadsheet Table View)
        table_frame = tk.Frame(main_content, bg="#1e1e2e", padx=5, pady=5)
        table_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Styling Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e2e", foreground="#cdd6f4", fieldbackground="#1e1e2e", rowheight=32, font=("Arial", 10))
        style.configure("Treeview.Heading", background="#313244", foreground="#cdd6f4", font=("Arial", 10, "bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", "#b4befe")], foreground=[("selected", "#11111b")])

        cols = ("ID", "Name", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Treeview")
        self.tree.heading("ID", text="🆔 Student ID")
        self.tree.heading("Name", text="👤 Full Name")
        self.tree.heading("Grade", text="🏅 Grade")
        
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Name", width=260, anchor=tk.W)
        self.tree.column("Grade", width=90, anchor=tk.CENTER)
        
        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.bind("<<TreeviewSelect>>", self.handle_row_select)

    def update_stats(self):
        count = self.manager.get_total_count()
        self.stats_lbl.config(text=f"📊 Total Students: {count}")

    def refresh_table(self, student_list=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_list = student_list if student_list is not None else self.manager.get_all_students()
        for student in display_list:
            self.tree.insert("", tk.END, values=(student.id, student.name, student.grade))
        self.update_stats()

    def handle_add(self):
        try:
            self.manager.add_student(self.ent_id.get(), self.ent_name.get(), self.ent_grade.get())
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", "Student record added successfully!")
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def handle_update(self):
        try:
            self.manager.update_student(self.ent_id.get(), self.ent_name.get(), self.ent_grade.get())
            self.refresh_table()
            messagebox.showinfo("Success", "Student details updated successfully!")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))

    def handle_delete(self):
        s_id = self.ent_id.get()
        if not s_id:
            messagebox.showwarning("Warning", "Please select a student from the list first!")
            return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID: {s_id}?"):
            try:
                self.manager.delete_student(s_id)
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Success", "Student record removed successfully.")
            except KeyError as e:
                messagebox.showerror("Error", str(e))

    def handle_search(self, event):
        query = self.ent_search.get()
        results = self.manager.search_student(query)
        self.refresh_table(results)

    def reset_view(self):
        self.ent_search.delete(0, tk.END)
        self.refresh_table()

    def handle_row_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected[0], "values")
        
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, vals[0])
        
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, vals[1])
        
        self.ent_grade.delete(0, tk.END)
        self.ent_grade.insert(0, vals[2])

    def clear_form(self):
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_grade.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()