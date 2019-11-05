from tkinter import *
from collections import defaultdict
from PIL import Image
from PIL import ImageTk
import sqlite3
import time,random
import tkinter.messagebox as tmsg

global nodes
global namefriend
global ind
global p
global person

nodes = []
buttonchatclicked = 0
def fetchData():
    crsr2 = db.execute("SELECT * FROM FRIEND")
    i=0
    for row in crsr2 :
        graph[row[0]].append(row[1])
        graph[row[1]].append(row[0])
        
graph = defaultdict(list)
def addedge(u,v):
    graph[u].append(v)
    graph[v].append(u)
#CONTROLS
def controls():
    db.execute("DELETE FROM FRIEND WHERE FRIEND = 'Varun'")
    #db.execute("UPDATE FRIEND SET MESSAGE = ? WHERE USER IN ('Vikas','Tarun','Ankita')",("",))
    db.commit()

#CORE DATABASE
def debug():
    crsr = db.execute("SELECT * FROM FACEBOOK")
    c=0
    print("\n")
    print("FACEBOOK HEADQUARTERS DATABASE 2019")
    for row in crsr :
        if(c==0):
            print("USERNAME       ", "PASSWORD      ", "CITY      ", "WORK      ", "DOB      ", "STATUS      ")
            print("----------------------------------------------------------------------")
        print(row[0],"    ",row[1],"    ",row[2],"    ",row[3],"    ",row[4],"    ",row[5])
        c+=1
    print(c, "People are registered into your website")
    print("*********************************\n\n")
    crsr2 = db.execute("SELECT * FROM FRIEND")
    i=0
    print("FRIENDS DATA")
    for row in crsr2 :
        if(i==0):
            print("USERNAME       ", "FRIEND      ","MESSAGE            ")
            print("-------------------------------------------------")
        print(row[0],"    ",row[1],"    ",row[2])
        i+=1
    print("\n")
    print(graph)
#MAIN    
db = sqlite3.connect("fbdb.db")
db.execute("CREATE TABLE IF NOT EXISTS FACEBOOK(USERNAME CHAR[30], PASSWORD CHAR[30], CITY CHAR[20], WORK CHAR[20], DOB CHAR[10], STATUS CHAR[150])")
db.execute("CREATE TABLE IF NOT EXISTS FRIEND(USER CHAR[30], FRIEND CHAR[30], MESSAGE CHAR[100])")
#Insert all the edges means connect all the friends in the graph by using the FRIEND table. Use addedge function. Then,
#In the window which will have the add friend button, when it will be clicked, the friend and user will be inserted in the FRIEND table and then,
# Call the function addedge again from there.
# Then we will make a button My Friends in mypage window, only my friends will be shown and the remaining will be shown in Find Friends.
db.commit()

global fb
fb = Tk()
fb.geometry("360x850")
fb.wm_iconbitmap("fb.ico")
fb.title("Facebook - Welcome to Facebook!")
Label(text = "Welcome To Facebook! Login or Signup",font=("Calibri",15,"bold")).pack()

def write():
    quote = u1 + " : "+msg.get()
    crsr = db.execute("UPDATE FRIEND SET MESSAGE = ? WHERE FRIEND = ?",(quote,namefriend,) )
    db.commit()
def message():
    global msg
    msg = StringVar()
    print("Write your message")
    mess = Entry(friendpage,textvariable=msg,width="55")
    mess.pack(pady="4px")
    send = Button(friendpage,text="Send",height="1",width="10",bg = "indigo",fg = "white",command=write)
    send.pack(pady="1px")
    
def addfriend():
    db.execute("INSERT INTO FRIEND (USER,FRIEND) VALUES(?,?)",(u1,nodes[ind]))
    #db.execute("INSERT INTO FRIEND (USER,FRIEND) VALUES(?,?)",(nodes[ind],u1))
    db.commit()
    addbutton.destroy()
    graph[u1].append(nodes[ind])
    graph[nodes[ind]].append(u1)
    messbutton = Button(friendpage, text = "Message", height="2",width="20",bg = "indigo",fg = "white",command=message)
    messbutton.pack(pady="3px")
    print(f"{u1} is a friend of {nodes[ind]}")
def wall():
    global friendpage
    global x
    global p
    global fp
    global addbutton
    global messbutton
    global namefriend

    if(friendname.get() is not ""):
        namefriend = friendname.get()
        
    friendpage = Toplevel(mypage)
    friendpage.wm_iconbitmap("fb.ico")
    friendpage.title(f"{namefriend}")
    friendpage.geometry("360x550")
    
    x = Image.open("de.png")
    x= x.resize((120,75),Image.ANTIALIAS)
    fp = ImageTk.PhotoImage(x)
    Label(friendpage, image = fp,anchor="w").pack(fill="both")
    Label(friendpage, text = namefriend, anchor = "w",font = (15)).pack(fill="both",padx="3px")
    crsr = db.execute("SELECT CITY FROM FACEBOOK WHERE USERNAME = (?)", (namefriend,))
    for row in crsr:
        city1 = row[0]
    Label(friendpage, text = f"Lives in {city1}",anchor = "w").pack(fill="both",padx="3px")
    crsr = db.execute("SELECT WORK FROM FACEBOOK WHERE USERNAME = (?)", (namefriend,))
    for row in crsr:
        work1 = row[0]
    Label(friendpage, text = f"Works as {work1}",anchor = "w").pack(fill="both",padx="3px")
    crsr = db.execute("SELECT DOB FROM FACEBOOK WHERE USERNAME = (?)", (namefriend,))
    for row in crsr:
        dob1 = row[0]
    Label(friendpage, text = f"Born on {dob1}",anchor = "w").pack(fill="both",padx="3px")
    crsr = db.execute("SELECT STATUS FROM FACEBOOK WHERE USERNAME = (?)", (namefriend,))
    for row in crsr:
         status1 = row[0]
    Label(friendpage, text = status1,anchor = "c").pack(fill="both",pady="4px")
    if(namefriend in graph[u1]):
        messbutton = Button(friendpage, text = "Message", height="2",width="20",bg = "indigo",fg = "white",command=message)
        messbutton.pack(pady="3px")
    else:
        addbutton = Button(friendpage, text = "Add Friend", height="2",width="20",bg = "indigo",fg = "white",command=addfriend)
        addbutton.pack(pady="3px")
    question.after(1200,lambda : question.destroy())
    if(friendname.get() is ""):
        p.destroy()
    else:
        entername.delete(0,END)

def friendFind():
    global namefriend
    crsr = db.execute("SELECT DISTINCT(USERNAME) FROM FACEBOOK WHERE USERNAME != (?)",(u1,))
    for row in crsr:
        nodes.append(row[0])
    global ind
    global p
    randomIndex = []
    n = len(nodes)
    for t in range(n):
        if(nodes[t] not in graph[u1]):
            randomIndex.append(t)
    randomsize = len(randomIndex)
    ind = nodes.index(nodes[random.choice(randomIndex)])
    namefriend = nodes[ind]
    p = Button(mypage,text = namefriend,height="1",width="10",bg = "indigo",fg = "white",command = wall )
    p.pack(pady="3px")
        
