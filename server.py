import threading
import socket

host=socket.gethostbyname(socket.gethostname())
port=55555
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))

clients=dict()
names=dict()
grp=[]
mem=[]
server.listen(20)
print("Connected")

def broadcast(msg,client):
    val=clients.get(client)
    i=grp.index(val)
    for client in mem[i]:
        client.send(msg)
        
def handle(client):
    while True:
        try:
            msg=client.recv(1024)
            broadcast(msg,client)
        except:
            index=clients.get(client)
            del clients[client]
            grp.pop(index)
            mem[index].remove(client)
            name=names[index]
            names.remove(name)
            broadcast(f"{name} exited!!..".encode('ascii'),client)
            break

def create(client):
    client.send("Name of grp: ".encode('ascii'))
    l=client.recv(1024).decode('ascii')
    grp.append(l)
    l=list()
    l.append(client)
    mem.append(l)
    print("new grp "+str(grp[-1])+ " is created")
    client.send("welcome!...".encode('ascii'))
    clients[client]=grp[-1]
    
def receive():
    while True:
        client,addr=server.accept()
        print("Connected with ",addr)
        
        client.send("Name: ".encode("ascii"))
        name=client.recv(1024).decode("ascii")
        names[client]=name
        print(f"{name} has joined!!..")
        def input():
            client.send("1.Create new grp   2.join grp   3.Quit".encode('ascii'))
            x=client.recv(1024).decode('ascii')
            if x not in ['1','2','3']:
                client.send("Invalid input!!...".encode('ascii'))
                print()
                input()
            elif x=='1':
                create(client)
                
            elif x=='2':
                client.send("Enter group name to join: ".encode('ascii'))
                n=client.recv(1024).decode('ascii')
                if n in grp:
                    i=grp.index(n)
                    mem[i].append(client)
                    clients[client]=n
                    broadcast(f"{name} joined grp!!...".encode('ascii'),client)
                else:
                    client.send("Group doesn't exist!!....".encode('ascii'))
                    client.close()
                    
            elif x=='3':
                client.close()
        
        input()
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()
        
receive()

