import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def update_p(d, p, tree, parent):
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time!")
            parent.destroy()
            return
        row = tree.item(tree.selection()[0])['values']
        if row[0] == 'No Class' and row[1] == 'No Class':
            conn.execute(f"DELETE FROM SCHEDULE WHERE ID='{str((d * periods) + p)}'")
            conn.commit()
            update_table()
            parent.destroy()
            return

        conn.commit()
        conn.execute(f"INSERT INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, FID, SID)\
            VALUES ('{str((d * periods) + p)}', {d}, {p}, '{row[1]}','{row[0]}','{id}')")
        conn.commit()
        update_table()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list!")
        parent.destroy()
        return

    parent.destroy()


def process_button(d, p):
    add_p = tk.Tk()
    add_p.title('Subjects')
    add_p.iconbitmap('student.ico')

    tk.Label(
        add_p,
        text='Select Subject',
        font=('Consolas', 12, 'bold')
    ).pack()

    tk.Label(
        add_p,
        text=f'Day: {day_names[d]}',
        font=('Consolas', 12)
    ).pack()

    tk.Label(
        add_p,
        text=f'Period: {period_names[p]}',
        font=('Consolas', 12)
    ).pack()

    tree = ttk.Treeview(add_p)
    tree['columns'] = ('one', 'two')
    tree.column("#0", width=0, stretch=tk.NO, anchor='c')
    tree.column("one", width=70, stretch=tk.NO, anchor='c')
    tree.column("two", width=80, stretch=tk.NO, anchor='c')
    tree.heading('#0', text="", anchor='c')
    tree.heading('one', text="Faculty", anchor='c')
    tree.heading('two', text="Subject Code", anchor='c')

    if combo1.get():   
        # get subject code list from the database     
        cursor = conn.execute(f"SELECT FID, SUBJECTS.SUBCODE\
        FROM SUBJECTS WHERE FID = '{combo1.get()}'")

    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1])
        )
    tree.insert("", 0, value=('No Class', 'No Class'))
    tree.pack(pady=10, padx=30)

    tk.Button(
        add_p,
        text="OK",
        padx=15,
        command=lambda x=d, y=p, z=tree, d=add_p: update_p(x, y, z, d)
    ).pack(pady=20)

    add_p.mainloop()

def update_table():
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FID, SID FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SID={id}")
            cursor = list(cursor)
            if len(cursor) != 0:
                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
            else:
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()

def register_course(student_id):
    global id
    global days
    global periods
    global butt_grid
    id = student_id
    days = 5
    periods = 6
    section = None
    butt_grid = []

    global period_names
    global day_names
    period_names = ['8am', '10am', '12pm', '2pm', '4pm', '6pm']
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']
    # connecting database
    global conn
    conn = sqlite3.connect('student_info.db')

    # creating Table in the database
    conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
    (ID CHAR(10) NOT NULL PRIMARY KEY,\
    DAYID INT NOT NULL,\
    PERIODID INT NOT NULL,\
    SUBCODE CHAR(10) NOT NULL,\
    FID CHAR(5) NOT NULL)')
    # DAYID AND PERIODID ARE ZERO INDEXED


    tt = tk.Tk()
    tt.title('Register Courses')
    tt.iconbitmap('student.ico')

    title_lab = tk.Label(
        tt,
        text='TIMETABLE',
        font=('Consolas', 20, 'bold'),
        pady=5
    )
    title_lab.pack()

    table = tk.Frame(tt)
    table.pack()

    first_half = tk.Frame(table)
    first_half.pack(side='left')

    for i in range(days):
        b = tk.Label(
            first_half,
            text=day_names[i],
            font=('Consolas', 12, 'bold'),
            width=9,
            height=2,
            bd=5,
            relief='raised'
        )
        b.grid(row=i + 1, column=0)

    for i in range(periods):
        b = tk.Label(first_half)
        b.grid(row=0, column=i + 1)

        b.config(
            text=period_names[i],
            font=('Consolas', 12, 'bold'),
            width=9,
            height=1,
            bd=5,
            relief='raised'
        )

    for i in range(days):
        b = []
        for j in range(periods):
            bb = tk.Button(first_half)
            bb.grid(row=i + 1, column=j + 1)


            bb.config(
                text='Hello World!',
                font=('Consolas', 10),
                width=13,
                height=3,
                bd=5,
                relief='raised',
                wraplength=80,
                justify='center',
                command=lambda x=i, y=j: process_button(x, y)
            )
            b.append(bb)

        butt_grid.append(b)
        b = []
    sec_select_f = tk.Frame(tt, pady=15)
    sec_select_f.pack()

    tk.Label(
        sec_select_f,
        text='Select Faculty:  ',
        font=('Consolas', 12, 'bold')
    ).pack(side=tk.LEFT)

    cursor = conn.execute("SELECT DISTINCT FID FROM FACULTY")
    sec_li = [row[0] for row in cursor]
    sec_li.insert(0, 'Select Your Faculty')

    global combo1
    combo1 = ttk.Combobox(
        sec_select_f,
        values=sec_li,
    )
    combo1.pack(side=tk.LEFT)
    combo1.current(0)

    update_table()

    tt.mainloop()