import socket
import json
import threading

HEADER = 64 
PORT = 6000
FORMAT = 'utf-8'
SERVER = "192.168.0.101"
DISCONNECTER = "!fu"
ADDR = (SERVER,PORT)
questions = []
user = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def checkrec(): #thread to check for server replies
    reply = client.recv(2400)
    reply = reply.decode(FORMAT)
    print(reply)  
    print("\n")  
def add_question():
    question_data = {}
    
    question_data["question"] = input("Enter the text for the question: ")
    question_data["option a"] = input("Enter option a: ")
    question_data["option b"] = input("Enter option b: ")
    question_data["option c"] = input("Enter option c: ")
    question_data["option d"] = input("Enter option d: ")
    question_data["answer"] = input("Enter the answer (a, b, c, or d): ")
    question_data["byuser"] = user
    questions.append(question_data)
    qstr = json.dumps(question_data)
    send(qstr)



def send(masag):
    message = masag.encode(FORMAT)
    msg_len = len(message)
    send_len = (str(msg_len)).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
print(f"""Hi user, write what u want to send to the server:
      If you wanna log in, press L
      If you wanna register as a new user, press R
      Once logged in If you want to send a question, press Q
      If you'd like to answer any of the questions, press V to view the questions
      If you want to answer any of the questions, press a number, followed by the option then 
      enter, for example to answer the second question with option b would be to type
      "2 b" and then enter.
      Press D to view the leaderboard, and at anytime u need, write help to see this message""")


while True:
    thread = threading.Thread(target=checkrec, args=())
    thread.start()
    mass = input();
    if mass == "help":
        print(f"""Hi user, write what u want to send to the server:
      If you wanna log in, press L
      If you wanna register as a new user, press R
      Once logged in If you want to send a question, press Q
      If you'd like to answer any of the questions, press V to view the questions
      If you want to answer any of the questions, press a number, followed by the option then 
      enter, for example to answer the second question with option b would be to type
      "2 b" and then enter.
      Press D to view the leaderboard, and at anytime u need, write help to see this message""")
    if mass == "Q":
        add_question()
    if mass == "R":
        usr = input()
        pswd = input()
        string = f"newusr {usr} {pswd}"
        send(string)
    if mass == "L":
        usr = input()
        pswd = input()
        string = f"login {usr} {pswd}"
        send(string)
    else: 
        send(mass); 
     



