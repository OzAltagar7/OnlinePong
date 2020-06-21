import random

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

colors = [RED, WHITE, YELLOW, BLUE]

def get_random_color():
    random_color = random.choice(colors)
    colors.remove(random_color)
    return random_color