import socket
import pickle
import os

# The server's IP and port
SERVER_IP = "192.168.1.187"
PORT = 1235
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

    def receive_data():
        # Receive the first message (the header),
        # which indicates the incoming data length
        data_length = int(pickle.loads(client_socket.recv(HEADER_SIZE)))
        
        # Check wether the data is not None
        if data_length:
            # Receive the data itself
            data = pickle.loads(client_socket.recv(data_length))

            # Print the incoming message
            print(f"[{SERVER_ADDRESS[0], SERVER_ADDRESS[1]}] {data}")

    while True:
        data = input("WHAT WOULD YOU LIKE TO SEND TO THE SERVER? ")
        send_data(data)

        # In case the user disconnected
        if data == DISCONNECT_MESSAGE:
            break

        receive_data()
    
    client_socket.close()

if __name__ == "__main__":
    main()