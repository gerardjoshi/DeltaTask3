import socket
import threading
import json
import hashlib
HEADER = 64 
PORT = 6000
SERVER ="192.168.0.101" #socket.gethostbyname(socket.gethostname()) #command doesnt work on mac for direct address, needs settings  
print(socket.gethostbyname(socket.gethostname())) #basically jus gets the local Ip from device
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECTER = "!fu"
questions = []
users = {}
leaderb = {}
latestadr = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def answering(answers):
   
    words = answers.split()
    
  
    if words and words[0].isdigit():
        return True
    return False

def checknewusr(sentence):
   
    words = sentence.split()
    if words and words[0] == "newusr":
        return True
    return False
def checklogin(sentence):
   
    words = sentence.split()
    if words and words[0] == "login":
        return True
    return False

def create_account(username, password):
    if username in users:
        print("Username already exists!")
        return False


    
    # SHA-256 hashing ting
    hash_object = hashlib.sha256(password.encode())
    hashed_password = hash_object.hexdigest()
    users[username] = hashed_password
    print("Account created successfully!")
    return True
def authenticate(username, password):
    if username not in users:
        print("Username does not exist!")
        return False
    hash_object = hashlib.sha256(password.encode())
    hashed_password = hash_object.hexdigest()
    
    if users[username] == hashed_password:       #checks the hash ting
        print(f"Authentication successful! for {username}")
        return True
    else:
        print(f"Authentication failed for {username}")
        return False




def handle_client(conn, addr):
    #this runs for each client
    print(f"new conns -- {addr}") #shows who the new conns is 
    connected = True
    while connected:
        message_len = conn.recv(HEADER).decode(FORMAT) 
        if message_len:     #important this runs in threads as these are blocking lines of code and shouldnt blocks other clients
            message_len = int(message_len)
            message = conn.recv(message_len).decode(FORMAT)
            if message == DISCONNECTER :
                connected = False
            elif message and message[0] == '{':
                question_rec = json.loads(message)
                questions.append(question_rec)
                print(json.dumps(questions[0]))
            elif message == "V" :
                qsend = " "
                for question in questions :
                    qsend = qsend + str(question["question"])
                    qsend = qsend + f"\n"
                qsend = qsend.encode(FORMAT)
                conn.send(qsend)
            elif checknewusr(message):
                
   
                words = message.split()
                usrnm = words[1]
                passwd = words[2]
                create_account(usrnm,passwd)
                latestadr[f"{usrnm}"] = addr
            elif checklogin(message):
                
   
                words = message.split()
                usrnm = words[1]
                passwd = words[2]
                authenticate(usrnm,passwd)
                latestadr[f"{usrnm}"] = addr
            elif answering(message):
                words = message.split() 
                qn = words[0]
                opt = words[1]
                if questions[qn-1]["answer"] == opt:
                    leaderb[""]

            else:    
                print(f"{addr} says {message}")
    conn.close()

def start():                                 
    server.listen()
    print(f"{SERVER}")
    while True:
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"active conns -- {threading.active_count() - 1 }") #used to have a -1, no longer needed new lib- nvm im dumb af 
print("im gonna start now")

start()

