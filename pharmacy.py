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
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

conn = sqlite3.connect("./Database/med_store.db")
c = conn.cursor()

c.execute("""CREATE TABLE if not exists "inventory" (
	"id"	INTEGER,
	"medicine_name"	TEXT,
	"company_name"	TEXT,
	"stock"	INTEGER,
	"cost_per_unit"	REAL,
	"sell_per_unit"	REAL,
	"buy_from"	TEXT,
	"buy_from_contact"	TEXT,
	"shelf"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")
conn.commit()
c.execute("SELECT COUNT(*) from inventory")
id = c.fetchone()[0]
c.execute("SELECT medicine_name,company_name FROM inventory WHERE stock <= 10 ")
lessThanTen = c.fetchall()
warnStock =""
warnStockLen = len(lessThanTen)
for item in lessThanTen:
    warnStock =warnStock+"   "+str(item)
c.execute("""CREATE TABLE if not exists "company_table" (
	"id"	INTEGER,
	"company_name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")
conn.commit()
c.execute("""CREATE TABLE if not exists "medicine_table" (
	"id"	INTEGER,
	"medicine_name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")

conn.commit()
c.execute("""CREATE TABLE if not exists "revenue" (
	"id"	INTEGER,
	"cost_per_transaction"	FLOAT,
    "sell_per_transaction"	FLOAT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")

conn.commit()
c.execute("""CREATE TABLE if not exists "transactions" (
	"id"	INTEGER,
	"medicine_name"	TEXT,
    "company_name" TEXT,
    "quantity" Text,
    "amount" TEXT,
    "date" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
""")
conn.commit()
def adminArea(userName):
    apt=Tk()
    apt.title("Admin Interface")
    width_of_window=1496
    height_of_window = 705
    screen_width =apt.winfo_screenwidth()
    screen_height = apt.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    apt.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    apt.title("Stock Maintainance")
    apt.iconbitmap('icon.ico')
    header = Frame(apt, bg='darkcyan')
    footer = Frame(apt, bg='black')
    apt.columnconfigure(0, weight=1) # 100%
    apt.rowconfigure(0, weight=1) # 10%
    apt.rowconfigure(3,weight=1)
    apt.rowconfigure(4,weight=1)
    apt.rowconfigure(5,weight=1)
    apt.rowconfigure(6,weight=1)
    apt.rowconfigure(7,weight=1)
    apt.rowconfigure(8,weight=1)
    apt.rowconfigure(9,weight=1)
    apt.rowconfigure(10, weight=1) # 10%
    header.grid(row=0, sticky="news")
    footer.grid(row=10,sticky="news")
    Label(apt, text="Feni Medical Hall",font="times  30 bold", fg="black", bg="darkcyan" ).grid(row=0,column=0,columnspan=100)
    address_apt =Label(apt,text="677, East Dholaipar Bajar, Dania Road, Dhaka-1362", bg="darkcyan", font="times 12 bold", fg="black")
    address_apt.place(x=567, y=57)

    Label(apt, text='*'*280).grid(row=1,column=0,columnspan=3)
    Label(apt, text='-'*280).grid(row=2,column=0,columnspan=3)
    userLabel = Label(apt, text="User: ", font="times 12 bold")
    userLabel.place(x= 50, y= 100)
    userLabel1 = Label(apt, text=userName, font="times 12 bold")
    userLabel1.place(x= 100, y= 100)

    Label(apt, text="Stock Maintainance", font="times 18").grid(row=2,column=0)
    Button(apt,text='Add Company Name',font="times 12 bold",bg="darkcyan",fg ="black", width=25, command=addCompanyName).grid(row=3,column=0, columnspan=2)
    Button(apt,text='Delete Company Name',font="times 12 bold",bg="darkcyan",fg ="red", width=25, command= del_company).grid(row=4,column=0)
    Button(apt,text='Add Medicine Name',font="times 12 bold",bg="darkcyan",fg ="black", width=25,command=addMedName).grid(row=5,column=0)
    Button(apt,text='Delete Medicine Name',font="times 12 bold",bg="darkcyan",fg ="red", width=25, command=del_medicine).grid(row=6,column=0)
    Button(apt,text='Add Medicine Info',font="times 12 bold",bg="darkcyan",fg ="black", width=25, command=add_to_stock).grid(row=7,column=0)
    Button(apt,text='Edit Medicine Info',font="times 12 bold",bg="darkcyan",fg ="black", width=25, command= updateItem).grid(row=8,column=0)
    Button(apt,text='Delete Medicine from Stock',font="times 12 bold",bg="darkcyan",fg ="red", width=25, command=delete_stock).grid(row=9,column=0)
    Label(apt, text="Developed By Md. Mydul Islam Anik.. (01521332139)", font="times 18", bg="black", fg="darkcyan").grid(row=10,column=0)
    revenueLabel = Button(apt, text="Total Revenue", font="times 12 bold", bg="darkcyan", fg="black", command=revenue)
    revenueLabel.place(x= 100, y= 350)
    backImage = PhotoImage(file='home.png')
    background_label = Label(apt, image=backImage)
    background_label.place(x=1000, y= 250)

    apt.mainloop()
def revenue():
    rev = Tk()
    width_of_window=496
    height_of_window = 205
    screen_width =rev.winfo_screenwidth()
    screen_height = rev.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    rev.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    rev.title("Revenue")
    rev.iconbitmap('plus.ico')
    costLabel = Label(rev, text="Total cost: ", fg="black", font ="times 12 bold")
    costLabel.place(x= 150, y= 50)
    costLabelamount = Label(rev, text="", fg="black", font ="times 12 bold")
    costLabelamount.place(x= 300, y= 50)
    sellLabel = Label(rev, text="Total Sell: ", fg="black", font ="times 12 bold")
    sellLabel.place(x= 150, y=100)
    sellLabelamount = Label(rev, text="", fg="black", font ="times 12 bold")
    sellLabelamount.place(x= 300, y= 100)

    revLabel = Label(rev, text="Total Revenue: ", fg="black", font ="times 12 bold")
    revLabel.place(x= 150, y= 150)
    revLabelamount = Label(rev, text="", fg="black", font ="times 12 bold")
    revLabelamount.place(x= 300, y= 150)
    sqlCost ="""
    SELECT SUM(amount_cost) FROM transactions
    """
    c.execute(sqlCost)
    cost = c.fetchone()[0]
    conn.commit()
    costLabelamount.configure(text=str(cost))
    sqlSell ="""
    SELECT SUM(amount) FROM transactions
    """
    c.execute(sqlSell)
    sell = c.fetchone()[0]
    conn.commit()
    sellLabelamount.configure(text=str(sell))
    revLabelamount.configure(text=str(float(sell)-float(cost)))




    rev.mainloop()





def addCompanyName(*args):
    comName = Tk()
    width_of_window=496
    height_of_window = 205
    screen_width =comName.winfo_screenwidth()
    screen_height = comName.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    comName.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    comName.title("Add Company Name")
    comName.iconbitmap('plus.ico')
    title_label=Label(comName, text="Add Company Name Here!!", font="times 12 bold", fg="darkcyan")
    title_label.place(x=160,y=10)
    com_entry = Entry(comName,width=15, font="times 20")
    com_entry.place(x=150,y=50)
    com_entry.focus()
    btn_add = Button(comName, text="Add Medicine",width=10, bg="darkcyan", command=lambda: get_item(com_entry))
    btn_add.place(x=280,y=100)
    def get_item(com_entry):
        try:

            Name = com_entry.get().upper().format()
        except KeyError:
            tkinter.messagebox.showerror("showerror","Can't use {} brackets",parent=comName)
        if Name == '':
            tkinter.messagebox.showerror("showerror","Please fill the required boxes",parent=comName)
        else:
            try:
               sql="""
               INSERT into company_table(company_name)
               VALUES(?)
               """
               getName ="SELECT COUNT(company_name) FROM company_table WHERE company_name=?"
               c.execute(getName,[Name])
               conn.commit()
               count = c.fetchone()[0]
               if count > 0:
                  tkinter.messagebox.showwarning("Information","You already added this", parent=comName)
               else:
                  c.execute(sql,[Name])
                  conn.commit()
                  com_entry.delete(0,END)
                  tkinter.messagebox.showinfo("Information","Successfully Added", parent=comName)

            except:
                tkinter.messagebox.showerror("showerror", "Oops! Something went wrong1", parent=comName)
    comName.bind("<Return>", lambda *args, com_entry= com_entry: get_item(com_entry))
    comName.mainloop()


def addMedName(*args):
    MedName = Tk()
    width_of_window=496
    height_of_window = 205
    screen_width =MedName.winfo_screenwidth()
    screen_height = MedName.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    MedName.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    MedName.title("Add Medicine Name")
    MedName.iconbitmap('plus.ico')
    title_label=Label(MedName, text="Add Medicine Name Here!!", font="times 12 bold", fg="darkcyan")
    title_label.place(x=160,y=10)
    Med_entry = Entry(MedName,width=15, font="times 20")
    Med_entry.place(x=150,y=50)
    btn_add = Button(MedName, text="Add Medicine",width=10, bg="darkcyan", command=lambda: get_item(Med_entry))
    btn_add.place(x=280,y=100)
    def get_item(Med_entry):
        try:
            Name = Med_entry.get().upper().format()
        except KeyError:
            tkinter.messagebox.showerror("showerror","Can't use {} brackets",parent=MedName)

        if Name == '':
            tkinter.messagebox.showerror("showerror","Please fill the required boxes",parent=MedName)
        else:
            try:
               sql="""
               INSERT into medicine_table(medicine_name)
               VALUES(?)
               """
               getName ="SELECT COUNT(medicine_name) FROM medicine_table WHERE medicine_name=?"
               c.execute(getName,[Name])
               count = c.fetchone()[0]
               conn.commit()
               if count > 0:
                  tkinter.messagebox.showwarning("Information","You already added this", parent=MedName)
               else:
                  c.execute(sql,[Name])
                  conn.commit()
                  Med_entry.delete(0,END)
                  tkinter.messagebox.showinfo("Information","Successfully Added", parent=MedName)
            except:
                tkinter.messagebox.showerror("showerror", "Oops! Something went wrong2", parent=MedName)
    MedName.bind("<Return>", lambda *args, Med_entry= Med_entry: get_item(Med_entry))
    MedName.mainloop()

def del_company():
    delCom = Tk()
    width_of_window=496
    height_of_window =205
    screen_width =delCom.winfo_screenwidth()
    screen_height = delCom.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    delCom.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    delCom.title("Delete Company Name")
    delCom.iconbitmap('plus.ico')
    lst_com=[]
    def clear_all():
        c.execute("SELECT company_name FROM company_table ORDER BY company_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl = ttk.Combobox(delCom,width=25 ,font="times 12 bold",state='readonly')
        ddl['values'] = lst_c
        ddl.place(x=150,y=50)
        ddl.set("Choose Company")
    title_label = Label(delCom, text="Delete Company Name", font="times 12 bold", fg="red")
    title_label.place(x=160,y=10)
    try:
        c.execute("SELECT company_name FROM company_table ORDER BY company_name")
        conn.commit()
        lst =c.fetchall()
        i =0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl = ttk.Combobox(delCom,width=25 ,font="times 12 bold",state='readonly')
        ddl['values'] = lst_c
        ddl.place(x=150,y=50)
        ddl.set("Choose Company")
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong3!", parent=delCom)
    btn_del = Button(delCom, text="Delete Company",width=15, bg="darkcyan", command=lambda :del_item(ddl))
    btn_del.place(x=280,y=100)
    def del_item(ddl):
        try:
            Name = ddl.get()
            sql = "DELETE FROM company_table WHERE company_name=?"
            c.execute(sql,[Name])
            conn.commit()
            tkinter.messagebox.showinfo("Information","Successfully Deleted", parent=delCom)
            clear_all()
            delCom.destroy()
            del_company()
        except :
            tkinter.messagebox.showerror("showerror","Ops! Something went wrong4!", parent=delCom)
    delCom.bind("<Return>", lambda *args, ddl= ddl: del_item(ddl))
    delCom.mainloop()

def del_medicine():
    delMed = Tk()
    width_of_window=496
    height_of_window =205
    screen_width =delMed.winfo_screenwidth()
    screen_height = delMed.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    delMed.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    delMed.title("Delete Medicine Name")
    delMed.iconbitmap('plus.ico')
    title_label = Label(delMed, text="Delete Medicine Name", font="times 12 bold", fg="red")
    title_label.place(x=160,y=10)
    def clear_all():
        c.execute("SELECT medicine_name FROM medicine_table ORDER BY medicine_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl = ttk.Combobox(delMed,width=25 ,font="times 12 bold",state='readonly')
        ddl['values'] = lst_c
        ddl.place(x=150,y=50)
        ddl.set("Choose Medicine")
    try:
        c.execute("SELECT medicine_name FROM medicine_table ORDER BY medicine_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl = ttk.Combobox(delMed,width=25 ,font="times 12 bold",state='readonly')
        ddl['values'] = lst_c
        ddl.place(x=150,y=50)
        ddl.set("Choose Medicine")
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong5!", parent=delMed)
    btn_del = Button(delMed, text="Delete Medicine",width=15, bg="darkcyan", command=lambda :del_item(ddl))
    btn_del.place(x=280,y=100)
    def del_item(ddl):
        try:
            Name = ddl.get()
            sql = "DELETE FROM medicine_table WHERE medicine_name=?"
            c.execute(sql,[Name])
            conn.commit()
            tkinter.messagebox.showinfo("Information","Successfully Deleted", parent=delMed)
            clear_all()
            delMed.destroy()
            del_medicine()
        except Exception as e:
            tkinter.messagebox.showerror("showerror","Something Went Wrong6!",parent=delMed)
    delMed.bind("<Return>", lambda *args, ddl= ddl: del_item(ddl))
    delMed.mainloop()


def add_to_stock():
    adStock = Tk()
    width_of_window = 1300
    height_of_window =750
    screen_width =adStock.winfo_screenwidth()
    screen_height = adStock.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    adStock.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    adStock.title("Add medicine to stock")
    adStock.iconbitmap('plus.ico')
    header = Frame(adStock, bg='darkcyan')
    footer = Frame(adStock, bg='black')
    adStock.columnconfigure(0, weight=1) # 100%
    adStock.rowconfigure(3, weight=1) # 10%
    adStock.rowconfigure(5,weight=8)
    adStock.rowconfigure(9,weight=1)
    footer.grid(row=9,sticky="snew")
    header.grid(row=3,sticky="snew")
    adStock.call('wm', 'attributes', '.', '-topmost', True)
    adStock.after_idle(adStock.call, 'wm', 'attributes', '.', '-topmost', False)
    adStock.focus_force()
    def clear_all():
        ddl_C_e.set("Choose Company")
        ddl_M_e.set("Choose Medicine")
        stock_E.delete(0,END)
        cp_e.delete(0,END)
        sp_e.delete(0,END)
        vendor_e.delete(0,END)
        vendorC_e.delete(0,END)
        shelf_e.delete(0,END)
    def get_items(*args):
        ddl_C = ddl_C_e.get()
        ddl_M = ddl_M_e.get()
        stock= stock_E.get()
        cp = cp_e.get()
        sp = sp_e.get()
        vendor = vendor_e.get()
        vendorC = vendorC_e.get()
        shelf = shelf_e.get()

        checkNumber = check_if_number(stock)
        checkFloatCp = check_if_float(cp)
        checkFloatSp =check_if_float(sp)

        if ddl_C == 'Choose Company' or ddl_M == 'Choose Medicine' or stock == '' or sp == '':
            tkinter.messagebox.showinfo("Information","Please fill up neccessary boxes", parent=adStock)
        elif checkNumber == 0 or checkFloatCp ==0 or checkFloatSp == 0:
            tkinter.messagebox.showinfo("Information","Invalid Input", parent=adStock)
        else:
            try:
                c.execute("SELECT COUNT(*) FROM inventory WHERE medicine_name=? AND company_name =?",[ddl_M,ddl_C])
                conn.commit()
                count_med = c.fetchone()[0]
                if count_med > 0:
                    old_stock ="""
                    SELECT stock
                    FROM inventory
                    WHERE medicine_name = ? AND company_name=?

                    """
                    c.execute(old_stock,[ddl_M,ddl_C])
                    conn.commit()
                    temp_stock = c.fetchone()[0]
                    temp_stock = int(temp_stock)
                    new_stock = (int(stock) + temp_stock)

                    update_sql="""
                    UPDATE inventory
                    SET stock=?,
                        cost_per_unit=?,
                        sell_per_unit=?,
                        buy_from=?,
                        buy_from_contact=?,
                        shelf = ?
                    WHERE
                        medicine_name=? AND company_name =?

                        """
                    c.execute(update_sql,[new_stock,cp,sp,vendor,vendorC,shelf,ddl_M,ddl_C])
                    conn.commit()
                    tkinter.messagebox.showinfo("Information","Successfully Updated", parent=adStock)
                    clear_all()


                else:
                    insert_sql = """
                    INSERT INTO inventory(
                                    medicine_name,
                                    company_name,
                                    stock,
                                    cost_per_unit,
                                    sell_per_unit,
                                    buy_from,
                                    buy_from_contact,
                                    shelf
                                    ) VALUES(?,?,?,?,?,?,?,?)
                        """
                    c.execute(insert_sql,[ddl_M,ddl_C,stock,cp,sp,vendor,vendorC,shelf])
                    conn.commit()
                    tkinter.messagebox.showinfo("Information","Successfully Added", parent=adStock)
                    clear_all()
                    adStock.destroy()
                    add_to_stock()
            except :
                tkinter.messagebox.showerror("showerror","Ops! Something Went Wrong88!!")

    header_l = Label( adStock, text= "Feni Medical Hall" , font= "times 25 bold", bg= "darkcyan")
    header_l.place(x= 500, y =10)
    address_l = Label( adStock, text= "677, East Dholaipar Bajar, Dania Road, Dhaka-1362" , font= "times 10 bold", bg= "darkcyan")
    address_l.place(x= 485, y =50)
    footer_l = Label( adStock, text= "Developed by Anik" , font= "times 10 bold", bg= "black", fg="white")
    footer_l.place(x= 500, y =700)
    try:
        c.execute("SELECT company_name FROM company_table ORDER BY company_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_C_l = Label(adStock,text="Company name:", font= "times 12 bold")
        ddl_C_l.place(x=100, y=100)
        ddl_C_e = ttk.Combobox(adStock,width=25 ,font="times 12 bold",state='readonly')
        ddl_C_e['values'] = lst_c
        ddl_C_e.place(x=300,y=100)
        ddl_C_e.set("Choose Company")

        c.execute("SELECT medicine_name FROM medicine_table ORDER BY medicine_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_M_l = Label(adStock, text ="Medicine Name:",  font="times 12 bold")
        ddl_M_l.place(x=100, y= 150)
        ddl_M_e = ttk.Combobox(adStock,width=25 ,font="times 12 bold",state='readonly')
        ddl_M_e['values'] = lst_c
        ddl_M_e.place(x=300,y=150)
        ddl_M_e.set("Choose Medicine")
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong!7", parent= adStock)

    stock_l = Label(adStock, text ="Stock:", font ="times 12 bold")
    stock_l.place(x=100,y=200)
    stock_E = Entry(adStock, width= 27, font="times 12 bold")
    stock_E.place(x=300,y=200)

    cp_l = Label(adStock, text ="Cost per unit:", font="times 12 bold")
    cp_l.place(x=100, y=250)
    cp_e =Entry(adStock,width=27, font="times 12 bold")
    cp_e.place(x=300,y=250)

    sp_l = Label(adStock, text ="Sell per unit:", font="times 12 bold")
    sp_l.place(x=100, y=300)
    sp_e =Entry(adStock,width=27, font="times 12 bold")
    sp_e.place(x=300,y=300)

    vendor_l = Label(adStock, text ="Vendor Name:", font="times 12 bold")
    vendor_l.place(x=100, y=350)
    vendor_e =Entry(adStock,width=27, font="times 12 bold")
    vendor_e.place(x=300,y=350)

    vendorC_l = Label(adStock, text ="Vendor Contact:", font="times 12 bold")
    vendorC_l.place(x=100, y=400)
    vendorC_e =Entry(adStock,width=27, font="times 12 bold")
    vendorC_e.place(x=300,y=400)

    shelf_l = Label(adStock, text = "Shelf:" , font= "times 12 bold")
    shelf_l.place(x=100, y =450)
    shelf_e = Entry(adStock, width =27, font="times 12 bold")
    shelf_e.place(x=300, y= 450)

    btn_add = Button(adStock, text="Add to database", width =15, font="times 8 bold", bg="darkcyan", fg="black", command=get_items)
    btn_add.place(x=450, y= 500)
    btn_clear = Button(adStock, text="Clear", width =15, font="times 8 bold", bg="darkcyan", fg="black", command= clear_all)
    btn_clear.place(x=320, y= 500)

    tbox = Text(adStock, width=45, height=23)
    tbox.place(x= 700, y = 100)
    tbox.insert(END, str(id)+" types of medicines added so far\n\n These products(total "+str(warnStockLen)+ ") has less than ten in stock :\n"+ warnStock)
    tbox.config(state=DISABLED)
    adStock.bind("<Return>",get_items)
    adStock.mainloop()

def updateItem():
    upStock = Tk()
    width_of_window = 1300
    height_of_window =750
    screen_width =upStock.winfo_screenwidth()
    screen_height = upStock.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    upStock.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    upStock.title("Update medicine in stock")
    upStock.iconbitmap('plus.ico')
    header = Frame(upStock, bg='darkcyan')
    footer = Frame(upStock, bg='black')
    upStock.columnconfigure(0, weight=1) # 100%
    upStock.rowconfigure(3, weight=1) # 10%
    upStock.rowconfigure(5,weight=8)
    upStock.rowconfigure(9,weight=1)
    footer.grid(row=9,sticky="snew")
    header.grid(row=3,sticky="snew")
    upStock.call('wm', 'attributes', '.', '-topmost', True)
    upStock.after_idle(upStock.call, 'wm', 'attributes', '.', '-topmost', False)
    upStock.focus_force()
    def clear_all():
        ddl_C_e.set("Choose Company")
        ddl_M_e.set("Choose Medicine")
        stock_E.delete(0,END)
        cp_e.delete(0,END)
        sp_e.delete(0,END)
        vendor_e.delete(0,END)
        vendorC_e.delete(0,END)
        shelf_e.delete(0,END)
    def search(ddl_C_e,ddl_M_e):
        C = ddl_C_e.get()
        M = ddl_M_e.get()
        stock_E.delete(0,END)
        cp_e.delete(0,END)
        sp_e.delete(0,END)
        vendor_e.delete(0,END)
        vendorC_e.delete(0,END)
        shelf_e.delete(0,END)
        try:
            sqlCheck ="""
            SELECT COUNT(medicine_name) FROM inventory
            WHERE company_name =? AND medicine_name =?
            """
            c.execute(sqlCheck,[C,M])
            count = c.fetchone()[0]
            conn.commit()
            if count > 0:
                sql ="""
                SELECT * FROM inventory
                WHERE company_name =? AND medicine_name =?
                """
                result = c.execute(sql,[C,M])

                for r in result:
                    item1 = r[1]
                    item2 = r[2]
                    item3 = r[3]
                    item4 = r[4]
                    item5 = r[5]
                    item6 = r[6]
                    item7 = r[7]
                    item8 = r[8]
                conn.commit()

                ddl_M_e.insert(0,str(r[1]))
                ddl_C_e.insert(0,str(r[2]))
                stock_E.insert(0,str(r[3]))
                cp_e.insert(0,str(r[4]))
                sp_e.insert(0,str(r[5]))
                vendor_e.insert(0,str(r[6]))
                vendorC_e.insert(0,str(r[7]))
                shelf_e.insert(0,str(r[8]))
            else:
                tkinter.messagebox.showinfo("Information","0 in stock", parent = upStock)
        except :
            tkinter.messagebox.showerror("showerror","Ops! Something went wrong8", parent= upStock)

    def update(ddl_C,ddl_M):
        C = ddl_C_e.get()
        M = ddl_M_e.get()
        stock = stock_E.get()
        cp = cp_e.get()
        sp = sp_e.get()
        vendor = vendor_e.get()
        vendorC = vendorC_e.get()
        shelf = shelf_e.get()
        try:
            update_sql="""
            UPDATE inventory
            SET stock=?,
                cost_per_unit=?,
                sell_per_unit=?,
                buy_from=?,
                buy_from_contact=?,
                shelf = ?
            WHERE
                medicine_name=? AND company_name =?

                """
            c.execute(update_sql,[stock,cp,sp,vendor,vendorC,shelf,M,C])
            conn.commit()
            tkinter.messagebox.showinfo("Information","Successfully Updated", parent=upStock)
            clear_all()
        except :
            tkinter.messagebox.showerror("showerror","Ops! Something went wrong99!", parent=upStock)




    header_l = Label( upStock, text= "Feni Medical Hall" , font= "times 25 bold", bg= "darkcyan")
    header_l.place(x= 500, y =10)
    address_l = Label( upStock, text= "677, East Dholaipar Bajar, Dania Road, Dhaka-1362" , font= "times 10 bold", bg= "darkcyan")
    address_l.place(x= 485, y =50)
    footer_l = Label( upStock, text= "Developed by Anik" , font= "times 10 bold", bg= "black", fg="white")
    footer_l.place(x= 500, y =700)
    try:
        c.execute("SELECT company_name FROM company_table ORDER BY company_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_C_l = Label(upStock,text="Company name:", font= "times 12 bold")
        ddl_C_l.place(x=100, y=100)
        ddl_C_e = ttk.Combobox(upStock,width=25 ,font="times 12 bold",state='readonly')
        ddl_C_e['values'] = lst_c
        ddl_C_e.place(x=300,y=100)
        ddl_C_e.set("Choose Company")

        c.execute("SELECT medicine_name FROM medicine_table ORDER BY medicine_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_M_l = Label(upStock, text ="Medicine Name:",  font="times 12 bold")
        ddl_M_l.place(x=100, y= 150)
        ddl_M_e = ttk.Combobox(upStock,width=25 ,font="times 12 bold",state='readonly')
        ddl_M_e['values'] = lst_c
        ddl_M_e.place(x=300,y=150)
        ddl_M_e.set("Choose Medicine")
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong9!", parent= upStock)

    btn_search = Button(upStock, text="search", font="times 12 bold", bg="darkcyan", fg="black", command = lambda:search(ddl_C_e,ddl_M_e))
    btn_search.place(x =550, y = 150)

    stock_l = Label(upStock, text ="Stock:", font ="times 12 bold")
    stock_l.place(x=100,y=200)
    stock_E = Entry(upStock, width= 27, font="times 12 bold")
    stock_E.place(x=300,y=200)

    cp_l = Label(upStock, text ="Cost per unit:", font="times 12 bold")
    cp_l.place(x=100, y=250)
    cp_e =Entry(upStock,width=27, font="times 12 bold")
    cp_e.place(x=300,y=250)

    sp_l = Label(upStock, text ="Sell per unit:", font="times 12 bold")
    sp_l.place(x=100, y=300)
    sp_e =Entry(upStock,width=27, font="times 12 bold")
    sp_e.place(x=300,y=300)

    vendor_l = Label(upStock, text ="Vendor Name:", font="times 12 bold")
    vendor_l.place(x=100, y=350)
    vendor_e =Entry(upStock,width=27, font="times 12 bold")
    vendor_e.place(x=300,y=350)

    vendorC_l = Label(upStock, text ="Vendor Contact:", font="times 12 bold")
    vendorC_l.place(x=100, y=400)
    vendorC_e =Entry(upStock,width=27, font="times 12 bold")
    vendorC_e.place(x=300,y=400)

    shelf_l = Label(upStock, text = "Shelf:" , font= "times 12 bold")
    shelf_l.place(x=100, y =450)
    shelf_e = Entry(upStock, width =27, font="times 12 bold")
    shelf_e.place(x=300, y= 450)
    btn_add = Button(upStock, text="Edit in database", width =15, font="times 8 bold", bg="darkcyan", fg="black", command= lambda : update(ddl_C_e,ddl_M_e))
    btn_add.place(x=450, y= 500)
    btn_clear = Button(upStock, text="Clear", width =15, font="times 8 bold", bg="darkcyan", fg="black", command= clear_all)
    btn_clear.place(x=320, y= 500)

    upStock.bind("<Return>", lambda *args, ddl_C_e =ddl_C_e, ddl_M_e=ddl_M_e : update(ddl_C_e,ddl_M_e))

    upStock.mainloop()

def delete_stock():
    delStock = Tk()
    width_of_window=496
    height_of_window = 205
    screen_width =delStock.winfo_screenwidth()
    screen_height = delStock.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    delStock.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    delStock.title("Delete Medicine from stock")
    delStock.iconbitmap('plus.ico')
    title_label=Label(delStock, text="Delete Medicine Information Here!!", font="times 12 bold", fg="darkcyan")
    title_label.place(x=160,y=10)
    def clear_all():
        ddl_C_e.set("Choose Company")
        ddl_M_e.set("Choose Medicine")
    def delete(ddl_C,ddl_M):
        C = ddl_C.get()
        M = ddl_M.get()
        try:
            sql ="""
            DELETE FROM inventory
            WHERE medicine_name =? AND company_name =?
            """
            sqlCheck ="""
            SELECT COUNT(medicine_name) FROM inventory
            WHERE company_name =? AND medicine_name =?
            """
            c.execute(sqlCheck,[C,M])
            count = c.fetchone()[0]
            conn.commit()
            if count > 0:
                c.execute(sql,[M,C])
                conn.commit()
                tkinter.messagebox.showinfo("showinfo","Successfully deleted!", parent= delStock)
                clear_all()
            else:
                tkinter.messagebox.showinfo("showinfo","0 in stock!", parent= delStock)
        except :
            tkinter.messagebox.showerror("showerror","Ops! Something went wrong10!", parent= delStock)

    try:
        c.execute("SELECT company_name FROM company_table ORDER BY company_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_C_e = ttk.Combobox(delStock,width=25 ,font="times 12 bold",state='readonly')
        ddl_C_e['values'] = lst_c
        ddl_C_e.place(x=100,y=50)
        ddl_C_e.set("Choose Company")
        c.execute("SELECT medicine_name FROM medicine_table ORDER BY medicine_name")
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_M_e = ttk.Combobox(delStock,width=25 ,font="times 12 bold",state='readonly')
        ddl_M_e['values'] = lst_c
        ddl_M_e.place(x=100,y=100)
        ddl_M_e.set("Choose Medicine")
    except :
        tkinter.messagebox.showerror("showerror","Ops! Something went wrong11!", parent= delStock)
    btn_delete = Button(delStock, text="Delete", bg="orange" ,fg="black", font="times 12 bold", command= lambda : delete(ddl_C_e, ddl_M_e))
    btn_delete.place(x= 270, y= 130)
    delStock.bind("<Return>", lambda *args, ddl_C_e=ddl_C_e, ddl_M_e= ddl_M_e: delete(ddl_C_e,ddl_M_e) )
    delStock.mainloop()


def check_if_number(text):
    try:
        int(text)
        return 1
    except  ValueError:
        return 0
def check_if_float(text):
    try:
        float(text)
        return 1
    except ValueError:
        return 0
