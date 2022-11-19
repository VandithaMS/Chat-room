import socket
import threading

name=input("Enter ur name: ")
server = socket.gethostbyname(socket.gethostname())
port=55555

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((server,port))

def receive():
    while True:
        try:
            msg=client.recv(1024).decode('ascii')
            if msg=='Name: ':
                client.send(name.encode('ascii'))
            elif msg in ["1.Create new grp   2.join grp   3.Quit", "Name of grp: ", "Enter group name to join: "]:
                print(msg)
            else:
                print("msg: "+msg)
        except:
            print("An error occured!!..")
            client.close()
            break
        
def write():
    #msg= input()
    while True:
        
        msg= str(input())
        if msg!="q":
            #print("you: ",msg)
            client.send(msg.encode('ascii'))
        else:
            print("Exited...")
            client.close()
            exit()

receive_thread=threading.Thread(target=receive)
receive_thread.start()
print("started")
write_thread=threading.Thread(target=write)
write_thread.start()