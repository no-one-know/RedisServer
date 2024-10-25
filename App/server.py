import socket  
import threading

valid_commands = ["ping", "info", "exit", "echo", "get", "set", "px"]

def parse_bulk_string(command):
    length = int(command[1])
    return command[2: 2+length]

def parse_simple_string(command):
    index = 1
    result = ""
    while True and index < len(command):
        if command[index] >= 'a' or command <= 'z':
            result += command[index]
        elif command[index] >= 'A' or command <= 'Z':
            result += command[index]
        else:
            break
        index += 1
    return result

def parse_numbers(command):
    index = 1
    result = ""
    while True and index < len(command):
        if command[index] >= '0' and command[index] <= '9':
            result += command[index]
        else:
            break
        index += 1
    return result

def parse_simple_error(command):
    index = 1
    result = ""
    while True and index < len(command):
        if command[index] >= 'a' or command <= 'z':
            result += command[index]
        elif command[index] >= 'A' or command <= 'Z':
            result += command[index]
        else:
            break
        index += 1
    return result

def parse_array(command):
    return parse_command(command[2:])

def parse_command(command):
    if len(command) == 0: return ""
    index = 0
    response = ""
    while index < len(command):
        if command[index] == '*': 
            result = parse_array(command[index:])
            return result
        elif command[index] == '$': 
            result = parse_bulk_string(command[index:])
            response += " " + result 
            index += len(result) + 2
        elif command[index] == '+': 
            result = parse_simple_string(command[index:])
            response += " " + result 
            index += len(result) + 1
        elif command[index] == '-': 
            result = parse_simple_error(command[index:])
            response += " " + result 
            index += len(result) + 1
        elif command[index] == ':': 
            result = parse_numbers(command[index:])
            response += " " + result 
            index += len(result) + 1
    return response.strip()
        
def parse_input_command_and_send_response(data, connection):
    command_after_removing_RESP_delimiter = ''.join(data.split('\r\n'))
    print("Command received: ", command_after_removing_RESP_delimiter)
    command_response = parse_command(command_after_removing_RESP_delimiter)
    print("Command response: ", command_response)
    if len(command_response) == 0:
        connection.sendall("-ERR unknown command\r\n".encode())
    command_attributes = command_response.split(' ')
    print("Command attributes: ", command_attributes)
    command = command_attributes[0]
    if command.lower() not in valid_commands:
        connection.sendall("-ERR unknown command\r\n".encode())
    if command.lower() == "ping":
        connection.sendall("+PONG\r\n".encode())
    elif command.lower() == "info":
        connection.sendall("+INFO\r\n".encode())
    elif command.lower() == "exit":
        connection.sendall("+OK\r\n".encode())
        connection.close()
    elif command.lower() == "echo":
        connection.sendall((f"${len(command_attributes[1])}"+"\r\n"+command_attributes[1]+"\r\n").encode())
    
def handle_client(connection, address):
    while(True):
        data = connection.recv(1024)
        if not data:
            break
        data = data.decode('utf-8').replace("\\n", "\n").replace("\\r", "\r").strip()
        # Now we will parse the input data and send the appropriate response
        parse_input_command_and_send_response(data, connection)
    connection.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 6379))
    server_socket.listen(3)  
    print("Server is listening on port 6379")
    # Now we will wait for a client to connect and assign it to a new thread to achieve concurrency
    while True:
        connection, address = server_socket.accept()  # wait for client
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

if __name__ == "__main__":
    main()
