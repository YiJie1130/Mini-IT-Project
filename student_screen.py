import tkinter as tk
import sqlite3
from tkinter import ttk
from PIL import ImageTk, Image
import register_course as register_course
import timetable_student as view_timetable

def create_treeview():
    #design treeview
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 3)))
    tree.column("#0", width=0, stretch=tk.NO, anchor='c', minwidth=0)
    tree.column("#1", width=120, stretch=tk.NO, anchor='c', minwidth=100)
    tree.column("#2", width=200, stretch=tk.NO, anchor='c', minwidth=200)
    tree.heading('#0', text="", anchor='c')
    tree.heading('#1', text="Name", anchor='c')
    tree.heading('#2', text="Student ID", anchor='c')
    tree['height'] = 12

def update_treeview():
    conn = sqlite3.connect("student_info.db")
    cursor = conn.execute("SELECT student_name, student_id FROM student_infos")
    for row in cursor:
        tree.insert(
            "",
            'end',
            values=(row[0], row[1])
        )
    tree.place(x=50, y=75)

def view_student():
    student_page = tk.Tk()
    student_page.geometry('420x430')
    student_page.title('View Student')
    student_page.iconbitmap('student.ico')

    tk.Label(student_page,text='Student List',font=('Consolas', 20, 'bold')).place(x=100,y=15)
    tk.Button(student_page,text='Back to Student Page',command=student_page.destroy).place(x=125,y=380)
    global tree
    tree = ttk.Treeview(student_page)
    create_treeview()
    update_treeview()

def create_coursestreeview():
    courses_tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 3)))
    courses_tree.column("#0", width=0, stretch=tk.NO, anchor='c', minwidth=0)
    courses_tree.column("#1", width=100, stretch=tk.NO, anchor='c', minwidth=100)
    courses_tree.column("#2", width=200, stretch=tk.NO, anchor='c', minwidth=200)
    courses_tree.heading('#0', text="", anchor='c')
    courses_tree.heading('#1', text="Faculty", anchor='c')
    courses_tree.heading('#2', text="Subject", anchor='c')
    courses_tree['height'] = 12

def update_coursestreeview():
    conn = sqlite3.connect("student_info.db")
    cursor = conn.execute("SELECT FID, SUBNAME FROM SUBJECTS")
    for row in cursor:
        courses_tree.insert(
            "",
            'end',
            values=(row[0], row[1])
        )
    courses_tree.place(x=60, y=75)

def courses_offered():
    courses_page = tk.Tk()
    courses_page.geometry('420x430')
    courses_page.title('Browse Courses Offered')
    courses_page.iconbitmap('student.ico')

    tk.Label(courses_page,text='Courses Offered',font=('Consolas', 20, 'bold')).place(x=107,y=15)
    tk.Button(courses_page,text='Back to Student Page',command=courses_page.destroy).place(x=135,y=380)
    global courses_tree
    courses_tree = ttk.Treeview(courses_page)
    create_coursestreeview()
    update_coursestreeview()
    
def student_page(student_id):
    student_menu= tk.Tk()
    student_menu.geometry('950x430')
    student_menu.title('Student')
    student_menu.iconbitmap('student.ico')
    student_menu.config(bg='#7AC5CD')

    open_image = Image.open("student_image.png")
    resized = open_image.resize((270,230))
    student_image = ImageTk.PhotoImage(resized)
    label_image = tk.Label(student_menu, image=student_image)
    label_image.config(bg='#7AC5CD')
    label_image.place(x=330,y=120)

    tk.Label(student_menu,text='WELCOME STUDENT',font=('Consolas', 25, 'bold'),bg='#7AC5CD',pady=10).place(x=340,y=30)

    tk.Label(student_menu,text='Please choose your option',font=('Consolas', 13, 'italic'),bg='#7AC5CD').place(x=95,y=100)

    studentsmenu_frame = tk.LabelFrame(text='OPTION', font=('Consolas'), padx=20, fg='#FFFF00', bg='#009ACD')
    studentsmenu_frame.place(x=95, y=143)

    tk.Button(studentsmenu_frame,text='View Students',font=('Consolas'),bg='#8DEEEE',command=view_student).pack(pady=20)
    tk.Button(studentsmenu_frame,text='Browse\nCourses Offered',font=('Consolas'),bg='#8DEEEE',command=courses_offered).pack(pady=20)

    tk.Label(student_menu,text='Please choose your option',font=('Consolas', 13, 'italic'),bg='#7AC5CD').place(x=620,y=100)

    timetable_frame = tk.LabelFrame(student_menu, text='Timetable', font=('Consolas'), padx=20, fg='#FFFF00', bg='#009ACD')
    timetable_frame.place(x=620, y=146)

    tk.Button(timetable_frame,text='Register Courses',font=('Consolas'),bg='#8DEEEE',command=lambda:register_course.register_course(student_id)).pack(pady=20)
    tk.Button(timetable_frame,text='View Timetable',font=('Consolas'),bg='#8DEEEE',command=lambda:view_timetable.view_timetable(student_id)).pack(pady=20)

    tk.Button(student_menu,text='Quit',font=('Consolas'),fg='#FFFF00',bg='#009ACD',command=student_menu.destroy).place(x=420, y=370)

    student_menu.mainloop()