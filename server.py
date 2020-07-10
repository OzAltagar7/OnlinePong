import socket
import threading
import pickle
import os
import pygame
from game_manager import GameManager
from game_settings import HEADER_SIZE, SERVER_ADDRESS

# Number of active connections to the server.
active_connections = 0

# An object for managing the game
game_manager = GameManager()

def handle_client(conn, addr):
    """
    Handle a connection with a single client.

    Args:
        conn (Socket): The server-side connection socket
        addr ((string, int)): The client's address (IP, PORT)
    """

    global active_connections
    active_connections += 1
    print(f"[NEW CONNECTION] ESTABLISHED A NEW CONNECTION WITH {addr}, [ACTIVE CONNECTIONS] {active_connections}")

    # A unique identifier for each connection. *starts from 0 up to infinity
    connection_number = active_connections - 1

    def send_data(data):
        """
        Send data to the client.

        Args:
            data (Any): The data that's being sent.
        """

        # In order for the data to be transmitted, it has to be in bytes format
        pickled_data = pickle.dumps(data)
        # Actual length of the data (for example 3) 
        data_length = len(pickled_data)
        # Padded length of the data (for example '3      ')
        padded_length = pickle.dumps(data_length)
        padded_length += b' ' * (HEADER_SIZE - len(padded_length))

        # Send the padded length and then the data right after
        conn.send(padded_length)
        conn.send(pickled_data)

    def receive_data():
        """
        Receive data from the client.

        Returns:
            Any: The data that was received.
        """

        # Receive the first message (the header),
        # which indicates the incoming data length
        data_length = int(pickle.loads(conn.recv(HEADER_SIZE)))
        
        # Check wether the data is not None
        if data_length:
            # Receive the data itself
            data = pickle.loads(conn.recv(data_length))

        return data

    try:
        # Generate a player and send it to the client
        send_data(game_manager.players[connection_number - 1])

        while True:
            # Wait for all players to connect
            if active_connections == 2:
                # Receive the player's Player object
                game_manager.players[connection_number - 1] = receive_data()

                # Send the opponent Player's object
                send_data(game_manager.players[connection_number - 2])

                # Move the ball and send it to the clients
                game_manager.move_ball() # Updates the score in case of a goal
                send_data(game_manager.ball)

                # Send the current game score to the clients
                send_data(game_manager.score)

    except:
        print(f"[CLIENT DISCONNECTED] {addr} HAS DISCONNECTED")

    # Close the connection socket in case of a break caused by a disconnection
    conn.close()
    active_connections -= 1


def main():
    """The main server function."""
    # Clear the terminal before a new run
    os.system('cls')    

    # Create the server_socket object and bind it to the desired address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    
    # Start listening for new connections
    server_socket.listen()
    print(f"[LISTENING] SERVER IS NOW LISTENING FOR NEW CONNECTIONS ON {SERVER_ADDRESS}")

    while True:
        # Accept a new connection
        conn, addr = server_socket.accept()
        # Start a new thread handling the new connection
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()