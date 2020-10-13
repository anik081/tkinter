from tkinter import *
from tkinter import ttk
import time
import sqlite3
import tkinter.messagebox
import os
import sys
import re
userName =""
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
def submitLogin(logImApp,nameEntry,passEntry):
    try:

        def clear():
            nameEntry.delete(0,END)
            nameEntry.focus()
            passEntry.delete(0,END)

        name= nameEntry.get()
        password= passEntry.get()
        if name =="" or password == "":
            tkinter.messagebox.showwarning("WARNING","Please fill all fields")
        else:
            sql="""
            SELECT COUNT(*) FROM users WHERE user_name=? AND password=?
            """
            c.execute(sql,[name,password])
            count = c.fetchone()[0]
            conn.commit()
            if count>0:
                userName = name
                tkinter.messagebox.showinfo("Information","Successfully logged in!")
                import main

                logImApp.destroy()
                main.main_shop(userName)



            else:
                tkinter.messagebox.showwarning("Warning","No users found")
                clear()
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong222!")


def userLogin():
    logImApp = Tk()
    logImApp.title("Admin Interface")
    width_of_window=600
    height_of_window = 300
    screen_width =logImApp.winfo_screenwidth()
    screen_height = logImApp.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    logImApp.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    logImApp.title("Create User")
    logImApp.iconbitmap('icon.ico')
    titleLabel = Label(logImApp,text="Login as User Here!", fg="black", font="times 12 bold")
    titleLabel.place(x=200, y= 50)
    NameLabel = Label(logImApp,text="User Name" ,font="times 12 bold", fg="black")
    NameLabel.place(x=85, y= 100)
    passLabel = Label(logImApp, text="Password", font="times 12 bold", fg="black")
    passLabel.place(x=98, y = 150)
    nameEntry = Entry(logImApp, font="times 12 bold", width="25")
    nameEntry.place(x=210, y= 100)
    nameEntry.focus()
    passEntry = Entry(logImApp, font="times 12 bold", width="25",show="*")
    passEntry.place(x=210, y= 150)


    btnSubmit = Button(logImApp, text="Log In", font="times 12 bold", command=lambda: submitLogin(logImApp,nameEntry,passEntry))
    btnSubmit.place(x=360, y= 200)
    logImApp.bind("<Return>",lambda *args, logImApp=logImApp, nameEntry=nameEntry, passEntry= passEntry: submitLogin(logImApp,nameEntry,passEntry))

    userName=nameEntry.get()



    logImApp.mainloop()
if __name__=='__main__':
    userLogin()
