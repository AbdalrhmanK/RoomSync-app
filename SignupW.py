import hashlib
import tkinter as tk
import sqlite3
from tkinter import messagebox
class SignupW:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sign Up")
        self.window.geometry("500x500")
        self.connection = sqlite3.connect("KSU.db")
        self.sign_up_label = tk.Label( self.window, text="Sign up" , font=('Helvetica bold', 26))
        self.sign_up_label.pack(pady=30)

        self.first_name_label = tk.Label(self.window, text="First Name:")
        self.first_name_label.place(relx=0.24 , rely=0.25)
        self.first_name_entry = tk.Entry(self.window)
        self.first_name_entry.place(relx=0.4 , rely=0.25)

        self.last_name_label = tk.Label(self.window, text="Last Name:")
        self.last_name_label.place( relx=0.24, rely=0.33)
        self.last_name_entry = tk.Entry(self.window)
        self.last_name_entry.place( relx=0.4, rely=0.33)

        self.student_id_label = tk.Label(self.window, text="Student ID:")
        self.student_id_label.place(relx=0.24,rely=0.41)
        self.student_id_entry = tk.Entry(self.window)
        self.student_id_entry.place(relx=0.4,rely=0.41)
        #
        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.place( relx=0.24,rely=0.49)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.place( relx=0.4,rely=0.49)
        #
        self.email_label = tk.Label(self.window, text="Email:")
        self.email_label.place( relx=0.28,rely=0.57)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.place( relx=0.4,rely=0.57)
        #
        self.phone_label = tk.Label(self.window, text="Phone:")
        self.phone_label.place( relx=0.28,rely=0.65)
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.place( relx=0.4,rely=0.65)
        #
        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit)
        self.submit_button.place( relx=0.4, rely=0.75)

        self.login_button = tk.Button(self.window, text="Login", command=self.go_Login)
        self.login_button.place( relx=0.55,rely=0.75)



    def submit(self):
        if not all([self.first_name_entry, self.last_name_entry, self.student_id_entry, self.password_entry, self.email_entry, self.phone_entry]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if not all([first_name, last_name, student_id, password, email, phone]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if len(student_id) != 10:
            tk.messagebox.showerror("Error", "ID must be 10 digits.")
            return
        if not student_id.isdigit():
            tk.messagebox.showerror("Error", "ID must contain only digits.")
            return
        if not phone.startswith("05") or len(phone) != 10:
            tk.messagebox.showerror("Error", "Phone number must be\n05########")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return
        if not first_name.isalpha() :
            messagebox.showerror("Error", "Name should be without number")
            return
        if not last_name.isalpha():
            messagebox.showerror("Error", "Name should be without number")
            return
            # Check if email is in the correct format
        if "@ksu.edu.sa" not in email:
            messagebox.showerror("Error", "Email must be in the format XXXXXXXX@ksu.edu.sa.")
            return
        is_registered = False
        if is_registered:
            messagebox.showerror("Error", "Student is already registered.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        connection = sqlite3.connect("KSU.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ksu_users (first_name text, last_name text, student_id text PRIMARY KEY, password text, email text, phone text)")
        # Check if student is already registered
        cursor.execute("SELECT * FROM ksu_users WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        if result:
            messagebox.showerror("Error", "ksu_users is already registered.")
            return
        cursor.execute("INSERT INTO ksu_users VALUES (?,?,?,?,?,?)", (first_name, last_name, student_id, hashed_password, email, phone))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Sign up successful!")

    def go_Login(self):
        self.window.withdraw()  # Withdraw the window instead of destroying it
        import LoginW
        login_window = LoginW.LoginW()
        login_window.window.mainloop()  # Run the main loop directly

    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    SignupW().run()
# conn = sqlite3.connect("KSU.db")
# conn.execute("""DELETE FROM ksu_users""")
# conn.commit()


