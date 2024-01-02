import tkinter
import tkinter as tk
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect("KSU.db")
conn.execute('''CREATE TABLE IF NOT EXISTS ClassRoom ( Number TEXT not null , Location Text not null , Capacity int not null);''')
class AdminW:
   def __init__(self):
      self.window = tk.Tk()
      self.window.title("Admin")
      self.window.geometry('550x550')


      self.label_class_room = tkinter.Label(self.window, text="Enter classRoom", font=('Helvetica bold', 26))
      self.label_class_room.pack(pady=30)
      self.connection = sqlite3.connect("KSU.db")
      self.class_number_label = tkinter.Label(text=" Classroom number : ")
      self.class_location_label = tkinter.Label(text=" Classroom location : ")
      self.class_capacity_label = tkinter.Label(text=" Classroom capacity : ")
      self.class_number_label.place(relx=0.25,rely=0.30)
      self.class_location_label.place(relx=0.25,rely=0.40)
      self.class_capacity_label.place(relx=0.25,rely=0.50)

      self.class_number_entry = tkinter.Entry()
      self.class_location_entry = tkinter.Entry()
      self.class_capacity_entry = tkinter.Entry()
      self.class_number_entry.place(relx=0.50, rely=0.30)
      self.class_location_entry.place(relx=0.50, rely=0.40)
      self.class_capacity_entry.place(relx=0.50, rely=0.50)

      self.create_button = tkinter.Button(text="Create button" , command=self.saveData)
      self.logout_button = tkinter.Button(text="Logout button" , command=self.logout)
      self.backup_button = tkinter.Button(text="Backup button" , command=self.backUp_action)
      self.create_button.place(relx=0.25, rely=0.65)
      self.backup_button.place(relx=0.45, rely=0.65)
      self.logout_button.place(relx=0.65, rely=0.65)

      self.window.mainloop()


   def saveData(self):
    self.classNumber = self.class_number_entry.get()
    self.classLocation = self.class_location_entry.get()
    self.classCapacity  = self.class_capacity_entry.get()
    try:
     if self.classNumber !='':
        if self.classLocation !='' :
          if self.classCapacity.isdigit() :
            conn.execute("""INSERT INTO ClassRoom(Number,Location,Capacity)
            VALUES (?,?,?)""",(self.classNumber , self.classLocation,self.classCapacity))
            tkinter.messagebox.showinfo("Success", "class is available to student")
            conn.commit()
          else:
            tkinter.messagebox.showerror("Error", "Capacity should be number")

     else:
      tkinter.messagebox.showerror(self.window,"One or more of the field is empty!")
    except:
      tkinter.messagebox.showerror(self.window, "There is an Error")


   def logout(self):
      self.window.update()
      self.window.destroy()
      import SignupW
      SignupW.SignupW()

   def backUp_action(self):
     try:
       self.backup_object_file = open("data_backup.csv", "a")
       self.connection = sqlite3.connect("KSU.db")
       self.cur = self.connection.execute("SELECT * FROM ksu_users")
       self.res = self.connection.execute("select * from Reserve_Classroom")
       self.en = self.connection.execute("select * from ClassRoom")
       for data in self.cur:
           self.backup_object_file.write(str(data[0]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[1]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[2]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[3]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[4]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[5]))
           self.backup_object_file.write("\n")
       for data in self.res:
           self.backup_object_file.write(str(data[0]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[1]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[2]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[3]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[4]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[5]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[6]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[7]))
           self.backup_object_file.write("\n")
       for data in self.en:
           self.backup_object_file.write(str(data[0]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[1]))
           self.backup_object_file.write(",")
           self.backup_object_file.write(str(data[2]))
           self.backup_object_file.write("\n")

       tkinter.messagebox.showinfo("Backup", "Backup is successfully done.")
       self.connection.close()
       self.backup_object_file.close()

     except:
         tkinter.messagebox.showerror("Error" , "There is no Table")
AdminW()
# conn.execute("""DELETE FROM ClassRoom""")
# conn.commit()
