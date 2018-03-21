#!/usr/bin/env python
"""
Manage sprite sheets.
"""

import pygame
# from global_vars import *


def create_frames(sprite_sheet_picture, frames_x, frames_y):
    """
    Create frames list by taking images from sprites sheet picture.
    :param sprite_sheet_picture: The pictures containing sprites sub pictures
    :param frames_x: Number of sprites horizontally
    :param frames_y: Number of sprites vertically
    :return: list of frames (images)
    """
    # sprite_sheet = SpriteSheet(sprite_sheet_picture)  # Load image as a SpriteSheet object
    # for y_image in xrange(frames_y):  # N images to take in x
    #     for x_image in xrange(frames_x):  # N images to take  in y
    #         frames.append(sprite_sheet.get_image(
    #             sprite_sheet.width / frames_x * x_image,
    #             sprite_sheet.height / frames_y * y_image,
    #             sprite_sheet.width / frames_x,
    #             sprite_sheet.height / frames_y))
    #
    # return frames

    frames = []

    image = pygame.image.load(sprite_sheet_picture).convert_alpha()
    width = image.get_size()[0]
    height = image.get_size()[1]

    for y_image in xrange(frames_y):  # N images to take in x
        for x_image in xrange(frames_x):  # N images to take  in y

            image.set_clip(pygame.Rect(
                width / frames_x * x_image,
                height / frames_y * y_image,
                width / frames_x,
                height / frames_y
            ))
            frame = image.subsurface(image.get_clip())  # Extract the sprite you want

            frames.append(frame)

    return frames