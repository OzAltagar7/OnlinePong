import socket
import pygame

# The server's IP and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1235
SERVER_ADDRESS = (HOST, PORT)

# Header of the data transmitted indicating the length of the data.
# Before sending any data through the socket, a message with length HEADER_SIZE
# will be sent indicating the length of the incoming data
HEADER_SIZE = 8

# Screen dimensions
WIN_WIDTH = 750
WIN_HEIGHT = 750

# Player dimensions and initial position
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 120
P1_INIT_X, P1_INIT_Y = 50, WIN_HEIGHT/2 - PLAYER_HEIGHT/2
P2_INIT_X, P2_INIT_Y = 680, WIN_HEIGHT/2 - PLAYER_HEIGHT/2

# Ball dimensions
BALL_RADIUS = 7.5
BALL_INIT_X, BALL_INIT_Y = WIN_HEIGHT/2 - BALL_RADIUS, WIN_HEIGHT/2 - BALL_RADIUS

# The distance between two rectangles that counts as a collision
COLLISION_TOLERANCE = 10

# Score text
pygame.font.init()
SCORE_FONT = pygame.font.Font("Fonts/Roboto-Regular.ttf", 32)

# Game FPS
FPS = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)