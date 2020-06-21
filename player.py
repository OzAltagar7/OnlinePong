import pygame

class Player:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 1

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP]:
            self.y -= self.speed

        if keys_pressed[pygame.K_DOWN]:
            self.y += self.speed

        if keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed       

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def __str__(self):
        return f"PLAYER | LOCATED AT {(self.x, self.y)}, WITH RADIUS OF {self.radius}, COLOR OF {self.color} AND A SPEED OF {self.speed}"
