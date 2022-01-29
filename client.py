import socket

HOST = '127.0.0.1'
PORT = 12345
BUFFER = 1024
acceptable_commands = ['hello', 'time', 'date', 'dow']


class Client:
    def __init__(self, host, port):
        self.client_socket = None
        self.host = host
        self.port = port
        self.connected = False

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to {self.client_socket.getpeername()}")
            self.connected = True
        except socket.error:
            print("Couldn't connect to server. Is it running?")
            self.connected = False

    def send_message(self, message):
        if self.connected:
            try:
                self.client_socket.send(message.encode())
                return self.client_socket.recv(BUFFER).decode()
            except socket.error:
                print("Couldn't send message. Server might be down. Try connecting again.")
                self.connected = False

    def close(self):
        self.client_socket.close()
        self.connected = False


client = Client(HOST, PORT)

while True:
    try:
        usr_input = input("Client: ")
    except KeyboardInterrupt:
        print("Interrupted by Keyboard. Quitting...")
        break
    if usr_input.lower() == 'connect':
        if not client.connected:
            client.connect()
        else:
            print("You are already connected!")
    elif client.connected:
        if usr_input.lower() in acceptable_commands:
            resp = client.send_message(usr_input.lower())
            if resp:
                print("Server:", resp)
        elif usr_input == "bye":
            resp = client.send_message(usr_input.lower())
            if resp:
                print("Server:", resp)
            client.close()
        else:
            print("Not acceptable command!")
    else:
        if usr_input.lower() in ('bye', 'quit', 'exit'):
            break
        else:
            print("You are not connected!")
