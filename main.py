from tkinter import *
import tkinter.font as font
import pyperclip, random, string,re
from tkinter import messagebox

root = Tk()
root.title("Password Manager")
root.configure(bg="gray8")
root.geometry("700x500")
p1 = PhotoImage(file="lock.png")
root.iconphoto(False, p1)

fontstyle = font.Font(family="Lucida Grande", size=10)

def login():
    pswd = Label(root, text="Password\n?", bg="gray8", fg="gray60", font=fontstyle)
    pswd.place(x=350, y=200, anchor="center")
    enter_pswd = Entry(root, bg="white", fg="black", font=fontstyle)
    enter_pswd.place(x=350, y=230, anchor="center")
    print(enter_pswd.get())
    sub = Button(text="Submit", bg="gray10", fg="gray60", font=fontstyle, border=0,
                 command=lambda: validate(enter_pswd.get()))
    sub.place(x=350, y=270, anchor="center")

    def validate(psd):
        if psd == "1234":
            generator()
            check()
            save()
            get_pswd()
        else:
            login()
        pswd.place_forget()
        enter_pswd.place_forget()
        sub.place_forget()

def generator():
    l1 = Label(root, text="Generate Password", bg="gray8", fg="gray50", font=fontstyle)
    l1.place(x=7, y=7)
    f = Frame(root, height=1, width=700, bg="gray50").place(x=130, y=17)
    r = IntVar()
    r.set("1")
    global l2
    Radiobutton(root, text="Strong", bg="gray8", fg="gray50", font=fontstyle, variable=r, value=14).place(x=7, y=50)
    Radiobutton(root, text="Moderate", bg="gray8", fg="gray50", font=fontstyle, variable=r, value=10).place(x=100, y=50)
    Radiobutton(root, text="Weak", bg="gray8", fg="gray50", font=fontstyle, variable=r, value=6).place(x=200, y=50)
    confirm = Button(text="Confirm", bg="gray10", fg="gray60", font=fontstyle, border=0,
                     command=lambda: gen(r.get()))
    confirm.place(x=300, y=50)
    l2 = Label(root, text="", bg="gray8", fg="white", font=fontstyle)
    l2.place(x=450, y=50)

    def gen(length):
        global l2
        if length == 14:
            l2.place_forget()
            a, b, c, d = 5, 3, 3, 3
        elif length == 10:
            l2.place_forget()
            a, b, c, d = 4, 2, 2, 2
        elif length == 6:
            l2.place_forget()
            a, b, c, d = 3, 1, 1, 1
        lower = [random.choice(string.ascii_lowercase) for i in range(a)]
        upper = [random.choice(string.ascii_uppercase) for i in range(b)]
        digits = [random.choice(string.digits) for i in range(c)]
        punct = [random.choice(r'!#$%&*+<>@|') for i in range(d)]
        ls = lower + upper + digits + punct
        random.shuffle(ls)
        result = "".join(ls)
        l2 = Label(root, text=result, bg="gray8", fg="white", font=fontstyle)
        l2.place(x=400, y=50)
        copy = Button(text="Copy", bg="gray10", fg="gray60", font=fontstyle, border=0,
                      command=pyperclip.copy(result))
        copy.place(x=550, y=50)

def check():
    label_title = Label(root, text="Check strength of password ", bg="gray8", fg="gray50", font=fontstyle)
    label_title.place(x=7, y=100)
    f = Frame(root, height=1, width=700, bg="gray50").place(x=180, y=110)
    label_for_pswd = Label(root, text="Enter the password you want to check: ", bg="gray8", fg="gray50", font=fontstyle)
    label_for_pswd.place(x=7, y=150)
    input_pswd = Entry(root, bg="seashell4", fg="black", font=fontstyle)
    input_pswd.place(x=300, y=150)
    check = Button(text="Check", bg="gray10", fg="gray60", font=fontstyle, border=0,
                   command=lambda: check_pswd(input_pswd.get()))
    check.place(x=500, y=150)
    global type_label
    type_label = Label(root, text="", bg="gray8", fg="gray50",
                       font=fontstyle)
    type_label.place(x=600, y=150)

