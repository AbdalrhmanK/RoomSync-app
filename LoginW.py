import hashlib
import tkinter
import tkinter as tk
import sqlite3
from tkinter import messagebox


class LoginW:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry('500x500')

        self.connection = sqlite3.connect("KSU.db")
        self.Login_label = tk.Label(self.window, text="Login", font=('Helvetica bold', 26))
        self.Login_label.pack(pady=30)

        self.user_id_label = tk.Label(self.window, text="User ID:")
        self.user_id_label.place(relx=0.28, rely=0.25)
        self.user_id_entry = tk.Entry(self.window)
        self.user_id_entry.place(relx=0.4, rely=0.25)

        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.place(relx=0.26, rely=0.33)
        self.password_entry = tk.Entry(self.window , show="*")
        self.password_entry.place(relx=0.4, rely=0.33)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit)
        self.submit_button.place(relx=0.4, rely=0.5)

        self.signup_button = tk.Button(self.window, text="Sign up", command=self.go_signup)
        self.signup_button.place(relx=0.55, rely=0.5)

    def submit(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()

        if not all([user_id, password]):
            tkinter.messagebox.showerror("Error", "Please fill in both student ID and password")
            return
        if len(user_id) != 10:
            tkinter.messagebox.showerror("Error", "ID must be 10 digits.")
            return
        if not user_id.isdigit():
            tkinter.messagebox.showerror("Error", "ID must contain only digits.")
            return
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = sqlite3.connect("KSU.db")
            conn.execute("CREATE TABLE IF NOT EXISTS Users_id (student_id text)")
            cursor = conn.cursor()
            value = conn.execute("SELECT student_id , password FROM ksu_users limit 1")
            for x in value:
                if user_id == x[0] and hashed_password == x[1] :
                    self.go_admin()
                    break
            cursor.execute("""
                    SELECT * FROM ksu_users
                    WHERE student_id=? AND password=?
                """, (user_id, hashed_password))
            result = cursor.fetchone()
            if result is not None:
               conn.execute("INSERT INTO Users_id VALUES (?)", (user_id,))
               conn.commit()
               self.go_student()
            else:
                tkinter.messagebox.showwarning("Error", "Wrong user information.")
        finally:
            conn.close()

    def go_student(self):
        self.window.withdraw()
        import StudentW
        Student_window = StudentW.StudentW()
        Student_window.window.mainloop()

    def go_admin(self):
        self.window.update()
        self.window.destroy()
        import AdminW
        AdminW.AdminW()

    def go_signup(self):
        self.window.withdraw()
        import SignupW
        Signup_window = SignupW.SignupW()
        Signup_window.run()
        Signup_window.window.mainloop()  # Run the main loop directly
