from graphlib import TopologicalSorter
from itertools import tee
import cv2
import json
import os
from socket import *
from threading import *
from tkinter import *
from tkinter import filedialog
import tkinter
import shutil

class LogIn:
    def __init__(self, frame, socket):
        self.socket = socket

        self.frame = Frame(frame, width=925, height=500)
        self.frame.place(x=0, y=0)

        backg = PhotoImage(file = './images/dang_nhap.png')
        logInLabel = Label(self.frame,image=backg)
        logInLabel.image = backg
        logInLabel.pack(fill='both', expand='yes')
        
        
        logInLabel.place(x=-2,y=-2)
        
        self.ten = Entry(self.frame, width=30, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.ten.place(x=528, y=217)
        self.mk = Entry(self.frame, show='*', width=30, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.mk.place(x=528, y=283)

        def show_password():
            if self.mk.cget('show')=='*':
                self.mk.config(show='')
                self.checkbtn.config(text="Ẩn")

            else:
                self.mk.config(show='*')
                self.checkbtn.config(text="Hiện")

        self.checkbtn = Button(self.frame,text="Hiện", width=5,activebackground='white', bg='white', command=lambda:show_password())
        self.checkbtn.place(x=788, y=283)

        btn = Button(self.frame, width=15, text="Đăng nhập", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, command=self.log_in, bg='#FFF6B6', fg='#002066')
        btn.place(x=620, y=337)

        register_btn = Button(self.frame, width=15, text="Đăng kí", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#FFF6B6', fg='#002066', command=self.register)
        register_btn.place(x=620, y=404)
    
    def log_in(self):
        name = self.ten.get()
        psw = self.mk.get()

        if name == '' or psw == '':
            return
        
        option = "DANG_NHAP"
        self.socket.sendall(option.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Da gui thong tin dang nhap")

        response = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(response.encode(FORMAT))

        if response != "SUCCESS":
            tkinter.messagebox.showinfo("Thông báo", "Sai tên đang nhập hoặc mật khẩu")
        else:
            self.frame.destroy()
            Menu(root, self.socket)

    def register(self):
        self.frame.destroy()
        Register(root, self.socket)

class Register:
    def __init__(self, frame, socket):
        self.socket = socket

        self.frame = Frame(frame, width=925, height=500)
        self.frame.place(x=0, y=0)

        backg = PhotoImage(file = './images/dang_ki.png')
        registerLabel = Label(self.frame,image=backg)
        registerLabel.image = backg
        registerLabel.pack(fill='both', expand='yes')
        registerLabel.place(x=-2,y=-2)
        
        self.ten = Entry(self.frame, width=30, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.ten.place(x=528, y=217)

        self.mk = Entry(self.frame, show='*', width=30, fg='black', bg='#f9f9f9', bd=0,
                            font=('Roboto', 13))
        self.mk.place(x=528, y=283)

        def show_password():
            if self.mk.cget('show')=='*':
                self.mk.config(show='')
                self.checkbtn.config(text="Ẩn")

            else:
                self.mk.config(show='*')
                self.checkbtn.config(text="Hiện")

        self.checkbtn = Button(self.frame,text="Hiện", width=5,activebackground='white', bg='white', command=lambda:show_password())
        self.checkbtn.place(x=788, y=283)


        btn = Button(self.frame, width=15, text="Đăng kí", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, command=self.register, bg='#FFF6B6', fg='#002066')
        btn.place(x=620, y=337)

        log_in_btn = Button(self.frame, width=15, text="Đăng nhập", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#FFF6B6', fg='#002066', command=self.log_in)
        log_in_btn.place(x=620, y=404)
    
    def register(self):
        name = self.ten.get()
        psw = self.mk.get()

        if psw == '' or name == '':
            return

        option = "DANG_KY"
        self.socket.sendall(option.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(name.encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(psw.encode(FORMAT))
        self.socket.recv(1024)

        print("Da gui thong tin dang ky")

        response = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(response.encode(FORMAT))

        if response == "1":
            tkinter.messagebox.showinfo("Thông báo", "Đăng ký thành công")
        elif response == "-1":
            tkinter.messagebox.showinfo("Thông báo", "Tên người dùng không hợp lệ")
        elif response == "-2":
            tkinter.messagebox.showinfo("Thông báo", "Mật khẩu không hợp lệ")
        elif response == "-3":
            tkinter.messagebox.showinfo("Thông báo", "Tên người dùng đã tồn tại")

    def log_in(self):
        self.frame.destroy()
        LogIn(root, self.socket)

class TakeNote:
    def __init__(self, socket):
        self.root = Toplevel()
        self.root.geometry("925x500")
        self.root.title("New note")

        self.socket = socket
        self.frame = Frame(self.root, width=925, height=500)
        self.frame.pack()
        self.frame.place(x=0, y=0)

        backg = PhotoImage(file = './images/ghi_chu.png')
        upNoteLabel = Label(self.frame,image=backg)
        upNoteLabel.image = backg
        upNoteLabel.pack(fill='both', expand='yes')
        upNoteLabel.place(x=-2,y=-2)
        self.topicEnt = Entry(self.frame, width=50, fg='black', bg='white', bd=0,
                            font=('Roboto', 13))
        self.topicEnt.place(x=260, y=60)
        self.contentEnt = Text(self.frame, width=57, height=12, fg='black', bg='white', bd=0,
                            font=('Roboto', 13))
        self.contentEnt.place(x=190, y=161)
        newNote = Button(self.frame, width=10, text="Ghi chú mới", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, command=self.UpNote, bg='#002066', fg='white')
        newNote.place(x=791, y=400)
        cancel = Button(self.frame, width=10, text="Đóng", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, command=self.cancel, bg='white', fg='#002066')
        cancel.place(x=791, y=451)
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.root.mainloop()

    def UpNote(self):
        topic = self.topicEnt.get()
        content = self.contentEnt.get(1.0, END)

        if topic == "" or content == "\n":
            tkinter.messagebox.showinfo("Thông báo", "Tiêu đề hoặc nội dung không được để trống")
            self.cancel()
            return

        self.socket.sendall("ADD_NOTE".encode(FORMAT))
        self.socket.recv(1024)
        
        self.socket.sendall(topic.encode(FORMAT))
        self.socket.recv(BUFFER_SIZE)

        self.socket.sendall(content.encode(FORMAT))
        self.socket.recv(BUFFER_SIZE)

        self.root.destroy()
        return
    def cancel(self):
        self.socket.sendall("CANCEL".encode(FORMAT))
        self.socket.recv(1024)

        print("Cancel note")
        self.root.destroy()
        return

class ShowNote:
    def __init__(self, socket, note_id):
        self.root = Toplevel()
        self.root.geometry("925x500")
        self.root.title("Viewing note")

        self.socket = socket
        self.frame = Frame(self.root, width=925, height=500, bg='white')
        self.frame.pack()
        self.frame.place(x=0, y=0)


        backg = PhotoImage(file = './images/hien_ghi_chu.png')
        showNoteBG = Label(self.frame,image=backg)
        showNoteBG.image = backg
        showNoteBG.pack(fill='both', expand='yes')
        showNoteBG.place(x=-2,y=-2)
        self.socket.sendall("VIEW_NOTE".encode(FORMAT))
        self.socket.recv(1024)
        self.socket.sendall(str(note_id).encode(FORMAT))


        self.socket.recv(1024)
        topic = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(topic.encode(FORMAT))
        content = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(content.encode(FORMAT))
        view_topic = Label(self.frame, width=40, text=topic, anchor=W,
                            font=('Roboto', 14), bg='white', fg='black')
        view_topic.place(x=380, y=100)
        view_content = Label(self.frame, width=57, text=content, anchor=W,
                            font=('Roboto', 12), bg='white', fg='black' , justify=LEFT)
        view_content.place(x=305, y=162)
        close_btn = Button(self.frame, width=10, text="Đóng", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='white', fg='#002066', command=self.cw)
        close_btn.place(x=791, y=451)

        self.root.mainloop()

    def cw(self):
        self.root.destroy()

class ShowFile:
    def __init__(self, socket, file_id):
        self.root = Tk()
        self.root.geometry("120x120")
        self.root.title("Viewing file")

        self.socket = socket
        self.frame = Frame(self.root, width=120, height=120, bg='white')
        self.frame.pack()
        
        
        self.frame.place(x=0, y=0)
        self.socket.sendall("VIEW_FILE".encode(FORMAT))
        self.socket.recv(1024)
        self.socket.sendall(str(file_id).encode(FORMAT))
        self.socket.recv(1024)
        self.file_name = self.socket.recv(1024).decode(FORMAT)
        self.socket.sendall(self.file_name.encode(FORMAT))
        self.st()
        if os.path.splitext(self.file_name)[1] == ".png" or os.path.splitext(self.file_name)[1] == ".jpg":
            path = './tmp/' + self.file_name
            img = cv2.imread(path)
            cv2.imshow('Viewing Image', img)
        close_btn = Button(self.frame, width=10, text="Tắt", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#002066', fg='white', command=self.cw)
        close_btn.place(x=13, y=50)
        dwn_btn = Button(self.frame, width=10, text="Tải về", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#002066', fg='white', command=self.df)
        dwn_btn.place(x=13, y=20)

        self.root.protocol("WM_DELETE_WINDOW", self.cw)
        
    
    def st(self):
        self.socket.sendall("DOWNLOAD".encode(FORMAT))
        self.socket.recv(1024)

        self.socket.sendall(self.file_name.encode(FORMAT))
        self.socket.recv(1024)

        cwd = os.getcwd()
        down_path = "./tmp/"
        if not os.path.exists(down_path):
            os.mkdir(down_path)
        os.chdir(down_path)
        filesize = int(self.socket.recv(1024).decode(FORMAT))
        self.socket.sendall(str(filesize).encode(FORMAT))
        file = open(self.file_name, "wb")
        recved = 0
        while True:
            data = self.socket.recv(BUFFER_SIZE)
            recved += len(data)
            if recved >= filesize:
                file.write(data)
                break
            file.write(data)
        file.close()
        os.chdir(cwd)
    
    def df(self):
        self.socket.sendall("DOWNLOAD".encode(FORMAT))
        self.socket.recv(1024)
        self.socket.sendall(self.file_name.encode(FORMAT))
        self.socket.recv(1024)

        cwd = os.getcwd()
        down_path = "./download/"
        if not os.path.exists(down_path):
            os.mkdir(down_path)
        os.chdir(down_path)

        filesize = int(self.socket.recv(1024).decode(FORMAT))
        self.socket.sendall(str(filesize).encode(FORMAT))
        
        file = open(self.file_name, "wb")
        recved = 0
        while True:
            data = self.socket.recv(BUFFER_SIZE)
            recved += len(data)
            if recved >= filesize:
                file.write(data)
                break
            file.write(data)
        file.close()

        os.chdir(cwd)
        self.clean_folder()
    def clean_folder(self):
        shutil.rmtree("./tmp/")
        os.makedirs("./tmp/", exist_ok=True)
    def cw(self):
        self.clean_folder()
        self.root.destroy()

class Menu:
    def __init__(self, frame, socket):
        self.socket = socket
        self.frame = Frame(frame, width=925, height=500)
        self.frame.pack()
        
        
        self.frame.place(x=0, y=0)
        self.filepath = ""

        backg = PhotoImage(file = './images/menu.png')
        MenuLabel = Label(self.frame,image=backg)
        MenuLabel.image = backg
        MenuLabel.pack(fill='both', expand='yes')
        MenuLabel.place(x=-2,y=-2)
        upFileButton = Button(self.frame, width=20, text="Tải tệp lên", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#FFF6B6', fg='black', command=self.UpFiles)
        upFileButton.place(x=665, y=405)
        refresh = Button(self.frame, width=20, text="Làm mới", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='white', fg='#002066', command=self.UpdateList)
        refresh.place(x=665, y=446)
        upNoteButton = Button(self.frame, width=20, text="Tải ghi chú lên", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#FFF6B6', fg='black', command=self.UpNote)
        upNoteButton.place(x=665, y=213)
        browse = Button(self.frame, width=20, text="Chọn tệp", activebackground='#6A93CE', 
                        font=('Roboto', 11), bd=0, bg='#FFF6B6', fg='black', command=self.addFiles)
        browse.place(x=665, y=359)
        self.notelist = Listbox(self.frame, width=40, height=5, bd=0, font=('Roboto', 16),
                                highlightthickness=0, selectbackground='#D4D4D4')
        self.notelist.place(x=76, y=75)
        self.notelist.bind("<<ListboxSelect>>", self.show_note)
        self.fileslist = Listbox(self.frame, width=40, height=5, bd=0, font=('Roboto', 16),
                                highlightthickness=0, selectbackground='#D4D4D4')
        self.fileslist.place(x=76, y=310)
        self.fileslist.bind("<<ListboxSelect>>", self.show_file)
        self.UpdateList()
    def addFiles(self):
        self.filepath = filedialog.askopenfilename(initialdir = "/", 
                title = "Select a File", filetypes=[("files", "*.*")])
    def show_file(self, event):
        selection = event.widget.curselection()
        file_id = selection[0] + 1
        ShowFile(self.socket, file_id)
    def UpNote(self):
        self.socket.sendall("THEM_NOTE".encode(FORMAT))
        self.socket.recv(1024)
        TakeNote(self.socket)
    def UpdateList(self):
        self.socket.sendall("NOTE".encode(FORMAT))
        self.socket.recv(1024)
        self.user_notes = json.loads(self.socket.recv(1024).decode(FORMAT))
        self.notelist.delete(0, END)
        ID = 1
        for i in self.user_notes:
            self.notelist.insert(ID, i['topic'])
            ID += 1  
        self.socket.sendall("FILE".encode(FORMAT))
        self.socket.recv(1024)
        self.user_files = json.loads(self.socket.recv(1024).decode(FORMAT))
        self.fileslist.delete(0, END)
        ID = 1
        for i in self.user_files:
            self.fileslist.insert(ID, i['name'])
            ID += 1
    def UpFiles(self):
        if self.filepath:
            self.socket.sendall("THEM_FILE".encode(FORMAT))
            self.socket.recv(1024)
            filesize = os.path.getsize(self.filepath)
            info = f"{self.filepath}{SEPARATOR}{filesize}"
            self.socket.sendall(info.encode(FORMAT))
            print("Uploading file")
            file = open(self.filepath, "rb")
            while True:
                data = file.read(BUFFER_SIZE)
                if not data:
                    break
                self.socket.sendall(data)    
            print("Upload completed")
            file.close()
            self.filepath = ""

    def show_note(self, event):
        selection = event.widget.curselection()
        note_id = selection[0] + 1
        ShowNote(self.socket, note_id)
    

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 300000
HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

root = Tk()
root.geometry('925x500+300+200')       
root.resizable(False, False)          
root.title('E-Note')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

login = LogIn(root, client_socket)


root.mainloop()