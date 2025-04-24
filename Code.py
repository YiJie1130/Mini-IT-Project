from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import admin_screen as admin
import student_screen as student
import sqlite3      
import pybase64

root = Tk()
root.geometry("620x400")
root.title("MULTIMEDIA UNIVERSITY REGISTRATION")
root.iconbitmap("bulb.ico")
root.config(bg='#C1CDCD')


def submit():
    connection = sqlite3.connect("student_info.db")
    cursor = connection.cursor()
    find_id = 'SELECT * FROM student_infos WHERE student_id = ?'
    cursor.execute(find_id,[(student_id.get())])
    find_id = cursor.fetchall()
    if find_id:
        messagebox.showerror("Failed",'Student ID Already Exist!')
        student_id.delete(0,END)
    elif len(student_id.get()) != 10:
        messagebox.showerror("Failed",'Please Enter 10 Character For Your Student ID!')
        student_id.delete(0,END)
    elif student_name.get() == "" or student_id.get() == "" or password.get() == "" or confirm_password.get() == "":
        messagebox.showerror("Failed",'PLEASE FILL IN THE REQUIREMENT!')
    elif password.get() == confirm_password.get():
        if password.get() == "" or confirm_password == "":
            messagebox.showerror("Failed",'PLEASE FILL IN THE REQUIREMENT!') 
        else:
            # CreATE a database or connect to one
            connection = sqlite3.connect('student_info.db')
            # create cursor,it do command
            cursor = connection.cursor()
            hash = password.get()
            hash = hash.encode("ascii")
            hash = pybase64.b64encode(hash)
            hash = hash.decode("ascii")
            # insert into table
            cursor.execute("INSERT INTO student_infos VALUES (:student_name, :student_id, :password, :faculty)",
                        {
                            'student_name': student_name.get(),
                            "student_id": student_id.get(),
                            "password": hash,
                            "faculty": combo.get()
                        })
            # Commit changes
            connection.commit()
            connection.close()

            # clear the text boxes
            student_name.delete(0, END)
            student_id.delete(0, END)
            password.delete(0, END)
            confirm_password.delete(0, END)
            combo.delete(0,END)
            messagebox.showinfo("Success",'REGISTER SUCCESSFUL!')
            root2.destroy()
    elif password.get() != confirm_password.get():
        messagebox.showerror("Failed",'PASSWORD IS NOT MATCH!')
        password.delete(0,END)
        confirm_password.delete(0,END)
    else:
        messagebox.showerror("Failed",'PLEASE FILL IN THE REQUIREMENT!')

def register():
    global root2
    global connection
    global student_name
    global student_id
    global password
    global confirm_password
    global combo
    global submit1

    root2 = Toplevel() 
    root2.geometry("780x340")
    root2.title("MULTIMEDIA UNIVERSITY REGISTRATION")
    root2.iconbitmap('questhead')
    root2.config(bg='#BDB76B')

    global register_image
    open_image = Image.open("register_image.png")
    resized = open_image.resize((220,200))
    register_image = ImageTk.PhotoImage(resized)
    label_image = Label(root2, image=register_image)
    label_image.place(x=500,y=50)

    Title = Label(root2,text="Register",font=('Consolas', 20, 'bold'), bg='#BDB76B')
    Title.grid(row=0,column=1)

    connection = sqlite3.connect('student_info.db')
    # create cursor,it do command
    cursor = connection.cursor()
    #Create table
    '''cursor.execute("""CREATE TABLE student_infos (
                student_name text,
                student_id INTEGER PRIMARY KEY,
                password text,
                faculty text
                )""")'''

    student_name = Entry(root2, width=35, bg='#FFF8DC')
    student_name.place(x=180,y=53,width=250)
    # student_name.grid(row=1, column=1, padx=20, pady=10)
    student_id = Entry(root2, width=35, bg='#FFF8DC')
    student_id.place(x=180,y=98,width=250)
    # student_id.grid(row=2, column=1, padx=20, pady=10)
    password = Entry(root2, width=35, show="•", bg='#FFF8DC')
    password.place(x=180,y=143,width=250)
    # password.grid(row=3, column=1, padx=20, pady=10)
    confirm_password = Entry(root2, width=35, show="•", bg='#FFF8DC')
    confirm_password.place(x=179,y=189,width=250)
    # confirm_password.grid(row=4, column=1, padx=20, pady=10)

    conn = sqlite3.connect('student_info.db')
    cursor = conn.execute("SELECT DISTINCT FID FROM FACULTY")
    faculty = [row[0] for row in cursor]
    combo = ttk.Combobox(root2,values=faculty)
    combo.place(x=180,y=237)
    combo.current(0)
    # deletebox = Entry(root2, width=35)
    # deletebox.grid(row=9, column=1, padx=20, pady=5)

    student_name_label = Label(root2, text="Student Name:", font=('Consolas', 13, 'bold'), bg='#BDB76B')
    student_name_label.grid(row=1, column=0, pady=10)
    student_id_label = Label(root2, text="Student ID:", font=('Consolas', 13, 'bold'), bg='#BDB76B')
    student_id_label.grid(row=2, column=0, pady=10)
    password_label = Label(root2, text="Password:", font=('Consolas', 13, 'bold'), bg='#BDB76B')
    password_label.grid(row=3, column=0, pady=10)
    confirm_password_label = Label(root2, text="Confirm Password:", font=('Consolas', 12, 'bold'), bg='#BDB76B')
    confirm_password_label.grid(row=4, column=0, pady=10)
    faculty_label = Label(root2, text="Faculty:", font=('Consolas', 13, 'bold'), bg='#BDB76B')
    faculty_label.grid(row=5, column=0, pady=10)
    
    # Submit button
    submit1 = Button(root2, text="Sign Up", bg='#F4A460', command=submit)
    submit1.place(x=200, y=282, height=28, width=110)

    # Commit changes
    connection.commit()
    connection.close()

