import pygame
from game_settings import PLAYER_WIDTH, PLAYER_HEIGHT, WHITE, WIN_HEIGHT

class Player:
    """
    Represent a player paddle.

    Attributes:
        rect (pygame.Rect): Rect object of the ball (x, y, width, height).
        color ((int, int, int)): The color of the player.
        speed (int): The player's speed (magnitude).
    """

    def __init__(self, x, y, width = PLAYER_WIDTH, height = PLAYER_HEIGHT, color = WHITE):
        """
        Constructor of the player class.

        Args:
            x (int): The player initial x position.
            y (int): The player initial y position.
            width (int, optional): The player's width. Defaults to PLAYER_WIDTH.
            height (int, optional): The player's height. Defaults to PLAYER_HEIGHT.
            color ((int, int, int)), optional): The color of the ball. Defaults to WHITE.
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 10

    def move(self):
        """Move the player according to user input."""

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP] and self.rect.top - self.speed >= 0:
            self.rect.y -= self.speed

        if keys_pressed[pygame.K_DOWN] and self.rect.bottom + self.speed <= WIN_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, win):
        """
        Draw the player.

        Args:
            win (pygame.Surface): the main game screen
        """

        pygame.draw.rect(win, self.color, self.rect)
