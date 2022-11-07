import socket, threading

def receive_messages(connection: socket.socket):
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 49999

try:
    client_socket = socket.socket()
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    threading.Thread(target=receive_messages, args=[client_socket]).start()

    print('Connected to chat!')
    while True:
        msg = input()
        if msg == 'quit':
            break
        client_socket.send(msg.encode())
    client_socket.close()

except Exception as e:
    print(f'Error connecting to server socket {e}')
    client_socket.close()