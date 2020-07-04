import socket
import threading
import pickle
import os
import pygame
from player import Player
from ball import Ball
from game_settings import *

# Number of active connections to the server.
active_connections = 0

# Contains both players Player objects
players = [Player(P1_INIT_X, P1_INIT_Y), Player(P2_INIT_X, P2_INIT_Y)]
# Holds the game ball (same for both players)
ball = Ball(BALL_INIT_X, BALL_INIT_Y)

def handle_client(conn, addr):
    global active_connections
    active_connections += 1
    print(f"[NEW CONNECTION] ESTABLISHED A NEW CONNECTION WITH {addr}, [ACTIVE CONNECTIONS] {active_connections}")

    # A unique identifier for each connection. *starts from 0 up to infinity
    connection_number = active_connections - 1

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

        return data

    try:
        # Generate a player and send it to the client
        send_data(players[connection_number - 1])

        while True:
            # Wait for all players to connect
            if active_connections == 2:
                # Receive the player's Player object
                players[connection_number - 1] = receive_data()

                # Send the opponent Player's object
                send_data(players[connection_number - 2])

                # Move the ball and send it to the clients
                ball.move(players[0], players[1])

                if ball.rect.x <= 0 or ball.rect.x >= WIN_WIDTH:
                    ball.reset()

                send_data(ball)

    except:
        print(f"[CLIENT DISCONNECTED] {addr} HAS DISCONNECTED")

    # Close the connection socket in case of a break caused by a disconnection
    conn.close()
    active_connections -= 1


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