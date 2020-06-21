import socket
import threading
import pickle
import os
import pygame
import random
from player import Player
from colors import get_random_color

# The server's IP and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1235
SERVER_ADDRESS = (HOST, PORT)

# Header of the data transmitted indicating the length of the data.
# Before sending any data through the socket, a message with length HEADER_SIZE
# will be sent indicating the length of the incoming data
HEADER_SIZE = 8

# Number of active connections to the server.
# threading.active_count() includes the main program thread hence the minus one
active_connections = threading.active_count() - 1

# Contains all of the players connected to the server
players = []

def generate_player():
    # Generate a new random player and append it to the player's list
    player = Player(random.randint(0, 750), random.randint(0, 750), 2, get_random_color())
    players.append(player)
    return player

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] ESTABLISHED A NEW CONNECTION WITH {addr}, [ACTIVE CONNECTIONS] {active_connections}")

    connection_number = threading.active_count() - 1

    def send_data(data):
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
        # Receive the first message (the header),
        # which indicates the incoming data length
        data_length = int(pickle.loads(conn.recv(HEADER_SIZE)))
        
        # Check wether the data is not None
        if data_length:
            # Receive the data itself
            data = pickle.loads(conn.recv(data_length))

            # Print the incoming message
            print(f"[{addr[0], addr[1]}] {data}")

        return data

    try:
        # Generate a player and send it to the client
        send_data(generate_player())

        while True:
            # Wait for all players to connect
            if threading.active_count() - 1 == 2:
                # Receive the player's Player object
                players[connection_number - 1] = receive_data()
                # Send the opponent Player's object
                send_data(players[connection_number - 2])
    except:
        print(f"[CLIENT DISCONNECTED] {addr} HAS DISCONNECTED")

    # Close the connection socket in case of a break caused by a disconnection
    conn.close()


def main():
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