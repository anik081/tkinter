from tkinter import *
from tkinter import ttk
import time
import sqlite3
import tkinter.messagebox
import os
import sys
import datetime
import math
import random
import win32api


date = datetime.datetime.now().date()
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
products_list = []
products_list_company =[]
products_price = []
products_quantity =[]
label_list=[]
def main_shop(userName):
    sp = Tk()
    width_of_window=1300
    height_of_window = 600
    screen_width =sp.winfo_screenwidth()
    screen_height = sp.winfo_screenheight()
    x = (screen_width/2) - (width_of_window/2)
    y = (screen_height/2) - (height_of_window/2)
    sp.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
    sp.title("Feni Medical Hall")
    sp.iconbitmap('plus.ico')







    def ajax(*args):

        ddl = ddl_M_e.get()
        ddl_c = ddl_C_e.get()


        def generate_bill(*args):
            directory ="./invoice/"+str(date)+"/"
            if not os.path.exists(directory):
                os.makedirs(directory)

            company_bill ="Feni Medical Hall\n"
            address_bill ="677, East Dholaipar Bajar,\nDania Road, Dhaka-1362\n"
            phone_bill="01818591440\n"
            sample_bill="Invoice\n"
            dt="Date: "+str(date)
            openHours ="\nOpen 24 hours\n"
            soldMed = "Sold medicine is not refundable!\n"
            user = "receipt creator: "+userName+"\n"

            table_header="\n=====================\nSN.  Name  Qty Tk\n---------------------\n"
            final = company_bill+address_bill+phone_bill+sample_bill+dt+openHours+soldMed+user+"\n"+table_header
            fileName = str(directory)+str(random.randrange(5000,100000))+".doc"
            f = open(fileName, "w")
            f.write(final)
            r = 1
            i=0
            for t in products_list:
                f.write("\n"+str(r)+"  "+str(products_list[i]+"..............")[:7]+"  "+str(products_quantity[i])+"  "+str("{:.2f}".format(products_price[i])))
                r=r+1
                i=i+1
            f.write("\n\n\tTotal: Tk. "+str(sum(products_price)))
            f.write("\n\n\tThank you")
            # os.startfile(fileName,"print")
            f.close()


            try:

                x=0
                for i in products_list:
                    ol_s = "SELECT medicine_name,company_name,stock FROM inventory WHERE medicine_name=?  AND company_name=?"
                    result_s = c.execute(ol_s,[products_list[x],products_list_company[x]])
                    conn.commit()
                    for r in result_s:
                        stock = r[2]
                    new_stock = int(stock) - int(products_quantity[x])
                    sql ="UPDATE inventory SET stock =? WHERE medicine_name=? AND company_name =?"
                    c.execute(sql,[new_stock,products_list[x],products_list_company[x]])
                    conn.commit()

                    sql2 ="INSERT INTO transactions (medicine_name, company_name,quantity,amount,date) VALUES (?,?,?,?,?)"
                    c.execute(sql2,[products_list[x],products_list_company[x],products_price[x],products_quantity[x],date])
                    conn.commit()
                    x=x+1
                for r in label_list:
                    r.destroy()
                del(products_list[:])
                del(products_list_company[:])
                del(products_quantity[:])
                del(products_price[:])
                total_l.configure(text="Total: ")
                change_e.delete(0,END)
                c_amount.configure(text="")
                tkinter.messagebox.showinfo("Information","Transactions Done!", parent=sp)
            except :
                tkinter.messagebox.showerror("showerror","Ops! Something went wrong!", parent=sp)
        def change_func():
            try:
                amount_given = float(change_e.get())
                our_total = float(sum(products_price))
            except ValueError:
                amount_given =0
                our_total = float(sum(products_price))
            to_give = amount_given - our_total
            c_amount.configure(text="Change: TK. "+str(to_give))


        def add_to_cart(*args):


            try:
                sql_quantity = "SELECT stock FROM inventory WHERE medicine_name=? AND company_name=?"
                c.execute(sql_quantity,[ddl,ddl_c])
                result = c.fetchone()[0]
                conn.commit()
                if int(quantity_e.get()) > int(result):
                    tkinter.messagebox.showinfo("Information","Not enough medicine in inventory", parent=sp)
                else:
                    final_price = float(quantity_e.get()) * float(price) -float(discount_e.get())
                    products_list.append(med)
                    products_price.append(final_price)
                    products_quantity.append(quantity_e.get())
                    products_list_company.append(com)

                    x_index = 0
                    y_index = 100
                    counter = 0
                    for p in products_list:
                        tempName = Label(right, text=str(products_list[counter]) , font= "times 12 bold" , bg="darkcyan", fg="white")
                        tempName.place(x=0, y= y_index)
                        label_list.append(tempName)
                        tempQt = Label(right, text=str(products_quantity[counter]) , font= "times 12 bold" , bg="darkcyan", fg="white")
                        tempQt.place(x=200, y= y_index)
                        label_list.append(tempQt)
                        tempPrice = Label(right, text=str(products_price[counter]) , font= "times 12 bold" , bg="darkcyan", fg="white")
                        tempPrice.place(x=400, y= y_index)
                        label_list.append(tempPrice)

                        y_index += 40
                        counter += 1

                        total_l.configure(text="Total: "+str(sum(products_price)))
                        quantity_l.place_forget()
                        quantity_e.place_forget()
                        discount_l.place_forget()
                        discount_e.place_forget()
                        add_btn.destroy()
                        ddl_C_e.set("Choose Company")
                        ddl_M_e.set("Choose Medicine")
                        medicine_l.configure(text="")
                        company_l.configure(text="")
                        price_l.configure(text="")
                        stock_l.configure(text="")
                        shelf_l.configure(text="")
                    def clearList(*args):
                        for r in label_list:
                            r.destroy()
                        del(products_list[:])
                        del(products_list_company[:])
                        del(products_quantity[:])
                        del(products_price[:])
                        tempName.configure(text="")
                        tempQt.configure(text="")
                        tempPrice.configure(text="")
                        total_l.configure(text="Total: ")

                    clear_l = Button(right, text="Clear", font="times 18 bold", bg= "orange" , fg ="white", command=clearList)
                    clear_l.place(x=400, y= 500)



            except :
                tkinter.messagebox.showerror("showerror","Ops! Something went wrong!", parent=sp)


        query_check  = "SELECT COUNT(*) FROM inventory WHERE medicine_name=?  AND company_name=?"
        c.execute(query_check,[ddl,ddl_c])
        conn.commit()
        count = c.fetchone()[0]
        if count > 0:
            query = "SELECT medicine_name,company_name,sell_per_unit,stock,shelf FROM inventory WHERE medicine_name=?  AND company_name=?"
            result = c.execute(query,[ddl,ddl_c])
            conn.commit()
            for r in result:
                med = r[0]
                com=r[1]
                price=r[2]
                stock = r[3]
                shelf = r[4]
            medicine_l.configure(text="Medicine Name: "+str(med))
            company_l.configure(text="Company Name: "+str(com))
            price_l.configure(text="Price: "+str(price))
            stock_l.configure(text="Stock: "+str(stock))
            shelf_l.configure(text="Shelf: "+str(shelf))

            quantity_l = Label(left, text="Enter Quantity: ", font="times 18 bold", bg= "white")
            quantity_l.place(x= 20, y =400)
            quantity_e = Entry(left, width= 10, font="times 18 bold", bg="darkcyan")
            quantity_e.place(x= 200, y =400)
            quantity_e.focus()
            discount_l = Label(left, text="Enter Discount: ", font="times 18 bold", bg= "white")
            discount_l.place(x= 20, y =440)
            discount_e = Entry(left, width= 10, font="times 18 bold", bg="darkcyan")
            discount_e.place(x= 200, y =440)
            discount_e.insert(END,0)
            c_amount = Label(left, text="",font="times 12 bold", fg="red", bg="white")
            c_amount.place(x= 200, y =573)


            add_btn = Button(left, text="Add to Cart", width="10", height =1, bg="darkcyan" ,font="times 12 bold", command= add_to_cart)
            add_btn.place(x=220, y= 480)

            change_l = Label(left, text="Given Amount: ", font="times 18 bold", bg= "white")
            change_l.place(x= 20, y =530)
            change_e = Entry(left, width= 10, font="times 18 bold", bg="darkcyan")
            change_e.place(x= 200, y =530)

            change_btn = Button(left, text="Calculate Change", font="times 12 bold", width=15, bg="orange", command=change_func)
            change_btn.place(x=350, y= 530)
            bill_btn = Button(left, text="Generate Bill", font="times 12 bold", width=15, bg="red", command=generate_bill)
            bill_btn.place(x=550, y= 530)


            sp.bind("<Up>",add_to_cart)
            sp.bind("<space>",generate_bill)


        else:
            medicine_l.configure(text="No medicine in inventory")
            company_l.configure(text="")
            price_l.configure(text="")
            stock_l.configure(text="")
            shelf_l.configure(text="")

    left = Frame(sp, width =750, height= 600, bg="white")
    left.pack(side= LEFT)

    right = Frame(sp, width =550, height= 600, bg="darkcyan")
    right.pack(side= RIGHT)
    title_label=Label(left, text="Feni Medical Hall", font="times 26 bold", fg="darkcyan", bg= "white")
    title_label.place(x=290,y=10)

    date_l = Label(right, text="Today's date: "+ str(date), font ="times 12 bold" , bg= "darkcyan" , fg="white")
    date_l.place(x=0,y=0)

    #table invoice
    tproduct = Label(right, text="Products", font="times 18 bold", bg= "darkcyan" , fg ="white")
    tproduct.place(x=0, y= 50)
    tquantity = Label(right, text="Quantity", font="times 18 bold", bg= "darkcyan" , fg ="white")
    tquantity.place(x=200, y= 50)
    tprice = Label(right, text="Amount", font="times 18 bold", bg= "darkcyan" , fg ="white")
    tprice.place(x=400, y= 50)
    total_l = Label(right, text="Total", font="times 18 bold", bg= "darkcyan" , fg ="white")
    total_l.place(x=0, y= 500)


    c.execute("SELECT company_name FROM company_table ORDER BY company_name")
    conn.commit()
    lst =c.fetchall()
    i=0
    lst_c=[]
    tot = len(lst)
    for r in range(i,tot):
        lst_c.append(" ".join(str(x) for x in lst[i]))
        i+=1
    ddl_C_e = ttk.Combobox(left,width=25 ,font="times 12 bold",state='readonly')
    ddl_C_e['values'] = lst_c
    ddl_C_e.place(x=20,y=80)
    ddl_C_e.set("Choose Company")
    com = ddl_C_e.get()
    def getComForSrc():
        com = ddl_C_e.get()
        c.execute("SELECT medicine_name FROM inventory WHERE company_name=? ORDER BY medicine_name",[com])
        conn.commit()
        lst =c.fetchall()
        i=0
        lst_c=[]
        tot = len(lst)
        for r in range(i,tot):
            lst_c.append(" ".join(str(x) for x in lst[i]))
            i+=1
        ddl_M_e['values'] = lst_c


    btn_com = Button(left, width=5, font="times 12 bold", text="Go", command= getComForSrc)
    btn_com.place(x=280,y=80)


    ddl_M_e = ttk.Combobox(left,width=25 ,font="times 12 bold",state='readonly')

    ddl_M_e.place(x=20,y=130)
    ddl_M_e.set("Choose Medicine")



    search_btn = Button(left, text="search", width="10", height =1, bg="darkcyan" ,font="times 12 bold", command=ajax)
    search_btn.place(x=250, y= 130)
    medicine_l = Label(left, text="", font="times 18 bold", bg="white", fg="darkcyan")
    medicine_l.place(x=0, y= 180)
    company_l = Label(left, text="", font="times 18 bold", bg="white", fg="darkcyan")
    company_l.place(x=0, y= 210)
    price_l = Label(left, text="", font="times 18 bold", bg="white", fg="darkcyan")
    price_l.place(x=0, y= 240)
    stock_l = Label(left, text="", font="times 18 bold", bg="white", fg="darkcyan")
    stock_l.place(x=0, y= 270)
    shelf_l = Label(left, text="", font="times 18 bold", bg="white", fg="darkcyan")
    shelf_l.place(x=0, y= 300)
    userLabel = Label(left, text="User: "+userName, font="times 12 bold", bg="orange", fg="black")
    userLabel.place(x=17,y=50)
    adminAreaBtn = Button(left, text="Admin Area", font="times 12 bold", bg="darkcyan", fg="black", command=goToAdminArea)
    adminAreaBtn.place(x=17,y=0)
    sp.bind("<Return>", ajax)

    sp.mainloop()

def goToAdminArea():
    import loginAdmin
    loginAdmin.userLogin()
