from player import Player
from ball import Ball
from game_settings import P1_INIT_X, P1_INIT_Y, P2_INIT_X, P2_INIT_Y, BALL_INIT_X, BALL_INIT_Y, WIN_WIDTH, WIN_HEIGHT

class GameManager:
    def __init__(self):
        self.players = [Player(P1_INIT_X, P1_INIT_Y), Player(P2_INIT_X, P2_INIT_Y)]
        self.ball = Ball(BALL_INIT_X, BALL_INIT_Y)
        self.score = [0,0]

    def move_ball(self):
        self.ball.move(self.players[0], self.players[1])
        if self.ball.rect.x <= 0 or self.ball.rect.x >= WIN_WIDTH:
            self.update_score()
            self.ball.reset()

    def update_score(self):
        if self.ball.rect.x <= 0:
            self.score[0] += 1

        elif self.ball.rect.x >= WIN_WIDTH:
            self.score[1] += 1

    
