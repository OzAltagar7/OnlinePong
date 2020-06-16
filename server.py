import socket
import threading
import pickle
import os

from client import A

# The server's IP and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1234
SERVER_ADDRESS = (HOST, PORT)

# Header of the data transmitted indicating the length of the data.
# Before sending any data through the socket, a message with length HEADER_SIZE
# will be sent indicating the length of the incoming data
HEADER_SIZE = 8

# A disconnection message indicating the disconnecting of a client
# meaning closing the connection on the server-side
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] ESTABLISHED A NEW CONNECTION WITH {addr}, [ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    connected = True
    while connected:
        # Receive the first message (the header),
        # which indicates the incoming data length
        data_length = int(pickle.loads(conn.recv(HEADER_SIZE)))
        
        # Check the data is not None
        if data_length:
            # Receive the data itself
            data = pickle.loads(conn.recv(data_length))

            # Handle a client disconnection
            if data == DISCONNECT_MESSAGE:
                print(f"[CLIENT DISCONNECTED] {addr} HAS DISCONNECTED")
                connected = False
            else:
                # Print the incoming message
                print(f"[{addr[0], addr[1]}] {data}")
    
    # Close the connection socket
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
        client_thread.join()

        # All clients have disconnected
        if threading.active_count() - 1 == 0:
            print("[SERVER DISCONNECTED] NO MORE CLIENTS LEFT")
            break
    
    server_socket.close()

if __name__ == "__main__":
    main()