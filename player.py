import pygame
from game_settings import WHITE

class Player:
    def __init__(self, x, y, width = 25, height = 100, color = WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP]:
            self.y -= self.speed

        if keys_pressed[pygame.K_DOWN]:
            self.y += self.speed 

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def __str__(self):
        return f"PLAYER | LOCATED AT {(self.x, self.y)}, COLOR OF {self.color} AND A SPEED OF {self.speed}"
