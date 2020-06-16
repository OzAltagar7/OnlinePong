import socket
import pickle
import os

# The server's IP and port
SERVER_IP = "192.168.1.187"
PORT = 1234
SERVER_ADDRESS = (SERVER_IP, PORT)

# Header of the data transmitted indicating the length of the data.
# Before sending any data through the socket, a message with length HEADER_SIZE
# will be sent indicating the length of the incoming data
HEADER_SIZE = 8

# A disconnection message indicating the disconnecting of a client
# meaning closing the connection on the server-side
DISCONNECT_MESSAGE = "!DISCONNECT"

def main():
    # Clear the terminal before a new run
    os.system('cls')    

    # Create the client_socket object and connect it to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)

    def send_data(data):
        # In order for the data to be transmitted, it has to be in bytes format
        pickled_data = pickle.dumps(data)
        # Actual length of the data (for example 3) 
        data_length = len(pickled_data)
        # Padded length of the data (for example '3      ')
        padded_length = pickle.dumps(data_length)
        padded_length += b' ' * (HEADER_SIZE - len(padded_length))

        # Send the padded length and then the data right after
        client_socket.send(padded_length)
        client_socket.send(pickled_data)

    while True:
        send_data(input("MESSAGE: "))

if __name__ == "__main__":
    main()