import os
import pygame
from client import Client
from player import Player
from ball import Ball
from text_manager import TextManager
from game_settings import WIN_WIDTH, WIN_HEIGHT, WIN_CAPTION, GAME_ICON, WAITING_FOR_OPPONENT, WHITE, BLACK, FPS, init_window

def main():
    """The main game function."""
    # Initialize the pygame module
    pygame.init()
    clock = pygame.time.Clock()

    # Create the main game window
    win = init_window()

    # Client object for handling the connection to the server.
    # When connecting, the server will send a random Player object
    # which will serve as the player
    player_client = Client()
    p1 = player_client.receive_data()

    # Manager of the game text
    text_manager = TextManager(win)

    def redraw_window():
        """Clear the screen and render a new frame."""

        # Clear the screen by coloring it black
        win.fill(BLACK)
        # Draw the middle line the display the score
        pygame.draw.aaline(win, WHITE, (WIN_WIDTH/2, 0), (WIN_WIDTH/2, WIN_HEIGHT))
        text_manager.display_score(score)

        # Draw the players and the ball
        p1.draw(win)
        p2.draw(win)
        ball.draw(win)

        # Update the screen
        pygame.display.update()

    run = True
    while run:
        # Make the game run at a constant speed independent on the machine it runs on
        clock.tick(FPS)

        p1.move()

        # Send the player's Player object to the server
        player_client.send_data(p1)
        
        # Receive the opponent, the ball and the score from the server
        p2 = player_client.receive_data()
        ball = player_client.receive_data()
        score = player_client.receive_data()
        
        redraw_window()

        # Handle a user exit button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    # close the game window and the connection to the server
    pygame.quit()
    player_client.close_connection()

if __name__ == "__main__":
    main()