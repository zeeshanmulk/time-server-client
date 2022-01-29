import socket
import sys
from datetime import datetime
from threading import Thread, active_count, Event

BUFFER = 1024
HOST = '127.0.0.1'
PORT = 12345

exit_event = Event()


class Server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((host, port))
            print(f"Listening on port {port}")
        except socket.error:
            print("Socket binding failed!")
            sys.exit(0)

    @staticmethod
    def send_msg(client_socket, message):
        try:
            client_socket.send(message.encode())
        except socket.error:
            print("Sending message failed.")

    def listen(self):
        self.socket.settimeout(1.0)
        self.socket.listen(100)
        while True:
            try:
                client_socket, address = self.socket.accept()
                print("Socket up and running with a connection from ", address)
                Thread(target=self.process_requests, args=(client_socket,)).start()
                print(f"Number of connections: {active_count() - 1}")
            except socket.timeout:
                continue
            except socket.error:
                print("A network error has occurred. Quitting...")
                break
            except KeyboardInterrupt:
                print("Interrupted by Keyboard. Quitting...")
                exit_event.set()
                break
        self.socket.close()

    def process_requests(self, client_socket):
        client_socket.settimeout(1.0)
        while True:
            if exit_event.is_set():
                break

            try:
                received_data = client_socket.recv(BUFFER).decode()
            except socket.timeout:
                continue
            except socket.error:
                print("A network error has occurred!")
                break

            date_time = datetime.now()
            if received_data:
                match received_data:
                    case 'hello':
                        self.send_msg(client_socket, f'Hello there client {client_socket.getpeername()}')
                    case 'bye':
                        self.send_msg(client_socket, "Bye")
                        break
                    case 'time':
                        time_str = date_time.strftime("%H:%M:%S")
                        self.send_msg(client_socket, time_str)
                    case 'date':
                        date_str = date_time.strftime("%B %d, %Y")
                        self.send_msg(client_socket, date_str)
                    case 'dow':
                        dow_str = date_time.now().today().strftime('%A')
                        self.send_msg(client_socket, dow_str)
                    case _:
                        self.send_msg(client_socket, "Command not recognized!")
        print(f"Session {client_socket.getpeername()} terminated.")
        client_socket.close()


if __name__ == "__main__":
    Server(HOST, PORT).listen()
