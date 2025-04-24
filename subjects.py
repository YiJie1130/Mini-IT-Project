import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# create treeview (call this function once)
def create_treeview():
    tree['columns'] = ('one', 'two', 'three', 'four')
    tree.column("#0", width=0, stretch=tk.NO, anchor='c')
    tree.column("one", width=60, stretch=tk.NO, anchor='c')
    tree.column("two", width=120, stretch=tk.NO, anchor='c')
    tree.column("three", width=250, stretch=tk.NO, anchor='c')
    tree.column("four", width=60, stretch=tk.NO, anchor='c')
    tree.heading('#0', text="")
    tree.heading('one', text="Faculty")
    tree.heading('two', text="Subject Code")
    tree.heading('three', text="Name")
    tree.heading('four', text="Type")
    tree['height'] = 11

# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT FID, SUBCODE, SUBNAME, SUBTYPE FROM SUBJECTS")
    for row in cursor:
        tree.insert(
            "",
            'end',
            values=(row[0], row[1], row[2], row[3])
        )
    tree.place(x=480, y=100)


# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    faculty = str(faculty_combo.get())
    subcode = str(subcode_entry.get())
    subname = str(subname_entry.get("1.0", tk.END)).upper().rstrip()
    subtype = str(combo.get())
    if subcode == "":
        subcode = None
    if subname == "":
        subname = None

    if subcode is None or subname is None:
        messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)
        return
    
    elif faculty:
        conn.execute(f"INSERT INTO SUBJECTS (FID, SUBCODE, SUBNAME, SUBTYPE)\
            VALUES ('{faculty}','{subcode}','{subname}','{subtype}')")
        conn.commit()
        update_treeview()

        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)

    elif subtype == "Lecture":
        conn.execute(f"INSERT INTO SUBJECTS (FID, SUBCODE, SUBNAME, SUBTYPE)\
            VALUES ('{faculty}','{subcode}','{subname}','{subtype}')")
        conn.commit()
        update_treeview()

        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)

    elif subtype == "Tutorial":
        conn.execute(f"INSERT INTO SUBJECTS (FID, SUBCODE, SUBNAME, SUBTYPE)\
            VALUES ('{faculty}','{subcode}','{subname}','{subtype}')")
        conn.commit()
        update_treeview()

        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)


# update a row in the database
def update_data():
    faculty_combo.delete(0,tk.END)
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)
    combo.delete(0,tk.END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        faculty_combo.insert(0, row[0])
        subcode_entry.insert(0, row[1])
        subname_entry.insert("1.0", row[2])
        combo.insert(0, row[3])

        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[1]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return


# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][1]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()


# main
def edit_subject():
    # connecting database
    global conn
    conn = sqlite3.connect('student_info.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS\
    (SUBCODE CHAR(10) NOT NULL PRIMARY KEY,\
    SUBNAME CHAR(50) NOT NULL,\
    SUBTYPE CHAR(1) NOT NULL)')

    # TKinter Window
    subjects_page = tk.Tk()
    subjects_page.geometry('1000x450')
    subjects_page.title('Add/Update/Delete Courses')
    subjects_page.iconbitmap('admin.ico')

    # Label1
    tk.Label(
        subjects_page,
        text='Faculty:',
        font=('Consolas', 15)
    ).place(x=156, y=128)

    conn = sqlite3.connect('student_info.db')
    cursor = conn.execute("SELECT DISTINCT FID FROM FACULTY")
    faculty = [row[0] for row in cursor]
    global faculty_combo
    faculty_combo = ttk.Combobox(subjects_page,values=faculty)
    faculty_combo.place(x=270,y=133)
    faculty_combo.current(0)

    # Label2
    tk.Label(
        subjects_page,
        text='List of Subjects',
        font=('Consolas', 20, 'bold')
    ).place(x=600, y=50)

    # Label3
    tk.Label(
        subjects_page,
        text='Add/Update/Delete Subject',
        font=('Consolas', 20, 'bold')
    ).place(x=100, y=50)

    # Label4
    tk.Label(
        subjects_page,
        text='Add information in the following prompt!',
        font=('Consolas', 10, 'italic')
    ).place(x=100, y=85)

    # Label5
    tk.Label(
        subjects_page,
        text='Subject code:',
        font=('Consolas', 15)
    ).place(x=100, y=180)

    # Entry1
    global subcode_entry
    subcode_entry = tk.Entry(
        subjects_page,
        font=('Consolas', 15),
        width=11
    )
    subcode_entry.place(x=270, y=180)

    # Label6
    tk.Label(
        subjects_page,
        text='Subject Name:',
        font=('Consolas', 15)
    ).place(x=100, y=230)

    # Text
    global subname_entry
    subname_entry = tk.Text(
        subjects_page,
        font=('Consolas', 10),
        width=17,
        height=3,
        wrap=tk.WORD
    )
    subname_entry.place(x=270, y=230)

    # Label7
    tk.Label(
        subjects_page,
        text='Subject Type:',
        font=('Consolas', 15)
    ).place(x=100, y=300)

    global combo
    combo = ttk.Combobox(subjects_page,values=['Lecture', 'Tutorial'])
    combo.place(x=270,y=307)
    combo.current(0)

    # Button1
    B1 = tk.Button(
        subjects_page,
        text='Add Subject',
        font=('Consolas', 12),
        command=parse_data
    )
    B1.place(x=150, y=380)

    # Button2
    B2 = tk.Button(
        subjects_page,
        text='Update Subject',
        font=('Consolas', 12),
        command=update_data
    )
    B2.place(x=410, y=380)

    # Treeview1
    global tree
    tree = ttk.Treeview(subjects_page)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subjects_page,
        text='Delete Subject',
        font=('Consolas', 12),
        command=remove_data
    )
    B3.place(x=680, y=380)

    # looping Tkiniter window
    subjects_page.mainloop()
    conn.close()  # close database ad=fter all operations
