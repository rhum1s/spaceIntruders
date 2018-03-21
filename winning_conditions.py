#!/usr/bin/env python
"""
Manage score, win and loose conditions
"""

from game_vars import *


class ScoreBoard():
    def __init__(self, score, lives, window):
        self.score = score
        self.lives = lives

        self.font = pygame.font.SysFont('Agency FB', 25, True, False)

        self.score_text = ""
        self.lives_text = ""

        self.window = window

    def increase_score(self, i):
        self.score = str(int(self.score) + i)

    def decrease_score(self, i):
        self.score = str(int(self.score) - i)

    def decrease_lives(self, i):
        self.lives = str(int(self.lives) - i)

    def reset(self):
        self.score = "0"
        self.lives = int(PLAYER_STARTING_LIVES)

    def draw(self):
        # Lives number displayed cannot be negative but we need to test this var so use another one for display
        if int(self.lives) < 0:
            lives_txt = "0"
        else:
            lives_txt = self.lives
        # Idem for score
        if int(self.score) < 0:
            score_txt = "0"
        else:
            score_txt = self.score

        self.score_text = self.font.render("SCORE: %s" % score_txt, True, WHITE)
        self.lives_text = self.font.render("LIVES: %s" % lives_txt, True, WHITE)

        self.window.screen.blit(self.score_text, [10, 10])
        self.window.screen.blit(self.lives_text, [10, 35])