def login():   
    conn = sqlite3.connect('student_info.db')

    user = str(combo1.get())
    if user == "Student":
        connection = sqlite3.connect("student_info.db")
        cursor = connection.cursor()
        hashed = password_enter.get()
        hashed = hashed.encode("ascii")
        hashed = pybase64.b64encode(hashed)
        hashed = hashed.decode("ascii")         
        find_user = 'SELECT * FROM student_infos WHERE student_id = ? and password = ?'
        cursor.execute(find_user,[(id_enter.get()), (hashed)])
        result = cursor.fetchall()
        if result:
            messagebox.showinfo("Success", 'LOGIN SUCCESSFUL')
            student_id = id_enter.get()
            root.destroy()               
            student.student_page(student_id)
        else:
            messagebox.showerror("Failed", 'Incorrect Username or Password!')
            id_enter.delete(0,END)
            password_enter.delete(0,END) 

    elif user == "Admin":
        if id_enter.get() == 'admin' and password_enter.get() == 'admin':
            messagebox.showinfo("Success", 'Welcome Admin')
            root.destroy()
            admin.adminpage()
            # os.system('admin_screen.py')
            # sys.exit()
        else:
            messagebox.showerror('Failed', 'Incorrect Username or Password!')
            id_enter.delete(0,END)
            password_enter.delete(0,END)

def Show_password():
    if password_enter.cget('show') == '•':
        password_enter.config(show='')
    else:
        password_enter.config(show='•')

def Login():
    root1 = Toplevel()
    root1.geometry("650x340")
    root1.title("MULTIMEDIA UNIVERSITY REGISTRATION")
    root1.iconbitmap("questhead")
    root1.config(bg='#FFB5C5')

    global login_image
    open_image = Image.open("login_image.png")
    resized = open_image.resize((240,220))
    login_image = ImageTk.PhotoImage(resized)
    label_image = Label(root1, image=login_image)
    label_image.place(x=380,y=50)

    Title = Label(root1,text="Log in",font=('Consolas', 20, 'bold'), bg='#FFB5C5')
    Title.grid(row=0,column=1)

    #CreATE a database or connect to one
    connection = sqlite3.connect('student_info.db')
    #create cursor,it do command
    cursor = connection.cursor()

    username_label = Label(root1, text="Student ID:", font=('Consolas', 12, 'bold'), bg='#FFB5C5')
    password_label = Label(root1, text="Password:", font=('Consolas', 12, 'bold'), bg='#FFB5C5')

    username_label.grid(row=1, column=0, padx=20, pady=20)
    password_label.grid(row=2, column=0, padx=20, pady=20)

    global id_enter
    id_enter = Entry(root1, width=20, bg='#FFF8DC')
    id_enter.place(x=130,y=63,width=200)

    global password_enter
    password_enter = Entry(root1, width=20, bg='#FFF8DC', show="•")
    password_enter.place(x=129,y=130,width=200)

    show_password = Checkbutton(root1,text="show password", bg='#FFB5C5',command=Show_password)
    show_password.place(x=127, y=158)

    #submitbutton = Button(root, text="Login", activebackground="white", activeforeground="blue",command=login)
    submitbutton = tk.Button(root1,text='Login',font=('Consoles', 12, 'bold'),borderwidth=1,relief="raised", bg='#FFBBFF',activebackground="#FF82AB", activeforeground="blue",command=login)
    submitbutton.place(x=126,y=230,width=150)

    global combo1
    combo1 = ttk.Combobox(root1,values=['Student', 'Admin'])
    combo1.place(x=130,y=190)
    combo1.current(0)

    label = Label(root1,text="Don't have an account?",font=('Microsoft Yahei UI Light',9), bg='#FFB5C5')
    label.place(x=120,y=280)
    register_button = Button(root1,width=6,text='Register',border=0,fg='blue', bg='#FFB5C5',command=register)
    register_button.place(x=255,y=281)

open_image = Image.open("MMU.png")
resized = open_image.resize((150,60))
mmu_image = ImageTk.PhotoImage(resized)
label_image = Label(root, image=mmu_image)
label_image.place(x=240,y=10)
Title = Label(root,text="Multimedia Registration",font=('Consolas', 20, 'bold'))
Title.place(x=150,y=70)

frame_login_register = LabelFrame(root,padx=100,pady=70,bg='#E0EEEE')
frame_login_register.place(x=150,y=150)

opening_register_button = Button(frame_login_register,text='Register',borderwidth=8,command=register)
opening_register_button.grid(row=0,column=0)

opening_login_button = Button(frame_login_register,text='Login',borderwidth=8,command=Login)
opening_login_button.grid(row=0,column=2)

root.mainloop()