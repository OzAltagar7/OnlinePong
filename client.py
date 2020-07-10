import socket
import pickle
from game_settings import SERVER_ADDRESS, HEADER_SIZE

class Client:
    """
    Used for handling a client connection to the server.

    Attributes:
        server_address (string, int): The server's address (host, port).
        header_size (int): Header of the data transmitted indicating the length of the data.
        client_socket (socket): The client-side socket of the connection.
    """

    def __init__(self, server_address = SERVER_ADDRESS, header_size = HEADER_SIZE):
        """
        Constructor of the Client class.

        Args:
            server_address ((string, int), optional): The server's address (host, port). Defaults to SERVER_ADDRESS.
            header_size (int, optional): Header of the data transmitted indicating the length of the data. Defaults to HEADER_SIZE.
        """

        self.server_address = server_address
        self.header_size = header_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_data(self, data):
        """
        Send data to the server.

        Args:
            data (Any): The data that's being sent.
        """

        # In order for the data to be transmitted, it has to be in bytes format
        pickled_data = pickle.dumps(data)
        # Actual length of the data (for example 3) 
        data_length = len(pickled_data)
        # Padded length of the data (for example '3      '. *Not of type string)
        padded_length = pickle.dumps(data_length)
        padded_length += b' ' * (self.header_size - len(padded_length))

        # Send the padded length and then the data right after
        self.client_socket.send(padded_length)
        self.client_socket.send(pickled_data)

    def receive_data(self):
        """
        Receive data from the server.

        Returns:
            Any: The data that was received.
        """

        # Receive the first message (the header),
        # which indicates the incoming data length
        data_length = int(pickle.loads(self.client_socket.recv(self.header_size)))
        
        if data_length:
            # Receive the data itself
            data = pickle.loads(self.client_socket.recv(data_length))

        return data

    def close_connection(self):
        """End the connection to the server."""

        self.client_socket.close()