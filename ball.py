import pygame
from game_settings import BALL_RADIUS, WHITE, WIN_WIDTH, WIN_HEIGHT, COLLISION_TOLERANCE, BALL_INIT_X, BALL_INIT_Y
import random
import math

class Ball:
    """
    The game ball.

    Attributes:
        rect (pygame.Rect): Rect object of the ball (x, y, width, height).
        color ((int, int, int)): The color of the ball.
        speed (int): The ball's speed (magnitude).
        moving_direction ([int, int]): The ball moving direction along the [XY] plane
    """

    def __init__(self, x, y, radius = BALL_RADIUS, color = WHITE):
        """
        Constructor of the Ball class.

        Args:
            x (int): The ball initial x position.
            y (int): The ball initial y position.
            radius (int, optional): The ball radius. Defaults to BALL_RADIUS.
            color ((int, int, int)), optional): The color of the ball. Defaults to WHITE.
        """

        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.color = color
        self.speed = 3
        self.moving_direction = [random.choice([1, -1]), random.choice([1, -1])]

    def move(self, p1, p2):
        """
        Move the ball around and apply collisions with other objects.

        Args:
            p1 (Player): The left player.
            p2 (Player): The right player.
        """

        # Handle collisions with the top and bottom of the screen
        if self.rect.top <= 0 or self.rect.bottom >= WIN_HEIGHT:
            self.moving_direction[1] *= -1

        # Handle collisions with the players
        if (self.rect.colliderect(p1.rect) and self.moving_direction[0] < 0) or \
            (self.rect.colliderect(p2.rect) and self.moving_direction[0] > 0):
            # Handle collisions from the side of the player
            if abs(self.rect.left - p1.rect.right) <= COLLISION_TOLERANCE or \
                abs(self.rect.right - p2.rect.left) <= COLLISION_TOLERANCE:
                self.moving_direction[0] *= -1

           # Handle collisions from the top of the player
            if (abs(self.rect.bottom - p1.rect.top) <= COLLISION_TOLERANCE and self.moving_direction[1] > 0) or \
                (abs(self.rect.top - p1.rect.bottom) <= COLLISION_TOLERANCE and self.moving_direction[1] < 0) or \
                (abs(self.rect.bottom - p2.rect.top) <= COLLISION_TOLERANCE and self.moving_direction[1] > 0) or \
                (abs(self.rect.top - p2.rect.bottom) <= COLLISION_TOLERANCE and self.moving_direction[1] < 0):
                self.moving_direction[1] *= -1

        self.rect.x += self.speed * self.moving_direction[0]
        self.rect.y += self.speed * self.moving_direction[1]
            
    def reset(self):
        """Reset the ball to it's starting position."""

        self.rect.x = BALL_INIT_X
        self.rect.y = BALL_INIT_Y
        self.moving_direction = [random.choice([1, -1]), random.choice([1, -1])]

    def draw(self, win):
        """
        Draw the ball.

        Args:
            win (pygame.Surface): the main game screen
        """

        pygame.draw.ellipse(win, self.color, self.rect)