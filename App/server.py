import socket  
import threading

def handle_client(connection, address):
    print(f"Accepted connection from {address}")
    while(True):
        data = connection.recv(1024)
        if not data:
            break
        print(f"Received: {data} from address: {address}")
        connection.sendall(b"+PONG\r\n")
    connection.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 6379))
    server_socket.listen(3)  
    print("Server is listening for connections")
    # Now we will wait for a client to connect and assign it to a new thread to achieve concurrency
    while True:
        connection, address = server_socket.accept()  # wait for client
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

if __name__ == "__main__":
    main()
