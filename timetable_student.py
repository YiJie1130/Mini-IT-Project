import tkinter as tk
import sqlite3

def update_table(sec):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f'SELECT SUBCODE, FID, SID FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SID={id}')
            cursor = list(cursor)

            butt_grid[i][j]['bg'] = 'white'
            if len(cursor) != 0:
                subcode = cursor[0][0]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = 'white'
                if subtype == 'Lecture':
                    butt_grid[i][j]['bg'] = 'green'
                elif subtype == 'Tutorial':
                    butt_grid[i][j]['bg'] = 'blue'

                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
            else:
                butt_grid[i][j]['fg'] = 'black'
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()


def process_button(d, p, sec):
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SUBCODE, FID FROM SCHEDULE\
                WHERE ID='{str((d * periods) + p)}'")
    cursor = list(cursor)
    if len(cursor) != 0:
        subcode = str(cursor[0][0])
        fid = str(cursor[0][1])

        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])

    else:
        subcode = fid = subname = 'None'

    tk.Label(details, text='Class Details', font=('Consolas', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: ' + day_names[d], font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Time: ' + period_names[p], font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: ' + subcode, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Name: ' + subname, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Name: ' + fid, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Consolas'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()


def student_tt_frame(tt, sec):
    title_lab = tk.Label(
        tt,
        text='TIMETABLE',
        font=('Consolas', 20, 'bold'),
        pady=5
    )
    title_lab.pack()

    global section
    section = sec

    table = tk.Frame(tt)
    table.pack()

    first_half = tk.Frame(table)
    first_half.pack(side='left')

    second_half = tk.Frame(table)
    second_half.pack(side='left')


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
                command=lambda x=i, y=j, z=sec: process_button(x, y, z)
            )
            b.append(bb)

        butt_grid.append(b)
        b = []

    update_table(sec)

def view_timetable(student_id):
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

    tt = tk.Tk()
    tt.title('View Timetable')
    tt.iconbitmap('student.ico')

    student_tt_frame(tt, section)

    sec_select_f = tk.Frame(tt, pady=15)
    sec_select_f.pack()

    tk.Canvas(
        sec_select_f,
        width=50,
        height=45,
        bg='green'
    ).pack(side=tk.LEFT)

    tk.Label(
        sec_select_f,
        text=':Lecture',
        font=('Consolas', 12, 'bold')
    ).pack(side=tk.LEFT) 

    tk.Canvas(
        sec_select_f,
        width=50,
        height=45,
        bg='blue'
    ).pack(side=tk.LEFT)

    tk.Label(
        sec_select_f,
        text=':Tutorial',
        font=('Consolas', 12, 'bold')
    ).pack(side=tk.LEFT) 

    tt.mainloop()