import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import pandas as pd


# ------------ MAIN APP ------------
class EmployeeManagerApp:
    def __init__(self, root, conn, cursor):
        self.root = root
        self.conn = conn
        self.cursor = cursor
        self.root.title("Employee Manager (MySQL)")
        self.root.geometry("700x500")

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        form_frame = tk.Frame(self.root, padx=10, pady=10)
        form_frame.pack(fill=tk.X)

        tk.Label(form_frame, text="Name").grid(row=0, column=0)
        self.name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(form_frame, text="Department").grid(row=0, column=2)
        self.dept_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.dept_var).grid(row=0, column=3)

        tk.Label(form_frame, text="Salary").grid(row=0, column=4)
        self.salary_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.salary_var).grid(row=0, column=5)

        tk.Button(form_frame, text="Add", command=self.add_employee).grid(row=1, column=1, pady=5)
        tk.Button(form_frame, text="Update", command=self.update_employee).grid(row=1, column=2)
        tk.Button(form_frame, text="Delete", command=self.delete_employee).grid(row=1, column=3)
        tk.Button(form_frame, text="Clear", command=self.clear_fields).grid(row=1, column=4)

        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10)
        tk.Label(search_frame, text="Search by Name:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.populate_table())

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Dept", "Salary"), show="headings")
        for col in ("ID", "Name", "Dept", "Salary"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        export_frame = tk.Frame(self.root)
        export_frame.pack(pady=5)
        tk.Button(export_frame, text="Export to CSV", command=self.export_to_csv).pack()

    def execute_db(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def add_employee(self):
        if not self.name_var.get() or not self.dept_var.get() or not self.salary_var.get():
            messagebox.showerror("Input Error", "All fields are required")
            return
        try:
            salary = float(self.salary_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Salary must be a number")
            return
        self.execute_db("INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)",
                        (self.name_var.get(), self.dept_var.get(), salary))
        self.populate_table()
        self.clear_fields()

    def update_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select a record to update")
            return
        emp_id = self.tree.item(selected[0])['values'][0]
        try:
            salary = float(self.salary_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Salary must be a number")
            return
        self.execute_db("UPDATE employees SET name=%s, department=%s, salary=%s WHERE id=%s",
                        (self.name_var.get(), self.dept_var.get(), salary, emp_id))
        self.populate_table()
        self.clear_fields()

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select a record to delete")
            return
        emp_id = self.tree.item(selected[0])['values'][0]
        self.execute_db("DELETE FROM employees WHERE id=%s", (emp_id,))
        self.populate_table()
        self.clear_fields()

    def clear_fields(self):
        self.name_var.set("")
        self.dept_var.set("")
        self.salary_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def on_row_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name_var.set(values[1])
            self.dept_var.set(values[2])
            self.salary_var.set(values[3])

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        keyword = self.search_var.get()
        if keyword:
            self.cursor.execute("SELECT * FROM employees WHERE name LIKE %s", ('%' + keyword + '%',))
        else:
            self.cursor.execute("SELECT * FROM employees")
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def export_to_csv(self):
        self.cursor.execute("SELECT * FROM employees")
        data = self.cursor.fetchall()
        df = pd.DataFrame(data, columns=["ID", "Name", "Department", "Salary"])
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            df.to_csv(file, index=False)
            messagebox.showinfo("Exported", f"Data exported to {file}")


# ------------ LOGIN WINDOW ------------
class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login to MySQL")
        master.geometry("300x250")

        # Host input
        tk.Label(master, text="Host:").pack()
        self.host_var = tk.StringVar(value="localhost")
        tk.Entry(master, textvariable=self.host_var).pack()

        # Username input
        tk.Label(master, text="Username:").pack()
        self.user_var = tk.StringVar()
        tk.Entry(master, textvariable=self.user_var).pack()

        # Password input
        tk.Label(master, text="Password:").pack()
        self.pass_var = tk.StringVar()
        tk.Entry(master, show="*", textvariable=self.pass_var).pack()

        # Database name input
        tk.Label(master, text="Database Name:").pack()
        self.db_var = tk.StringVar(value="employee_db")
        tk.Entry(master, textvariable=self.db_var).pack()

        # Connect button
        tk.Button(master, text="Connect", command=self.try_connect).pack(pady=10)

    def try_connect(self):
        host = self.host_var.get()
        user = self.user_var.get()
        password = self.pass_var.get()
        db_name = self.db_var.get()

        try:
            # Step 1: connect without db to create one
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            conn.commit()
            conn.close()

            # Step 2: reconnect with new db
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    department VARCHAR(100),
                    salary DECIMAL(10,2)
                )
            """)

            # Step 3: launch main GUI
            self.master.destroy()
            root = tk.Tk()
            app = EmployeeManagerApp(root, conn, cursor)
            root.mainloop()

        except mysql.connector.Error as err:
            messagebox.showerror("Connection Failed", f"MySQL Error:\n{err}")



# ------------ RUN APP ------------
if __name__ == "__main__":
    login = tk.Tk()
    LoginWindow(login)
    login.mainloop()
