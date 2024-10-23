import socket  # noqa: F401


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 6379))
    server_socket.listen(2)  # 5 is the maximum number of clients that can be queued
    print("Server is listening for connections")
    connection, address = server_socket.accept()  # wait for client
    print(f"Connection from {address}")
    while(True):
        data = connection.recv(1024)
        if not data:
            break
        print(f"Received: {data}")
        connection.sendall(b"+PONG\r\n")
    connection.close()

if __name__ == "__main__":
    main()
