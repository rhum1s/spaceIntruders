#!/usr/bin/env python
"""
Initiate and manage PyGame's display
"""

from global_vars import *
import pygame


class Display():
    """ PyGame display and screen refresh """
    def __init__(self, len_x, len_y, title, fps=60, bg_picture=None):
        self.len_x = len_x
        self.len_y = len_y
        self.title = title
        self.fps = fps
        self.bg_picture = bg_picture

        self.size = (self.len_x, self.len_y)

        pygame.mixer.pre_init(44100, -16, 2, 2048)  # Prevents sounds lag
        pygame.init()
        pygame.mixer.init()  # For sounds
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        # pygame.mouse.set_visible(False)  # Hide the mouse cursor
        self.clock = pygame.time.Clock()  # Used to manage how fast the screen updates
        if self.bg_picture:
            self.background_image = pygame.image.load(bg_picture).convert()  # .convert_alpha()  # For transparency

    def modify_background_image(self, image):
        self.background_image = pygame.image.load(image).convert()

    def prepare_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, [0, 0])

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.fps)


class Button():
    def __init__(self, screen, x, y, width, height, colors, text="", text_color=(0, 0, 0), action=None):
        """
        Creates a button activating a function.
        :param screen: pygame.display
        :param colors: List of default and hover colors. Ex: [(200,0,0), (250,0,0)]
        :param action: A function object (without '()')
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colors, self.color_default, self.color_hover = colors, colors[0], colors[1]
        self.text = text
        self.text_color = text_color
        self.action = action

        self.font = pygame.font.SysFont('Agency FB', 20, True, False)
        self.button_text = self.font.render(self.text, True, self.text_color)

        self.hover_sound = pygame.mixer.Sound("sounds/Pen_Clicks_v2.wav")
        self.hover_sound.set_volume(0.4)
        self.sound_played = False  # Used to not plays sound in loop on hover

    def place_text(self):
        """
        Print text centered in button
        """
        self.screen.blit(
            self.button_text, [
                (self.x + (self.width / 2)) - (self.button_text.get_width() / 2),
                (self.y + (self.height / 2)) - (self.button_text.get_height() / 2)])

    def draw(self):
        """
        Calculate and draw everything.
        Must be done each frame
        """
        mouse_pos = pygame.mouse.get_pos()
        click_pos = pygame.mouse.get_pressed()  # Tuple (left, center, right)

        # If mouse in button highlight ...
        if self.x + self.width > mouse_pos[0] > self.x and self.y + self.height > mouse_pos[1] > self.y:

            # Play sound if mouse just hovered
            if self.sound_played is False:
                self.hover_sound.play()
                self.sound_played = True

            pygame.draw.rect(self.screen, self.color_hover, (self.x, self.y, self.width, self.height))

            # ... And allow click to launch action
            if click_pos[0] == 1 and self.action is not None:  # If left click
                self.hover_sound.play()
                self.action()
        else:
            self.sound_played = False
            pygame.draw.rect(self.screen, self.color_default, (self.x, self.y, self.width, self.height))

        # Anyway, place text
        self.place_text()


def pause(window):
    # Print pause text
    font = pygame.font.SysFont('Calibri', 40, True, False)
    text = font.render("PAUSE", True, WHITE)
    window.screen.blit(text, [(SCREEN_WIDTH / 2) - (text.get_width() / 2),
                              (SCREEN_HEIGHT / 2) - (text.get_height() / 2)])
    window.update()

    # Manage pause, restart or quit
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            break
        if event.type == pygame.QUIT:
            pygame.quit()


def quit_game():
    pygame.quit()
    quit()