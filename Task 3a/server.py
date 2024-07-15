import socket
import threading
import json
import hashlib
import mysql.connector
from mysql.connector import Error
import time
HEADER = 64 
PORT = 6000
SERVER =socket.gethostbyname(socket.gethostname()) #command print only masked address on macos, check settings for using this addr in client
print(socket.gethostbyname(socket.gethostname())) #basically jus gets the local Ip from device, doesnt work on macos (its masked)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECTER = "!fu"
questions = []
users = {}
leaderb = {}
latestadr = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3333',
    'database': 'sys'
}
def create_tables():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        leaderboard_table_query = """
        CREATE TABLE IF NOT EXISTS leaderboard (
            username VARCHAR(255) PRIMARY KEY,
            score INT
        )
        """
        cursor.execute(leaderboard_table_query)

        users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255)
        )
        """
        cursor.execute(users_table_query)

        connection.commit()
        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")

def update_leaderboard():
    while True:
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            for user, score in leaderb.items():
                query = f"INSERT INTO leaderboard (username, score) VALUES ('{user}', {score}) ON DUPLICATE KEY UPDATE score={score}"
                cursor.execute(query)

            connection.commit()
            cursor.close()
            connection.close()
            time.sleep(10)  

        except Error as e:
            print(f"Error: {e}")

def update_users():
    while True:
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            for user, passwd in users.items():
                query = f"INSERT INTO users (username, password) VALUES ('{user}', '{passwd}') ON DUPLICATE KEY UPDATE password='{passwd}'"
                cursor.execute(query)

            connection.commit()
            cursor.close()
            connection.close()
            time.sleep(10)  # Wait for 10 seconds before updating again

        except Error as e:
            print(f"Error: {e}")

def fetch_data():
    while True:
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            # Fetch leaderboard data
            leaderboard_query = "SELECT username, score FROM leaderboard"
            cursor.execute(leaderboard_query)
            leaderboard_rows = cursor.fetchall()
            # Clear the dictionary and update with new values
            leaderb.clear()
            for row in leaderboard_rows:
                leaderb[row[0]] = row[1]

            # Fetch users data
            users_query = "SELECT username, password FROM users"
            cursor.execute(users_query)
            users_rows = cursor.fetchall()
            # Clear the dictionary and update with new values
            users.clear()
            for row in users_rows:
                users[row[0]] = row[1]

            cursor.close()
            connection.close()
            time.sleep(10)  

        except Error as e:
            print(f"Error: {e}")


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
    leaderb[username] = 0 
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
                if questions[int(qn)-1]["answer"] == opt:     #checks if answer is correct and gives said user one point
                    usrnm = list(latestadr.keys())[list(latestadr.values()).index(addr)]
                    leaderb[usrnm] = int(leaderb[usrnm]) + 1
            elif message == "D":
                leads = json.dumps(leaderb)
                leads = leads.encode(FORMAT)
                conn.send(leads)
            else:    
                print(f"{addr} says {message}")
    conn.close()

def start():                                 
    server.listen()
    thread1 = threading.Thread(target=update_leaderboard)
    thread2 = threading.Thread(target=update_users)
    thread3 = threading.Thread(target=fetch_data)
    thread1.start()
    thread2.start()
    thread3.start()
    print(f"{SERVER}")
    while True:
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"active conns -- {threading.active_count() - 1 }") #used to have a -1, no longer needed new lib- nvm im dumb af 
print("im gonna start now")
create_tables()
start()

