import os
import pygame
from client import Client
from player import Player



def main():
    # Create a game window with dimensions of 750 X 750
    win = pygame.display.set_mode((750, 750))

    # Client object for handling the connection to the server.
    # When connecting, the server will send a random Player object
    # which will serve as the player
    player_client = Client()
    p1 = player_client.receive_data()

    def redraw_window():
        p1.draw(win)
        p2.draw(win)

        pygame.display.update()

    run = True
    FPS = 60
    clock = pygame.time.Clock()
    while run:
        # Make the game run at a constant speed independent on the machine it runs on
        clock.tick(FPS)

        # Send the player's Player object to the server
        player_client.send_data(p1)
        
        try:
            # Receive the opponent's Player object from the server
            p2 = player_client.receive_data()
        except:
            break
        
        p1.move()
        redraw_window()

        # Handle user exit button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    # In case of a break in the main game loop,
    # close the game window and the connection to the server
    pygame.quit()
    player_client.close_connection()

if __name__ == "__main__":
    main()