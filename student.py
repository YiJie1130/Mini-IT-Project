import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pybase64


# create treeview (call this function once)
def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 4)))
    tree.column("#0", width=0, stretch=tk.NO, anchor='c', minwidth=0)
    tree.column("#1", width=120, stretch=tk.NO, anchor='c', minwidth=100)
    tree.column("#2", width=200, stretch=tk.NO, anchor='c', minwidth=200)
    tree.column("#3", width=50, stretch=tk.NO, anchor='c', minwidth=50)
    tree.heading('#0', text="", anchor='c')
    tree.heading('#1', text="Name", anchor='c')
    tree.heading('#2', text="Student ID", anchor='c')
    tree.heading('#3', text="Faculty", anchor='c')
    tree['height'] = 10


# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT student_name, student_id, faculty FROM student_infos")
    for row in cursor:
        tree.insert(
            "",
            'end',
            values=(row[0], row[1], row[2])
        )
    tree.place(x=590, y=100)


# Parse and store data into database and treeview upon clcicking of the add button
def add_student():
    student_id = id_entry.get()
    name = str(name_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    faculty = str(combo.get())

    connection = sqlite3.connect("student_info.db")
    cursor = connection.cursor()
    find_id = 'SELECT * FROM student_infos WHERE student_id = ?'
    cursor.execute(find_id,[(student_id)])
    find_id = cursor.fetchall()
    if find_id:
        messagebox.showerror("Failed",'Student ID Already Exist!')
        id_entry.delete(0,tk.END)
        return
    
    elif len(student_id) != 10:
        messagebox.showerror("Failed",'Please Enter 10 Character For Your Student ID!')
        id_entry.delete(0,tk.END)
        return

    elif student_id == "" or name == "" or \
            passw == "" or conf_passw == "" :
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    elif passw != conf_passw:
        messagebox.showerror("Passwords Mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return
    
    hash = passw.encode("ascii")
    hash = pybase64.b64encode(hash)
    hash = hash.decode("ascii")
    conn.execute("INSERT INTO student_infos VALUES (:student_name, :student_id, :password, :faculty)",
                {
                    'student_name': name,
                    "student_id": student_id,
                    "password": hash,
                    "faculty" : faculty
                })
    conn.commit()
    update_treeview()

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)

# update a row in the database
def update_student():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    combo.delete(0, tk.END)
    
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one student at a time to update!")
            return

        select = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM student_infos WHERE student_name = '{select}'")

        cursor = list(cursor)
        hashed = cursor[0][2]
        hashed = hashed.encode("ascii")
        hashed = pybase64.b64decode(hashed)
        hashed = hashed.decode("ascii")
        id_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, hashed)
        conf_passw_entry.insert(0, hashed)
        combo.insert(0,cursor[0][3])

        conn.execute(f"DELETE FROM student_infos WHERE student_id = '{cursor[0][1]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return


# remove selected data from databse and treeview
def remove_student():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return
    for x in tree.selection():
        c = conn.cursor()
        c.execute(f"DELETE from student_infos WHERE student_name='{tree.item(x)['values'][0]}'")
        conn.commit()
        tree.delete(x)
        update_treeview()


# toggles between show/hide password
def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()

def edit_student():
        # main
        # connecting database
        global conn
        conn = sqlite3.connect('student_info.db')

        # # creating Table in the database
        # conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
        # (SID CHAR(10) NOT NULL PRIMARY KEY,\
        # PASSW CHAR(50) NOT NULL,\
        # NAME CHAR(50) NOT NULL,\
        # ROLL INTEGER NOT NULL,\
        # SECTION CHAR(5) NOT NULL)')

        # TKinter Window
        adminmenu_student = tk.Tk()
        adminmenu_student.geometry('1000x470')
        adminmenu_student.title('Add/Update/Delete Students')
        adminmenu_student.iconbitmap('admin.ico')

        # Label1
        tk.Label(adminmenu_student,text='List of Students',font=('Consolas', 20, 'bold')).place(x=620, y=60)

        # Label2
        tk.Label(adminmenu_student,text='Add/Update/Delete Student',font=('Consolas', 20, 'bold')).place(x=110, y=50)

        # Label3
        tk.Label(adminmenu_student,text='Add information in the following prompt!',font=('Consolas', 10, 'italic')).place(x=110, y=85)

        # Label4
        tk.Label(adminmenu_student,text='Student ID:',font=('Consolas', 12)).place(x=100, y=130)

        # Entry1
        global id_entry
        id_entry = tk.Entry(adminmenu_student,font=('Consolas', 12),width=20)
        id_entry.place(x=260, y=130)

        # Label5
        tk.Label(adminmenu_student,text='Student Name:',font=('Consolas', 12)).place(x=100, y=170)

        # Entry2
        global name_entry
        name_entry = tk.Entry(adminmenu_student,font=('Consolas', 12),width=20)
        name_entry.place(x=260, y=170)

        # Label6
        tk.Label(adminmenu_student,text='Password:',font=('Consolas', 12)).place(x=100, y=210)

        # Entry3
        global passw_entry
        passw_entry = tk.Entry(adminmenu_student,font=('Consolas', 12),width=20,show="●")
        passw_entry.place(x=260, y=210)

        global B1_show
        B1_show = tk.Button(adminmenu_student,text='○',font=('Consolas', 9, 'bold'),command=show_passw)
        B1_show.place(x=460, y=210)

        # Label7
        tk.Label(adminmenu_student,text='Confirm Password:',font=('Consolas', 12)).place(x=100, y=250)

        # Entry4
        global conf_passw_entry
        conf_passw_entry = tk.Entry(adminmenu_student,font=('Consolas', 12),width=20,show="●")
        conf_passw_entry.place(x=260, y=250)

        # Label8
        tk.Label(adminmenu_student,text='Faculty:',font=('Consolas', 12)).place(x=100, y=290)

        # combobox
        conn = sqlite3.connect('student_info.db')
        cursor = conn.execute("SELECT DISTINCT FID FROM FACULTY")
        faculty = [row[0] for row in cursor]
        global combo
        combo = ttk.Combobox(adminmenu_student,values=faculty)
        combo.place(x=260,y=295)
        combo.current(0)

        # Button1
        B1 = tk.Button(adminmenu_student,text='Add Student',font=('Consolas', 12),command=add_student)
        B1.place(x=150, y=400)

        # Button2
        B2 = tk.Button(adminmenu_student,text='Update Student',font=('Consolas', 12),command=update_student)
        B2.place(x=410, y=400)

        # Treeview1
        global tree
        tree = ttk.Treeview(adminmenu_student)
        create_treeview()
        update_treeview()

        # Button3
        B3 = tk.Button(adminmenu_student,text='Delete Student',font=('Consolas', 12),command=remove_student)
        B3.place(x=670, y=400)

        # looping Tkiniter window
        adminmenu_student.mainloop()
        conn.close()  # close database after all operations