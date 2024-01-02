import tkinter
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox
from time import strftime
import logging
from dateutil.parser import parse

logging.basicConfig(filename="app.log", filemode="a", level=logging.DEBUG, format='%(asctime)s - %(message)s')


class StudentW:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Student Window")
        self.window.geometry('500x500')

        self.Tabs = ttk.Notebook(self.window)

        self.Reserve = ttk.Frame(self.Tabs)
        self.View = ttk.Frame(self.Tabs)
        self.connection = sqlite3.connect("KSU.db")
        self.Tabs.add(self.Reserve, text="Reserve a Classroom")
        self.Tabs.add(self.View, text="View my Reservations")

        self.Tabs.pack(expand=1, fill="both")

        self.conn = sqlite3.connect("KSU.db")
        self.all_std_id = self.conn.execute("SELECT student_id from Users_id")
        all_id = []
        for row in self.all_std_id:
            s = row[0]
            all_id.append(s)
        self.std_id = all_id[-1]

        self.label_myReservation = tkinter.Label(self.View, text="My Reservations", font=('Helvetica bold', 26))
        self.label_myReservation.pack(pady=30)

        self.buttonBack1 = tk.Button(self.View, text='Show classes', command=self.show_class)
        self.buttonBack1.place(relx=0.35, rely=0.7)

        self.buttonBack2 = tk.Button(self.View, text='Logout', command=self.logout)
        self.buttonBack2.place(relx=0.55, rely=0.7)

        self.label_class_room = tkinter.Label(self.Reserve, text="Available classRoom", font=('Helvetica bold', 26))
        self.label_class_room.pack(pady=30)

        self.conn.execute(''' CREATE TABLE IF NOT EXISTS Reserve_Classroom
        ( id int ,
          Number Text NOT NULL,
          Location Text NOT NULL,
          Capacity INT NOT NULL,
          Sdate Text NOT NULL,
          Stime Text NOT NULL,
          Edate Text Not NULL,
          Etime Text Not NULL);
        ''')
        class_number = []
        class_location = []
        class_Capacity = []

        try:
            self.cursor = self.conn.execute("SELECT * from ClassRoom")
            for row in self.cursor:
                class_number.append(row[0])
                class_location.append(row[1])
                class_Capacity.append(row[2])
        except:
            tkinter.messagebox.showerror("Error", "There is no classRoom you can Reserve ")

        self.label_combo_Classroom = tkinter.Label(self.Reserve, text="Classroom Numbers:")
        self.label_combo_Classroom.place(relx=0.2, rely=0.25)
        self.combo_Classroom_number = ttk.Combobox(self.Reserve)
        self.combo_Classroom_number.place(relx=0.44, rely=0.25)
        self.combo_Classroom_number['values'] = class_number

        self.label_combo_locations = tkinter.Label(self.Reserve, text="Enter Locations:")
        self.label_combo_locations.place(relx=0.25, rely=0.35)
        self.combo_locations = ttk.Combobox(self.Reserve)
        self.combo_locations.place(relx=0.44, rely=0.35)
        self.combo_locations['values'] = class_location

        self.label_combo_capacity = tkinter.Label(self.Reserve, text="Enter Capacity:")
        self.label_combo_capacity.place(relx=0.25, rely=0.45)
        self.combo_capacity = ttk.Combobox(self.Reserve)
        self.combo_capacity.place(relx=0.44, rely=0.45)

        self.combo_capacity['values'] = class_Capacity

        # start date

        self.sel = tk.StringVar()
        self.start_cal_label = tkinter.Label(self.Reserve, text="Start date:")
        self.start_cal = DateEntry(self.Reserve, selectmode='day', textvariable=self.sel)
        self.start_cal.place(relx=0.20, rely=0.6)
        self.start_cal_label.place(relx=0.07, rely=0.6)

        # Start time
        s_hr = tk.Label(self.Reserve, text='Hour:')
        self.var1 = tkinter.StringVar()
        s_hr.place(relx=0.1, rely=0.69)

        Shr = tk.Scale(self.Reserve, from_=0, to=23,
                       orient='horizontal', length=100, variable=self.var1)
        Shr.place(relx=0.19, rely=0.65)

        self.var2 = tkinter.StringVar()
        s_mn = tk.Label(self.Reserve, text='Mintue:')
        s_mn.place(relx=0.08, rely=0.77)

        Smn = tk.Scale(self.Reserve, from_=0, to=59,
                       orient='horizontal', length=100, variable=self.var2)
        Smn.place(relx=0.19, rely=0.73)

        # End date

        self.sel1 = tk.StringVar()
        self.End_cal_label = tkinter.Label(self.Reserve, text="End date:")
        self.End_cal = DateEntry(self.Reserve, selectmode='day', textvariable=self.sel1)
        self.End_cal.place(relx=0.7, rely=0.6)
        self.End_cal_label.place(relx=0.58, rely=0.6)

        # End time
        e_hr = tk.Label(self.Reserve, text='Hour:')
        self.var3 = tkinter.StringVar()
        e_hr.place(relx=0.61, rely=0.69)
        Ehr = tk.Scale(self.Reserve, from_=0, to=23,
                       orient='horizontal', length=100, variable=self.var3)
        Ehr.place(relx=0.69, rely=0.65)

        self.var4 = tkinter.StringVar()
        e_mn = tk.Label(self.Reserve, text='Mintue:')
        e_mn.place(relx=0.59, rely=0.77)

        Emn = tk.Scale(self.Reserve, from_=0, to=59,
                       orient='horizontal', length=100, variable=self.var4)
        Emn.place(relx=0.69, rely=0.73)

        def my_upd(*args):
            print(self.sel.get())

        self.sel.trace('w', my_upd)

        def my_upd1(*args):
            print(self.sel1.get())

        self.sel1.trace('w', my_upd1)
        # self.buttonBack = tk.Button(self.window, text='Logout', command=self.logout)
        # self.buttonBack.pack()
        self.buttonBack1 = tk.Button(self.Reserve, text='Logout', command=self.logout)
        self.buttonBack1.place(relx=0.55, rely=0.9)

        self.buttonBack2 = tk.Button(self.Reserve, text='Reserve', command=self.reserve)
        self.buttonBack2.place(relx=0.4, rely=0.9)

        self.window.mainloop()

    def show_class(self):
        ws = tkinter.Tk()
        ws.title('TreeView')
        ws.geometry('400x300')
        conn = sqlite3.connect("KSU.db")
        tv = ttk.Treeview(ws, columns=(1, 2, 3, 4, 5, 6, 7, 8), show='headings', height=8)
        tv.heading(1, text="ID")
        tv.heading(2, text="Number")
        tv.heading(3, text="Location")
        tv.heading(4, text="Capacity")
        tv.heading(5, text="Sdate")
        tv.heading(6, text="Stime")
        tv.heading(7, text="Edate")
        tv.heading(8, text="Etime")

        cursor = conn.execute(
            "SELECT id,Number,Location,Capacity ,Sdate,Stime ,Edate,Etime from Reserve_Classroom WHERE id = ?",
            (self.std_id,))
        count = 0
        for row in cursor:
            tv.insert(parent='', index=count, text='',
                      values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            count += 1
        conn.close()
        tv.pack()
        ws.mainloop()

    def reserve(self):
        self.class_number = self.combo_Classroom_number.get()
        self.location = self.combo_locations.get()
        self.capacity = self.combo_capacity.get()
        self.Sdate = self.start_cal.get()
        self.Edate = self.End_cal.get()
        self.Sdate = parse(self.Sdate)
        self.Edate = parse(self.Edate)
        self.f_hr = self.var1.get()
        self.f_mn = self.var2.get()
        self.e_hr = self.var3.get()
        self.e_mn = self.var4.get()

        if int(self.f_mn) < 10:
            c = "0" + self.f_mn
            self.f_mn = c
        if int(self.e_mn) < 10:
            c = "0" + self.e_mn
            self.e_mn = c
        self.Stime = self.f_hr + ":" + self.f_mn
        self.Etime = self.e_hr + ":" + self.e_mn

        if self.class_number == '':
            tkinter.messagebox.showerror(self.window, "Please shows a classRoom number")
        elif self.location == '':
            tkinter.messagebox.showerror(self.window, "Please shows a location")
        elif self.capacity == '':
            tkinter.messagebox.showerror(self.window, "Please shows a capacity")
        else:
            self.empty = self.conn.execute('''select * from Reserve_Classroom''')

            if self.empty.fetchone() == None:
                self.conn.execute("""INSERT INTO Reserve_Classroom( id,Number,Location,Capacity ,Sdate,Stime ,Edate,Etime)
                        VALUES (?,?,?,?,?,?,?,?)""", (
                self.std_id, self.class_number, self.location, self.capacity, self.Sdate, self.Stime, self.Edate,
                self.Etime))
                tkinter.messagebox.showinfo("Success", "Reserve class done")
                self.conn.commit()
                logging.info(
                    f"Student ID is {self.std_id} Classroom number is {self.class_number} and Location is {self.location} and Start date is {self.Sdate} and Start time is {self.Stime} and End date is {self.Edate} and End time is {self.Etime} ")
            else:
                add_all_class = []
                cursor = self.conn.execute("SELECT Number,Location ,Sdate,Edate ,Stime,Etime from Reserve_Classroom")
                for row in cursor:
                    if row[0] == self.class_number and row[1] == self.location:
                        str = [row[2], row[3], row[4], row[5]]
                        add_all_class.append(str)
                if len(add_all_class) == 0:
                    self.conn.execute("""INSERT INTO Reserve_Classroom(id,Number,Location,Capacity ,Sdate,Stime ,Edate,Etime)
                                     VALUES (?,?,?,?,?,?,?,?)""", (
                    self.std_id, self.class_number, self.location, self.capacity, self.Sdate, self.Stime, self.Edate,
                    self.Etime))
                    tkinter.messagebox.showinfo("Success", "Reserve class done")
                    self.conn.commit()
                    logging.info(
                        f" Student ID is {self.std_id} Classroom number is {self.class_number} and Location is {self.location} and Start date is {self.Sdate} and Start time is {self.Stime} and End date is {self.Edate} and End time is {self.Etime} ")

                else:
                    for values in add_all_class:
                        self.count = 0
                        sdate = values[0]
                        edate = values[1]
                        sdate = parse(sdate)
                        edate = parse(edate)
                        stime = values[2]
                        etime = values[3]

                        def time_in_range(start, end, x):
                            """Return true if x is in the range [start, end]"""
                            if start <= end:
                                return start <= x <= end
                            else:
                                return start <= x or x <= end

                        if self.Sdate > sdate and self.Sdate < edate:
                            self.count = 1
                        if self.Edate > sdate and self.Edate < edate:
                            self.count = 1
                        if self.count == 1:
                            tkinter.messagebox.showerror(self.window,
                                                         "Sorry classroom is occupied during the given time & date1")
                            break
                        else:
                            if self.Sdate >= sdate and self.Sdate <= edate:
                                self.bool = time_in_range(stime, etime, self.Stime)
                                if self.bool:
                                    self.count = 1
                            if self.Edate >= sdate and self.Edate <= edate:
                                self.bool = time_in_range(stime, etime, self.Etime)
                                if self.bool:
                                    self.count = 1
                            if self.count == 1:
                                tkinter.messagebox.showerror(self.window,
                                                             "Sorry classroom is occupied during the given time & date2")
                                break
                            else:
                                if self.count == 0:
                                    if sdate >= self.Sdate and sdate <= self.Edate:
                                        self.bool = time_in_range(self.Stime, self.Etime, stime)
                                        if self.bool:
                                            self.count = 1
                                    if edate >= self.Sdate and edate <= self.Edate:
                                        self.bool = time_in_range(self.Stime, self.Etime, etime)
                                        if self.bool:
                                            self.count = 1
                                if self.count == 1:
                                    tkinter.messagebox.showerror(self.window,
                                                                 "Sorry classroom is occupied during the given time & date3")
                                    break
                                # if sdate > self.Sdate or sdate < self.Edate:
                                #     logging.info("is enter fdate2")
                                #     self.count = 1
                                # if self.Sdate < edate or self.Edate > edate:
                                #     logging.info("is enter edate2")
                                #     self.count = 1
                                # if self.count == 1:
                                #     tkinter.messagebox.showerror(self.window,"Sorry classroom is occupied during the given time & date")
                                #     break
                    if self.count == 0:
                        self.conn.execute("""INSERT INTO Reserve_Classroom(id,Number,Location,Capacity ,Sdate,Stime ,Edate,Etime)
                VALUES (?,?,?,?,?,?,?,?)""", (
                        self.std_id, self.class_number, self.location, self.capacity, self.Sdate, self.Stime,
                        self.Edate, self.Etime))
                        tkinter.messagebox.showinfo("Success", "Reserve class done")
                        logging.info(
                            f"Student ID {self.std_id} Classroom number is {self.class_number} and Location is {self.location} and Start date is {self.Sdate} and Start time is {self.Stime} and End date is {self.Edate} and End time is {self.Etime} ")
                        self.conn.commit()

    def logout(self):
        self.window.update()
        self.window.destroy()
        import SignupW
        SignupW.SignupW()


StudentW()
# conn = sqlite3.connect("KSU.db")
# conn.execute("""DELETE FROM Reserve_Classroom""")
# conn.commit()
