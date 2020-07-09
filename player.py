import pygame
from game_settings import PLAYER_WIDTH, PLAYER_HEIGHT, WHITE, WIN_HEIGHT

class Player:
    def __init__(self, x, y, width = PLAYER_WIDTH, height = PLAYER_HEIGHT, color = WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 10

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP] and self.rect.top - self.speed >= 0:
            self.rect.y -= self.speed

        if keys_pressed[pygame.K_DOWN] and self.rect.bottom + self.speed <= WIN_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
