from tkinter import *
from collections import defaultdict
from PIL import Image
from PIL import ImageTk
import sqlite3
import time
import tkinter.messagebox as tmsg
global nodes


#CONTROLS
def controls():
    db.execute("DELETE FROM FACEBOOK WHERE PASSWORD = '1726351'")

#CORE DATABASE
def debug():
    crsr = db.execute("SELECT * FROM FACEBOOK")
    c=0
    print("\n")
    print("FACEBOOK HEADQUARTERS DATABASE 2019")
    for row in crsr :
        if(c==0):
            print("USERNAME       ", "PASSWORD      ")
            print("------------------------------------")
        print(row[0],"    ",row[1])
        c+=1
    print(c, "People are registered into your website")

#MAIN    
db = sqlite3.connect("fbdb.db")
db.execute("CREATE TABLE IF NOT EXISTS FACEBOOK(USERNAME CHAR[30], PASSWORD CHAR[30])")
db.commit()
crsr = db.execute("SELECT * FROM FACEBOOK")
db.commit()

global fb
fb = Tk()
fb.geometry("360x850")
fb.wm_iconbitmap("fb.ico")
fb.title("Facebook - Welcome to Facebook!")
Label(text = "Welcome To Facebook! Login or Signup",font=("Calibri",15,"bold")).pack()


def myAccount():
    global mypage
    global d
    global myf
    mypage = Toplevel(fb1)
    mypage.wm_iconbitmap("fb.ico")
    mypage.title(f"{u1}")
    mypage.geometry("360x550")

    d = Image.open("de.png")
    d= d.resize((120,75),Image.ANTIALIAS)
    myf = ImageTk.PhotoImage(d)
    Label(mypage, image = myf,anchor="w").pack(fill="both")
    lab = Label(mypage,text = "ONLINE",font=("Calibri",9,"bold"),fg="green")
    lab.place(x=40,y=80)
    Label(mypage,text = f"Welcome {u1}! What's on your mind?",font=("Calibri",14,"bold")).pack(pady="20px")
    
def check():
    fb1.wm_iconbitmap("fb.ico")
    found = 0
    global u1
    global p1
    u1 = user.get()
    p1 = passw.get()
    crsr = db.execute("SELECT * FROM FACEBOOK")
    for row in crsr:
        if(row[0] == u1 and row[1]== p1 ):
            print(f"{u1} is online")
            found=1
            break
    if(found==1):
        myAccount()
    if(found==0):
        status=Label(fb1,text = "Username or Password Incorrect! Try Again",fg="red")
        status.pack()
        status.after(1200,lambda : status.destroy())
    userlogin.delete(0,END)
    passwordlogin.delete(0,END)


def signin():
    global fb1
    fb1=Toplevel(fb)
    fb1.title("Login Page")
    fb1.geometry("300x250")
    fb1.wm_iconbitmap("fb.ico")
    global user
    global passw
    global userlogin
    global passwordlogin
    user = StringVar()
    passw = StringVar()
    Label(fb1,text = "Username",font=("Calibri",12)).pack(pady="10px")
    userlogin = Entry(fb1,textvariable=user,width="30")
    userlogin.pack(pady="5px")
    Label(fb1,text = "Password",font=("Calibri",12)).pack()
    passwordlogin = Entry(fb1,show="*",textvariable = passw,width="30")
    passwordlogin.pack()
    Button(fb1,text="Login",height="2",width="20",bg = "indigo",fg = "white",command=check).pack(pady="15px")
     
def signup():
    u2 = name.get()
    p2 = password.get()
    user_name.delete(0,END)
    pass_word.delete(0,END)
    found = 0
    crsr = db.execute("SELECT * FROM FACEBOOK")
    for row in crsr:
        if(row[0]==u2):
            status1 = Label(text = "Username Already Exists!",fg="red")
            status1.pack()
            status1.after(2000,lambda : status1.destroy())
            found=1
            break
    if(found==0):
        status0 = Label(text = "Registration Successful!",fg="green")
        status0.pack()
        status0.after(2000,lambda : status0.destroy())
        db.execute("INSERT INTO FACEBOOK(USERNAME, PASSWORD) VALUES(?,?)",(u2, p2))
        db.commit()
    
#Create An Account Label
global name
global password
Label(text = "Create an Account",font=("Calibri",12,"bold")).pack(pady="10px")
name = StringVar()
password = StringVar()


#Register Menu
global user_name
global pass_word

face = Image.open("f.png")
face = face.resize((250,75),Image.ANTIALIAS)
photoImg = ImageTk.PhotoImage(face)
Label(fb, image = photoImg).pack()

Label(text = "Name",font=("Calibri",12)).pack()
user_name = Entry(textvariable=name,width="55")
user_name.pack(pady="5px")
Label(text = "Password",font=("Calibri",12)).pack()
pass_word = Entry(textvariable = password,show="*",width="55")
pass_word.pack()

#Login and Register Buttons
Button(text="Sign-Up",height="2",width="30",bg = "indigo",fg = "white",command=signup).pack(pady="20px")
Button(text="Sign-In",height="2",width="30",bg = "indigo",fg = "white",command=signin).pack(pady="20px")

#DFS
graph = defaultdict(list)
vis = [False]*5
def dfs(x):
    vis[x]=True
    print(x)
    for i in graph[x]:
        if(vis[i]==True):
            continue
        dfs(i)
def addedge(u,v):
    graph[u].append(v)
addedge(1,2)
addedge(1,3)
addedge(2,4)
dfs(1)

#debug()
#controls()
fb.mainloop()
