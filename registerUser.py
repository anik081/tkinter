from tkinter import *
from tkinter import ttk
import time
import sqlite3
import tkinter.messagebox
import os
import sys
import re
data_directory ="./Database"
image_directory="./icons"
back_directory ="./Background"
invoice_directory ="./invoice"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)
if not os.path.exists(image_directory):
    os.makedirs(image_directory)
if not os.path.exists(back_directory):
    os.makedirs(back_directory)
if not os.path.exists(invoice_directory):
    os.makedirs(invoice_directory)
conn = sqlite3.connect("./Database/med_store.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists "users" (
	"id"	INTEGER,
	"user_name"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")
conn.commit()
def submitUser(nameEntry,passEntry,conPassEntry):
    try:
        def clear():
            nameEntry.delete(0,END)
            nameEntry.focus()
            passEntry.delete(0,END)
            conPassEntry.delete(0,END)
        name = nameEntry.get()
        password = passEntry.get()
        conPass = conPassEntry.get()

        if len(password)<6:
            tkinter.messagebox.showwarning("WARNING","Password Should be atleast 6 characters")
            clear()
        elif password != conPass:
            tkinter.messagebox.showwarning("WARNING","Passwords did not match")
            clear()
        elif name =="" or password=="" or conPass=="":
            tkinter.messagebox.showwarning("WARNING","Please fill all fileds")
            clear()
        else:

            sql ="""
            INSERT into users(user_name,password)
            VALUES(?,?)
            """
            sqlCheck ="""
            SELECT COUNT(*) FROM users WHERE user_name=?
            """
            c.execute(sqlCheck,[name])
            count = c.fetchone()[0]
            conn.commit()
            if count > 0:
                tkinter.messagebox.showwarning("WARNING","Already a user")
                clear()
            else:
                c.execute(sql,[name,password])
                conn.commit()
                tkinter.messagebox.showinfo("Information","Successfully created a new user")
                clear()
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong!")



def userReg():
    userApp = Tk()
    userApp.title("Admin Interface")
    width_of_window=600
    height_of_window = 300
    screen_width =userApp.winfo_screenwidth()
    screen_height = userApp.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    userApp.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    userApp.title("Create User")
    userApp.iconbitmap('icon.ico')
    titleLabel = Label(userApp,text="Create User Here!", fg="black", font="times 12 bold")
    titleLabel.place(x=200, y= 50)
    NameLabel = Label(userApp,text="User Name" ,font="times 12 bold", fg="black")
    NameLabel.place(x=85, y= 100)
    passLabel = Label(userApp, text="Password", font="times 12 bold", fg="black")
    passLabel.place(x=98, y = 150)
    conPassLabel = Label(userApp, text="Confirm Password", font="times 12 bold", fg="black")
    conPassLabel.place(x=45, y= 200)
    nameEntry = Entry(userApp, font="times 12 bold", width="25")
    nameEntry.place(x=210, y= 100)
    nameEntry.focus()
    passEntry = Entry(userApp, font="times 12 bold", width="25",show="*")
    passEntry.place(x=210, y= 150)
    conPassEntry = Entry(userApp, font="times 12 bold", width="25",show="*")
    conPassEntry.place(x=210, y= 200)

    btnSubmit = Button(userApp, text="Create", font="times 12 bold", command=lambda: submitUser(nameEntry,passEntry,conPassEntry))
    btnSubmit.place(x=360, y= 250)
    userApp.bind("<Return>",lambda *args, nameEntry=nameEntry, passEntry= passEntry, conPassEntry = conPassEntry: submitUser(nameEntry,passEntry,conPassEntry))



    userApp.mainloop()
userReg()
