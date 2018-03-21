#!/usr/bin/env python
"""
Vars that can change during game
"""

import pygame
from global_vars import *

# Sprites lists
intruders_sprites_list = pygame.sprite.Group()
player_ammo_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
intruders_ammo_sprites_list = pygame.sprite.Group()

# Player default start position
PLAYER_START_POS_X = (SCREEN_WIDTH / 2) - 35
PLAYER_START_POS_Y = SCREEN_HEIGHT - (70 * 2)

# Player characteristics
PLAYER_STARTING_LIVES = 3
LEVEL = 1

# Winning conditions
LOOSE = False

INTRUSIONS_COUNT = 0
RATE_OF_INTRUSIONS = 3