def myAccount():
    global mypage
    global d
    global myf
    global findFriend
    global p
    global question
    global friendname
    global entername
    mypage = Toplevel(fb1)
    mypage.wm_iconbitmap("fb.ico")
    mypage.title(f"{u1}")
    mypage.geometry("360x750")

    friendname = StringVar()
    d = Image.open("de.png")
    d= d.resize((120,75),Image.ANTIALIAS)
    myf = ImageTk.PhotoImage(d)
    Label(mypage, image = myf,anchor="w").pack(fill="both")
    lab = Label(mypage,text = "ONLINE",font=("Calibri",9,"bold"),fg="green")
    lab.place(x=40,y=80)
    Label(mypage,text = f"Welcome {u1}! What's on your mind?",font=("Calibri",14,"bold")).pack(pady="20px")
    crsr = db.execute("SELECT CITY FROM FACEBOOK WHERE USERNAME = (?)", (u1,))
    for row in crsr:
        city1 = row[0]
    Label(mypage, text = f"Lives in {city1}",anchor = "w").pack(fill="both",padx="3px")
    crsr = db.execute("SELECT WORK FROM FACEBOOK WHERE USERNAME = (?)", (u1,))
    for row in crsr:
        work1 = row[0]
    Label(mypage, text = f"Works as {work1}",anchor = "w").pack(fill="both",padx="3px")
    crsr = db.execute("SELECT DOB FROM FACEBOOK WHERE USERNAME = (?)", (u1,))
    for row in crsr:
        dob1 = row[0]
    Label(mypage, text = f"Born on {dob1}",anchor = "w").pack(fill="both",padx="3px")
    crsr = db.execute("SELECT STATUS FROM FACEBOOK WHERE USERNAME = (?)", (u1,))
    for row in crsr:
         status1 = row[0]
    Label(mypage, text = status1,anchor = "c").pack(fill="both",pady="4px")
    Label(mypage, text = "My Messages",anchor = "c",font=("Tahoma",14)).pack(fill="both",pady="2px")
    crsr = db.execute("SELECT MESSAGE FROM FRIEND WHERE FRIEND = ?",(u1,))
    for row in crsr:
        Label(mypage, text = row[0],anchor = "w",fg = "blue").pack(fill="both",pady="2px")
    Label(mypage,text ="My Friends",font=("Calibri",12,"bold"),anchor="w").pack(fill="both",padx="3px")
    for friend in graph[u1]:
        Label(mypage, text = friend, anchor = "w",fg="green").pack(fill="both",padx="3px")
    #person = random.choice(graph[u1])

    question = Label(mypage, text = "Enter the name to chat:" , anchor = "w")
    question.pack(fill="both",padx="3px",pady="3px")
    entername =Entry(mypage,textvariable=friendname,width="30")
    entername.pack(pady = "3px")
    chat = Button(mypage, text = "Chat Now!",height="2",width="10",bg = "indigo",fg = "white", command = wall)
    chat.pack(pady="4px")
    findFriend = Button(mypage, text = "Find Friends",height="2",width="20",bg = "indigo",fg = "white", command = friendFind)
    findFriend.pack(pady="4px")
    
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

def submit():
    global stat
    stat = yourself_entry.get("1.0","end-1c")
    db.execute("INSERT INTO FACEBOOK(USERNAME, PASSWORD, CITY, WORK, DOB, STATUS) VALUES(?,?,?,?,?,?)",(u2, p2,city.get(),profession.get(),DOB.get(),stat))
    db.commit()
    status0 = Label(fb,text = "Registration Successful!",fg="green")
    status0.pack()
    status0.after(2000,lambda : status0.destroy())
    nodes.append(u2)
    detail.destroy()
def register():
    global detail
    global city
    global profession
    global DOB
    global yourself_entry
    detail = Toplevel(fb)
    detail.title("Registration")
    detail.geometry("400x450")
    detail.wm_iconbitmap("fb.ico")
    city = StringVar()
    profession = StringVar()
    yourself = StringVar()
    DOB = StringVar()
    Label(detail,text = f"Welcome {u2}! Now Tell us About Yourself",font=("Calibri",13,"bold")).pack()
    Label(detail,text = "City",font=("Calibri",12)).pack()
    city_entry = Entry(detail, textvariable = city,width="30")
    city_entry.pack()
    Label(detail,text = "Profession",font=("Calibri",12)).pack()
    profession_entry = Entry(detail, textvariable = profession,width="30")
    profession_entry.pack()
    Label(detail,text = "Date of Birth",font=("Calibri",12)).pack()
    DOB_entry = Entry(detail, textvariable = DOB,width="30")
    DOB_entry.pack()
    Label(detail,text = "Bio",font=("Calibri",12)).pack()
    yourself_entry = Text(detail,width="40",height="10",font=("Calibri"))
    yourself_entry.pack()
    Button(detail,text="Submit",height="2",width="20",bg = "indigo",fg = "white",command=submit).pack()
    
def signup():
    global u2
    global p2
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
        register()
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

fetchData()
debug()
controls()
fb.mainloop()
