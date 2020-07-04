import socket
import pickle
from game_settings import *

class Client:
    def __init__(self, server_address = SERVER_ADDRESS, header_size = HEADER_SIZE):
        self.server_address = server_address
        self.header_size = header_size
        # Create the client_socket object and connect it to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_data(self, data):
        # In order for the data to be transmitted, it has to be in bytes format
        pickled_data = pickle.dumps(data)
        # Actual length of the data (for example 3) 
        data_length = len(pickled_data)
        # Padded length of the data (for example '3      ')
        padded_length = pickle.dumps(data_length)
        padded_length += b' ' * (self.header_size - len(padded_length))

        # Send the padded length and then the data right after
        self.client_socket.send(padded_length)
        self.client_socket.send(pickled_data)

    def receive_data(self):
        # Receive the first message (the header),
        # which indicates the incoming data length
        data_length = int(pickle.loads(self.client_socket.recv(self.header_size)))
        
        # Check wether the data is not None
        if data_length:
            # Receive the data itself
            data = pickle.loads(self.client_socket.recv(data_length))

        return data

    def close_connection(self):
        self.client_socket.close()