def check_pswd(pswd):
    global type_label
    p1, p2, p3 = "[A-Z]", "[a-z]", "[0-9]"
    r1 = re.findall(p1, pswd)
    r2 = re.findall(p2, pswd)
    r3 = re.findall(p3, pswd)
    ls = r1 + r2 + r3
    r4 = [i for i in pswd if i not in ls]
    if len(r1) >= 3 and len(r2) >= 5 and len(r3) >= 3 and len(r4) >= 3:
        type_label.place_forget()
        type_of_pswd = "".join("strong")
    elif len(r1) >= 2 and len(r2) >= 4 and len(r3) >= 2 and len(r4) >= 2:
        type_label.place_forget()
        type_of_pswd = "".join("moderate")
    elif len(r1) >= 1 and len(r2) >= 3 and len(r3) >= 1 and len(r4) >= 1:
        type_label.place_forget()
        type_of_pswd = "".join("weak")
    else:
        type_label.place_forget()
        type_of_pswd = "".join("extremely weak")
    type_label = Label(root, text=type_of_pswd, bg="gray8", fg="gray50",
                       font=fontstyle)
    type_label.place(x=570, y=150)
    return type_of_pswd

def saving(key, pswd):
    type_of_pswd = check_pswd(pswd)
    text = "Password is " + type_of_pswd + ". Save it?"
    response = messagebox.askyesno("Sure?", text)
    if response == 1:
        with open("file.txt", "a") as f:
            f.write(key)
            f.write(" ")
            f.write(pswd)
            f.write("\n")
            messagebox.showinfo("Info", "Password saved!")
    else:
        messagebox.askretrycancel("Retry", "Password not saved!")

def getting(key):
    state = 0
    with open("file.txt", "r") as f:
        ls = list(map(lambda x: x.replace("\n", ""), f.readlines()))
        for i in ls:
            if key in i:
                pyperclip.copy(i.split()[1])
                state=1

        if state==1:
            messagebox.showinfo("Info", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "Password does not exist")

def save():
    label_title = Label(root, text="Save password", bg="gray8", fg="gray50", font=fontstyle)
    label_title.place(x=7, y=210)
    f = Frame(root, height=1, width=700, bg="gray50").place(x=105, y=220)
    for_what = Label(root, text="For:", bg="gray8", fg="gray50", font=fontstyle)
    for_what.place(x=7, y=250)
    for_what_app = Entry(root, bg="seashell4", fg="black", font=fontstyle)
    for_what_app.place(x=50, y=250)
    pswd_is = Label(root, text="Password is:", bg="gray8", fg="gray50", font=fontstyle)
    pswd_is.place(x=300, y=250)
    pswd_for_app_is = Entry(root, bg="seashell4", fg="black", font=fontstyle)
    pswd_for_app_is.place(x=400, y=250)
    save_btn = Button(text="Save", bg="gray10", fg="gray60", font=fontstyle, border=0,
                      command=lambda: saving(for_what_app.get(), pswd_for_app_is.get()))
    save_btn.place(x=600, y=250)

def get_pswd():
    label_title = Label(root, text="Get password", bg="gray8", fg="gray50", font=fontstyle)
    label_title.place(x=7, y=290)
    f = Frame(root, height=1, width=700, bg="gray50").place(x=100, y=300)
    for_what = Label(root, text="For:", bg="gray8", fg="gray50", font=fontstyle)
    for_what.place(x=7, y=330)
    for_what_app = Entry(root, bg="seashell4", fg="black", font=fontstyle)
    for_what_app.place(x=50, y=330)
    get_btn = Button(text="Get", bg="gray10", fg="gray60", font=fontstyle, border=0,
                     command=lambda: getting(for_what_app.get()))
    get_btn.place(x=250, y=330)

login()
root.mainloop()
