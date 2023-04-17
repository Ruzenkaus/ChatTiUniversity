import socket
import threading

host = '127.0.0.1'
port = 57391

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


# broadcast
def broadcast(message):
    for client in clients:
        client.send(message)


# handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


# receive
def receive():
    while True:
        client, addres = server.accept()
        print(f"Connected with {str(addres)}")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of client is {nickname}')
        broadcast(f"{nickname} connected\n".encode('utf-8'))
        client.send("Connected to server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Server running...")
receive()