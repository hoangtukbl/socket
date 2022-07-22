from socket import *
from threading import *
import json
import os
import re

special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')    
def checkSpecialChar(username):
    if (special_char.search(username)):
        return True
    return False
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
def handle_client(client):
    while True:
        try:
            option = client.recv(1024).decode(FORMAT)
        except:
            break
        if not option:
            break
        if option == "DANG_NHAP":
            client.sendall(option.encode(FORMAT))
            ten_dn = client.recv(1024).decode(FORMAT)
            client.sendall(ten_dn.encode(FORMAT))
            mk = client.recv(1024).decode(FORMAT)
            client.sendall(mk.encode(FORMAT))
            f = open('tai_khoan.json', 'r')
            tai_khoan = json.load(f)
            f.close()
            logged_in = False
            for user in tai_khoan:
                if user['username'] == ten_dn:
                    if user['password'] == mk:
                        logged_in = True
                        print("Dang nhap thanh cong")
                        client.sendall("SUCCESS".encode(FORMAT))
                    else:
                        print("Dang nhap that bai")
                    break
            if not logged_in:
                client.sendall("Dang nhap that bai".encode(FORMAT))
            client.recv(1024)
        elif option == "DANG_KY":
            client.sendall(option.encode(FORMAT))
            ten_dn = client.recv(1024).decode(FORMAT)
            client.sendall(ten_dn.encode(FORMAT))
            mk = client.recv(1024).decode(FORMAT)
            client.sendall(mk.encode(FORMAT))
            f = open('tai_khoan.json', 'r+')
            tai_khoan = json.load(f)

            if len(ten_dn) < 5 or checkSpecialChar(ten_dn) or re.findall('[A-Z]',ten_dn):
                tmp = -1
            elif len(ten_dn) < 3:
                tmp = -2
            else:
                tmp = 1
            if tmp == 1:
                for user in tai_khoan:
                    if user['username'] == ten_dn:
                        print('Ten nguoi dung ton tai')
                        f.close()
                        tmp = -3
                        break
            client.sendall(str(tmp).encode(FORMAT))
            if tmp == 1:
                info = {
                    "username" : ten_dn,
                    "password" : mk
                }
                tai_khoan.append(info)
                f.seek(0)
                json.dump(tai_khoan, f, indent=4)
                f.close()
                newfolder = "./luu_tru/" + ten_dn
                os.mkdir(newfolder)
                khoi_tao = []
                file = open("./luu_tru/" + ten_dn + "/ghichu.json", "w")
                file.write(json.dumps(khoi_tao, indent=4))
                file.close()
                khoi_tao = []
                file = open("./luu_tru/" + ten_dn + "/files.json", "w")
                file.write(json.dumps(khoi_tao, indent=4))
                file.close()
                print("Tao tai khoan thanh cong")
            client.recv(1024)
        elif option == "THEM_NOTE":
            client.sendall(option.encode(FORMAT))
            file = open("./luu_tru/" + ten_dn + "/ghichu.json", "r+")
            note = json.load(file)
            tp = client.recv(1024).decode(FORMAT)
            client.sendall(tp.encode(FORMAT))
            if tp != "CANCEL":
                topic = client.recv(BUFFER_SIZE).decode(FORMAT)
                client.sendall(topic.encode(FORMAT))
                content = client.recv(BUFFER_SIZE).decode(FORMAT)
                client.sendall(content.encode(FORMAT))
                take_note = {
                    "id" : len(note) + 1,
                    "topic" : topic,
                    "content" : content
                }
                note.append(take_note)
                file.seek(0)
                json.dump(note, file, indent=4)    
                file.close()
            else: 
                file.close()
                print(tp)         
        elif option == "NOTE":
            client.sendall(option.encode(FORMAT))
            note_path = "./luu_tru/" + ten_dn + "/ghichu.json"
            file = open(note_path, "r")
            user_notes = json.load(file)
            client.sendall((json.dumps(user_notes)).encode(FORMAT))
            file.close()
        elif option == "VIEW_NOTE":
            client.sendall(option.encode(FORMAT))
            id = int(client.recv(1024).decode(FORMAT))
            client.sendall(str(id).encode(FORMAT))
            note_path = "./luu_tru/" + ten_dn + "/ghichu.json"
            file = open(note_path, "r")
            note = json.load(file)
            file.close()
            for note in note:
                if note['id'] == id:
                    client.sendall(note['topic'].encode(FORMAT))
                    client.recv(1024)
                    client.sendall(note['content'].encode(FORMAT))
                    client.recv(1024)
                    break
        elif option == "THEM_FILE":
            client.sendall(option.encode(FORMAT))
            info = client.recv(1024).decode(FORMAT).split(SEPARATOR)
            fpath = info[0]
            fsize = int(info[1])
            fname = os.path.basename(fpath)
            cwd = os.getcwd()
            up_path = "./luu_tru/" + ten_dn
            if not os.path.exists(up_path):
                os.mkdir(up_path)
            os.chdir(up_path)
            file = open("files.json", "r+")
            file_data = json.load(file)
            info = {
                "id" : len(file_data) + 1,
                "name" : fname
            }
            file_data.append(info)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            file.close()
            file = open(fname, "wb")
            recv = 0
            while True:
                data = client.recv(BUFFER_SIZE)
                recv += len(data)
                if recv >= fsize:
                    file.write(data)
                    break
                file.write(data)
            file.close()
            os.chdir(cwd)
            print("Receiving completed")
        elif option == "FILE":
            client.sendall(option.encode(FORMAT))
            file_path = "./luu_tru/" + ten_dn + "/files.json"
            file = open(file_path, "r")
            user_files = json.load(file)
            client.sendall((json.dumps(user_files)).encode(FORMAT))
            file.close()
        elif option == "VIEW_FILE":
            client.sendall(option.encode(FORMAT))
            id = int(client.recv(1024).decode(FORMAT))
            client.sendall(str(id).encode(FORMAT))
            file_path = "./luu_tru/" + ten_dn + "/files.json"
            file = open(file_path, "r")
            file_data = json.load(file)
            file.close()
            for file in file_data:
                if file['id'] == id:
                    client.sendall(file['name'].encode(FORMAT))
                    client.recv(1024)
                    break  
        elif option == "DOWNLOAD":
            client.sendall(option.encode(FORMAT))
            fname = client.recv(1024).decode(FORMAT)
            client.sendall(fname.encode(FORMAT))
            cwd = os.getcwd()
            os.chdir("./luu_tru/" + ten_dn)
            file = open(fname, "rb")
            filesize = os.path.getsize(fname)
            client.sendall(str(filesize).encode(FORMAT))
            client.recv(1024)
            while True:
                data = file.read(BUFFER_SIZE)
                if not data:
                    break
                client.sendall(data)    
            file.close()
            os.chdir(cwd)
            print("Download completed")
    client.close()   
clients = {}
addresses = {}

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 300000
HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
FORMAT = 'utf8'

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()