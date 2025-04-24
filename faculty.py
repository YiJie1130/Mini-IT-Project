import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# create treeview (call this function once)
def create_treeview():
    faculty_tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 3)))
    faculty_tree.column("#0", width=0, stretch=tk.NO, anchor='c')
    faculty_tree.column("#1", width=100, stretch=tk.NO, anchor='c')
    faculty_tree.column("#2", width=300, stretch=tk.NO, anchor='c')
    faculty_tree.heading('#0', text="", anchor='c')
    faculty_tree.heading('#1', text="Faculty ID", anchor='c')
    faculty_tree.heading('#2', text="Faculty Name", anchor='c')
    faculty_tree['height'] = 12


# update treeview (call this function after each update)
def update_treeview():
    for row in faculty_tree.get_children():
        faculty_tree.delete(row)
    cursor = conn.execute("SELECT FID, NAME FROM FACULTY")
    for row in cursor:
        faculty_tree.insert(
            "",
            'end',
            values=(row[0], row[1])
        )
    faculty_tree.place(x=580, y=100)


# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    fid = str(fid_entry.get()).upper()
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    email = str(email_entry.get())

    if fid == "" or passw == "" or \
            conf_passw == "" or name == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    conn.execute(f"INSERT INTO FACULTY (FID, PASSW, NAME, EMAIL)\
        VALUES ('{fid}','{passw}','{name}', '{email}')")
    conn.commit()
    update_treeview()

    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# update a row in the database
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    try:
        if len(faculty_tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one faculty at a time to update!")
            return

        q_fid = faculty_tree.item(faculty_tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM FACULTY WHERE FID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        email_entry.insert(0, cursor[0][3])


        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return


# remove selected data from databse and treeview
def remove_data():
    if len(faculty_tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return
    for i in faculty_tree.selection():
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{faculty_tree.item(i)['values'][0]}'")
        conn.commit()
        faculty_tree.delete(i)
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


# main
def edit_faculty():
    # connecting database
    global conn
    conn = sqlite3.connect('student_info.db')

    # creating Table in the database
    # conn.execute('''"CREATE TABLE IF NOT EXISTS FACULTY\
    # (FID CHAR(10) NOT NULL PRIMARY KEY,\
    # PASSW CHAR(50) NOT NULL,\
    # NAME CHAR(50) NOT NULL,\
    # EMAIL CHAR(50) NOT NULL\
    #              "''')

    # TKinter Window
    faculty_page = tk.Tk()
    faculty_page.geometry('1020x550')
    faculty_page.title('Add/Update/Delete Faculty')
    faculty_page.iconbitmap('admin.ico')

    # Label1
    tk.Label(
        faculty_page,
        text='List of Faculties',
        font=('Consolas', 20, 'bold')
    ).place(x=655, y=50)

    # Label2
    tk.Label(
        faculty_page,
        text='Add/Update/Delete Faculty',
        font=('Consolas', 20, 'bold')
    ).place(x=90, y=50)

    # Label3
    tk.Label(
        faculty_page,
        text='Add information in the following prompt!',
        font=('Consolas', 10, 'italic')
    ).place(x=100, y=85)

    # Label4
    tk.Label(
        faculty_page,
        text='Faculty ID:',
        font=('Consolas', 12)
    ).place(x=100, y=150)

    # Entry1
    global fid_entry
    fid_entry = tk.Entry(
        faculty_page,
        font=('Consolas', 12),
        width=20
    )
    fid_entry.place(x=260, y=150)

    # Label5
    tk.Label(
        faculty_page,
        text='Password:',
        font=('Consolas', 12)
    ).place(x=100, y=190)

    # Entry2
    global passw_entry
    passw_entry = tk.Entry(
        faculty_page,
        font=('Consolas', 12),
        width=20,
        show="●"
    )
    passw_entry.place(x=260, y=190)

    global B1_show
    B1_show = tk.Button(
        faculty_page,
        text='○',
        font=('Consolas', 9, 'bold'),
        command=show_passw
    )
    B1_show.place(x=460, y=190)

    # Label6
    tk.Label(
        faculty_page,
        text='Confirm Password:',
        font=('Consolas', 12)
    ).place(x=100, y=230)

    # Entry3
    global conf_passw_entry
    conf_passw_entry = tk.Entry(
        faculty_page,
        font=('Consolas', 12),
        width=20,
        show="●"
    )
    conf_passw_entry.place(x=260, y=230)

    # Label7
    tk.Label(
        faculty_page,
        text='Faculty Name:',
        font=('Consolas', 12)
    ).place(x=100, y=270)

    # Entry4
    global name_entry
    name_entry = tk.Entry(
        faculty_page,
        font=('Consolas', 12),
        width=25,
    )
    name_entry.place(x=260, y=270)

    # Label8
    tk.Label(
        faculty_page,
        text='Email:',
        font=('Consolas', 12)
    ).place(x=100, y=310)

    # Entry5
    global email_entry
    email_entry = tk.Entry(
        faculty_page,
        font=('Consolas', 12),
        width=25,
    )
    email_entry.place(x=260, y=310)

    # Button1
    B1 = tk.Button(
        faculty_page,
        text='Add Faculty',
        font=('Consolas', 12),
        command=parse_data
    )
    B1.place(x=170, y=445)

    # Button2
    B2 = tk.Button(
        faculty_page,
        text='Update Faculty',
        font=('Consolas', 12),
        command=update_data
    )
    B2.place(x=450, y=445)

    # Button3
    B3 = tk.Button(
        faculty_page,
        text='Delete Faculty',
        font=('Consolas', 12),
        command=remove_data
    )
    B3.place(x=730, y=445)

    # Treeview1
    global faculty_tree
    faculty_tree = ttk.Treeview(faculty_page)
    create_treeview()
    update_treeview()

    # looping Tkiniter window
    faculty_page.mainloop()
    conn.close()  # close database after all operations