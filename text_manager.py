from game_settings import SCORE_FONT, WHITE, WIN_WIDTH

class TextManager:
    def __init__(self, win):
        self.win = win

    def display_score(self, score):
        p1_score, p2_score = SCORE_FONT.render(f"{score[0]}", False, WHITE), SCORE_FONT.render(f"{score[1]}", False, WHITE)
        self.win.blit(p1_score, (WIN_WIDTH/2 - 200 - p1_score.get_size()[0], 200))
        self.win.blit(p2_score, (WIN_WIDTH/2 + 200, 200))