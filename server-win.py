import socket, threading
connections = []

def receive_messages(connection: socket.socket, address: str) -> None:
    while True:
        try:
            msg = connection.recv(1024)
            if msg:                
                print(f'{address[0]}:{address[1]} - {msg.decode()}')                
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                send_to_clients(msg_to_send, connection)
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break


def send_to_clients(message: str, connection: socket.socket) -> None:
    for client_conn in connections:        
        if client_conn != connection:
            try:                
                client_conn.send(message.encode())
            except Exception as e:
                print('Error send_to_clientsing message: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    if conn in connections:        
        conn.close()
        connections.remove(conn)


PORT = 49999
    
try:        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', PORT))
    server.listen(4)

    print('Server running!')
    
    while True:
        client_socket, address = server.accept()            
        connections.append(client_socket)
        threading.Thread(target=receive_messages, args=[client_socket, address]).start()

except Exception as e:
    print(f'An error has occurred when instancing socket: {e}')
finally:        
    if len(connections) > 0:
        for conn in connections:
            remove_connection(conn)

    server.close()