import tkinter as tk
from PIL import ImageTk, Image
import student as student_editing
import subjects as subject_editing
import faculty as faculty_editing

def adminpage():
    ad = tk.Tk()
    ad.geometry('650x500')
    ad.title('Admin')
    ad.iconbitmap('admin.ico')
    ad.config(bg='#7AC5CD')

    open_image = Image.open("admin_image.png")
    resized = open_image.resize((270,230))
    admin_image = ImageTk.PhotoImage(resized)
    label_image = tk.Label(ad, image=admin_image)
    label_image.config(bg='#7AC5CD')
    label_image.place(x=330,y=160)

    tk.Label(ad,text='ADMINISTRATOR',font=('Consolas', 20, 'bold'),bg='#7AC5CD',pady=10).pack()

    tk.Label(ad,text='You are the Administrator',font=('Consolas', 15, 'italic'),bg='#7AC5CD').pack(pady=9)

    tk.Label(ad,text='Please Choose Your Option',font=('Consolas', 13, 'italic'),bg='#7AC5CD').place(x=75,y=100)

    students_frame = tk.LabelFrame(text='Add/Remove/Update', font=('Consolas'), bg='#009ACD', padx=20)
    students_frame.place(x=75, y=143)

    tk.Button(students_frame,text='Students',font=('Consolas'),bg='#7AC5CD',command=student_editing.edit_student).pack(pady=20)
    tk.Button(students_frame,text='Courses',font=('Consolas'),bg='#7AC5CD',command=subject_editing.edit_subject).pack(pady=20)
    tk.Button(students_frame,text='Faculty',font=('Consolas'),bg='#7AC5CD',command=faculty_editing.edit_faculty).pack(pady=20)

    tk.Button(ad,text='Quit',font=('Consolas'),bg='#009ACD',fg='yellow',command=ad.destroy).place(x=275, y=430)

    ad.mainloop()