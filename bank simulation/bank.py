#!/usr/bin/env python
# coding: utf-8

# In[9]:


from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from tkinter.ttk import Style,Treeview
from datetime import datetime


# In[31]:


win=Tk()
win.state("zoomed")
win.configure(bg="powder blue")
win.resizable(width=False,height=False)

title=Label(win,text="Bank Account Automation",font=('Arial',60,'bold','underline'),bg='powder blue')
title.pack()


def home_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(x=0,y=120,relwidth=1,relheight=.9)

    def fp():
        frm.destroy()
        forgot_pass_screen()
    
    def new():
        frm.destroy()
        open_account_screen()
    
    def login():
        a=e_acn.get()
        p=e_pass.get()
        if(len(a)==0 or len(p)==0):
            messagebox.showwarning("Validation","Plz fill both field")
            return
        elif(not a.isdigit()):
            messagebox.showwarning("Validation","Acc No must be in digit")
            return
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from account where acc_no=? and pass=?",(a,p))
            global row
            row=cur.fetchone()
            if(row==None):
                messagebox.showerror("Invalid","Invalid ACN/PASS")
            else:
                row=list(row)
                frm.destroy()
                welcome_screen()
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
    
    lbl_acn=Label(frm,text="Acc No",font=('Arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.42,rely=.1)
    e_acn.focus()
    
    lbl_pass=Label(frm,text="Password",font=('Arial',20,'bold'),bg='pink')
    lbl_pass.place(relx=.3,rely=.25)

    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.42,rely=.25)
    
    btn_login=Button(frm,text="login",font=('Arial',20,'bold'),bd=5,command=login)
    btn_login.place(relx=.45,rely=.4)
    
    btn_reset=Button(frm,text="reset",font=('Arial',20,'bold'),bd=5,command=reset)
    btn_reset.place(relx=.55,rely=.4)
    
    btn_fp=Button(frm,text="forgot password",font=('Arial',20,'bold'),bd=5,width=16,command=fp)
    btn_fp.place(relx=.43,rely=.55)
    
    btn_new=Button(frm,text="open new account",font=('Arial',20,'bold'),bd=5,width=19,command=new)
    btn_new.place(relx=.41,rely=.7)
    

def forgot_pass_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(x=0,y=120,relwidth=1,relheight=.9)
    
    def back():
        frm.destroy()
        home_screen()
    
    def get():
        acn=e_acn.get()
        mob=e_mob.get()
        email=e_email.get()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select pass from account where acc_no=? and email=? and mob=?",(acn,email,mob))
        pwd=cur.fetchone()
        if(pwd==None):
            messagebox.showerror("invalid","Invalid details")
        else:
            messagebox.showinfo("Password",f"Your Pass:{pwd[0]}")
    
    btn_back=Button(frm,text="back",font=('Arial',20,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)
    
    lbl_acn=Label(frm,text="Acc No",font=('Arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.42,rely=.1)
    e_acn.focus()
    
    lbl_mob=Label(frm,text="Mob",font=('Arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.25)

    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.42,rely=.25)
    
    lbl_email=Label(frm,text="Email",font=('Arial',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.4)

    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.42,rely=.4)
    

    btn_get=Button(frm,text="get password",font=('Arial',20,'bold'),bd=5,command=get)
    btn_get.place(relx=.4,rely=.55)
 

def open_account_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(x=0,y=120,relwidth=1,relheight=.9)
    
    def back():
        frm.destroy()
        home_screen()
  
    def create():
        name=e_name.get()
        mob=e_mob.get()
        email=e_email.get()
        pwd=e_pass.get()
        bal=1000
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into account(name,mob,email,pass,bal) values(?,?,?,?,?)",(name,mob,email,pwd,bal))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(acc_no) from account")
        tup=cur.fetchone()
        con.close()
        messagebox.showinfo("Success",f"Your Account opend with ACN:{tup[0]}")
        e_name.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_pass.delete(0,"end")
        e_name.focus()
        return
    
    btn_back=Button(frm,text="back",font=('Arial',20,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)
    
    lbl_name=Label(frm,text="Name",font=('Arial',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)

    e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_name.place(relx=.42,rely=.1)
    e_name.focus()
    
    lbl_mob=Label(frm,text="Mob",font=('Arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.25)

    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.42,rely=.25)
    
    lbl_email=Label(frm,text="Email",font=('Arial',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.4)

    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.42,rely=.4)
    
    lbl_pass=Label(frm,text="Password",font=('Arial',20,'bold'),bg='pink')
    lbl_pass.place(relx=.3,rely=.55)

    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.42,rely=.55)
    

    btn_get=Button(frm,text="create account",font=('Arial',20,'bold'),bd=5,command=create)
    btn_get.place(relx=.4,rely=.7)


def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(x=0,y=120,relwidth=1,relheight=.9)
    
    def logout():
        frm.destroy()
        home_screen()
    
    def check():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.1,relwidth=.6,relheight=.7)
        
        l=Label(ifrm,text="This is detail Screen",fg='green',font=('Arial',30,'bold','underline'),bg='pink')
        l.pack()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select * from account where acc_no=?",(row[0],))
        tup=cur.fetchone()
        
        tv=Treeview(ifrm)
        tv.place(x=100,y=100,height=70,width=700)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial',10,'bold'),foreground='brown')


        tv['columns']=('ACN','Name','Email','Mob','Password','Bal')
        
        tv.column('ACN',width=100,anchor='c')
        tv.column('Name',width=100,anchor='c')
        tv.column('Email',width=100,anchor='c')
        tv.column('Mob',width=100,anchor='c')
        tv.column('Password',width=100,anchor='c')
        tv.column('Bal',width=100,anchor='c')
      
        tv.heading('ACN',text='ACN')
        tv.heading('Name',text='Name')
        tv.heading('Email',text='Email')
        tv.heading('Mob',text='Mob')
        tv.heading('Password',text='Password')
        tv.heading('Bal',text='Bal')
        
        tv['show']='headings'
        
        tv.insert("","end",values=(tup[0],tup[1],tup[3],tup[2],tup[4],tup[5]))
     
    def deposit():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.1,relwidth=.6,relheight=.7)
        
        def deposit_txn():
            amt=float(e_amt.get())
            dt=datetime.now()
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("insert into txn values(?,?,?,?)",(row[0],amt,'Cr.',dt))
            cur.execute("update account set bal=bal+? where acc_no=?",(amt,row[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Success",f"{amt} Amount deposited")
            e_amt.delete(0,"end")
            return
            
        l=Label(ifrm,text="This is Deposit Screen",fg='green',font=('Arial',30,'bold','underline'),bg='pink')
        l.pack()
        
        lbl_amt=Label(ifrm,text="Enter Amount",font=('Arial',20,'bold'),bg='pink')
        lbl_amt.place(relx=.1,rely=.3)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.3)
    
        btn_sub=Button(ifrm,text="submit",font=('Arial',20,'bold'),bd=5,command=deposit_txn)
        btn_sub.place(relx=.3,rely=.5)
    
    def withdraw():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.1,relwidth=.6,relheight=.7)
        
        def withdraw_txn():
            amt=float(e_amt.get())
            dt=datetime.now()
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select bal from account where acc_no=?",(row[0],))
            bal=cur.fetchone()
            con.close()
            if(bal[0]>amt):
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?)",(row[0],amt,'Db.',dt))
                cur.execute("update account set bal=bal-? where acc_no=?",(amt,row[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Success",f"{amt} Amount withdrawn")
                e_amt.delete(0,"end")
                return
            else:
                messagebox.showerror("Error","Insufficient Bal")
                return
        
        l=Label(ifrm,text="This is Withdraw Screen",fg='green',font=('Arial',30,'bold','underline'),bg='pink')
        l.pack()
        
        lbl_amt=Label(ifrm,text="Enter Amount",font=('Arial',20,'bold'),bg='pink')
        lbl_amt.place(relx=.1,rely=.3)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.3)
    
        btn_sub=Button(ifrm,text="submit",font=('Arial',20,'bold'),bd=5,command=withdraw_txn)
        btn_sub.place(relx=.3,rely=.5)
    
    def transfer():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.1,relwidth=.6,relheight=.7)
        
        def transfer_txn():
            amt=float(e_amt.get())
            to=int(e_to.get())
            dt=datetime.now()
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from account where acc_no=?",(to,))
            tup=cur.fetchone()
            con.close()
            if(tup==None):
                messagebox.showerror("Invalid","To account does not exist")
                return
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select bal from account where acc_no=?",(row[0],))
                bal=cur.fetchone()
                con.close()
                if(bal[0]>amt):
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?)",(row[0],amt,'Db.',dt))
                    cur.execute("insert into txn values(?,?,?,?)",(to,amt,'Cr.',dt))
                    cur.execute("update account set bal=bal-? where acc_no=?",(amt,row[0]))
                    cur.execute("update account set bal=bal+? where acc_no=?",(amt,to))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success",f"{amt} transfered successfully")
                    e_amt.delete(0,"end")
                    return
                else:
                    messagebox.showerror("Error","Insufficient Bal")
                    return

        
        
        l=Label(ifrm,text="This is Transfer Screen",fg='green',font=('Arial',30,'bold','underline'),bg='pink')
        l.pack()
        
        lbl_to=Label(ifrm,text="To ACN",font=('Arial',20,'bold'),bg='pink')
        lbl_to.place(relx=.1,rely=.3)
        
        e_to=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.3)
        
        lbl_amt=Label(ifrm,text="Enter Amount",font=('Arial',20,'bold'),bg='pink')
        lbl_amt.place(relx=.1,rely=.45)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.45)
        
    
        btn_sub=Button(ifrm,text="submit",font=('Arial',20,'bold'),bd=5,command=transfer_txn)
        btn_sub.place(relx=.3,rely=.6)
    
    
    def update_profile():
        frm=Frame(win)
        frm.configure(bg="pink")
        frm.place(relx=.2,rely=.2,relwidth=.6,relheight=.7)
  
        def update():
            name=e_name.get()
            mob=e_mob.get()
            email=e_email.get()
            pwd=e_pass.get()
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update account set name=?,mob=?,email=?,pass=? where acc_no=?",(name,mob,email,pwd,row[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Update","Profile Updated")
            row[1]=name
            frm.destroy()
            welcome_screen()
                    
        lbl_name=Label(frm,text="Name",font=('Arial',20,'bold'),bg='pink')
        lbl_name.place(relx=.3,rely=.1)

        e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
        e_name.place(relx=.42,rely=.1)
        e_name.focus()
        e_name.insert(0,row[1])

        lbl_mob=Label(frm,text="Mob",font=('Arial',20,'bold'),bg='pink')
        lbl_mob.place(relx=.3,rely=.25)

        e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
        e_mob.place(relx=.42,rely=.25)
        e_mob.insert(0,row[2])
        
        lbl_email=Label(frm,text="Email",font=('Arial',20,'bold'),bg='pink')
        lbl_email.place(relx=.3,rely=.4)

        e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
        e_email.place(relx=.42,rely=.4)
        e_email.insert(0,row[3])
        
        lbl_pass=Label(frm,text="Pass",font=('Arial',20,'bold'),bg='pink')
        lbl_pass.place(relx=.3,rely=.55)

        e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5)
        e_pass.place(relx=.42,rely=.55)
        e_pass.insert(0,row[4])

        btn_get=Button(frm,text="update",font=('Arial',20,'bold'),bd=5,command=update)
        btn_get.place(relx=.4,rely=.7)

    
    
    
    btn_logout=Button(frm,text="logout",font=('Arial',20,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.9,rely=0)
    
    lbl_wel=Label(frm,text=f"Welcome,{row[1]}",font=('Arial',20,'bold'),bg='pink')
    lbl_wel.place(relx=.0001,rely=0)
    
    btn_bal=Button(frm,text="check balance",font=('Arial',20,'bold'),bd=5,width=12,command=check)
    btn_bal.place(relx=.001,rely=.1)
    
    btn_dep=Button(frm,text="deposit",font=('Arial',20,'bold'),bd=5,width=12,command=deposit)
    btn_dep.place(relx=.001,rely=.25)
    
    btn_wd=Button(frm,text="withdraw",font=('Arial',20,'bold'),bd=5,width=12,command=withdraw)
    btn_wd.place(relx=.001,rely=.4)
    
    btn_tr=Button(frm,text="transfer",font=('Arial',20,'bold'),bd=5,width=12,command=transfer)
    btn_tr.place(relx=.001,rely=.55)
    
    btn_update=Button(frm,text="update",font=('Arial',20,'bold'),bd=5,width=12,command=update_profile)
    btn_update.place(relx=.001,rely=.7)
    
home_screen()
win.mainloop()


# In[8]:


con=sqlite3.connect(database="bank.sqlite")
cur=con.cursor()
#cur.execute("create table account(acc_no integer primary key autoincrement,name text,mob text,email text,pass text,bal float)")
#cur.execute("create table txn(acc_no integer,amt float,txn_type text,txn_date date)")
con.commit()
con.close()


# In[ ]:




