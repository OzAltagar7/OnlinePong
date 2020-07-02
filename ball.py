import pygame
from game_settings import WHITE, WIN_WIDTH, WIN_HEIGHT
import random
import math

class Ball:
    def __init__(self, x = int(WIN_WIDTH/2), y = int(WIN_HEIGHT/2), radius = 5, color = WHITE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 3
        self.moving_direction = [random.choice([1, -1]), random.choice([1, -1])]

    def move(self, p1, p2):
        self.x += self.speed * self.moving_direction[0]
        self.y += self.speed * self.moving_direction[1]

        if (self.y - self.radius) <= 0 or (self.y + self.radius) >= WIN_HEIGHT:
            self.moving_direction[1] = 1 if self.moving_direction[1] == -1 else -1
        
        # When being called, p1 and p2 has to be in the correct order!
        # p1 corrusponds to the left player and p2 to the right one
        if ((self.x + self.radius) >= p2.x and ((self.y - self.radius) >= p2.y and (self.y + self.radius) <= (p2.y + p2.height))) or \
            ((self.x - self.radius) <= (p1.x + p1.width) and ((self.y - self.radius) >= p1.y and (self.y + self.radius) <= (p1.y + p1.height))):
            self.moving_direction[0] = 1 if self.moving_direction[0] == -1 else -1

    def reset(self):
        self.x = int(WIN_WIDTH/2)
        self.y = int(WIN_HEIGHT/2)
        self.moving_direction = [random.choice([1, -1]), random.choice([1, -1])]

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)