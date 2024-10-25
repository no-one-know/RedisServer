import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 6379))
    while True:
        input_data = input("Enter command: ")
        if input_data == "exit":
            break
        client_socket.sendall(input_data.encode())
        data = client_socket.recv(1024)
        print("Response from server ", data.decode())
    client_socket.close()

if __name__ == "__main__":
    main()