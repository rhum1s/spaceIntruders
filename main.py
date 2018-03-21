#!/usr/bin/env python
"""
Space Intruders
"""

__version__ = "3.0.1"

import random

# Load program modules
from game_vars import *
from display import Display, Button, pause, quit_game
from winning_conditions import ScoreBoard
from spaceships import Spaceship, Intruder, IntruderCrazy, IntruderShooting, Boss


def manage_inputs(events):
    global player
    global LOOSE

    # Keys pressed once
    for e in events:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_w:  # Auto destruction
            player.explode()
            LOOSE = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:  # Pause game
            pause(window)

    # Player movement while key down
    keys = pygame.key.get_pressed()  # Checking pressed keys
    if keys[pygame.K_UP]:
        player.move("forward")
    if keys[pygame.K_DOWN]:
        player.move("backward")
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")
    if keys[pygame.K_SPACE]:
        player.shoot()


def manage_events():
    global LOOSE

    # If player's ammo hit an intruder explode it and add score
    for ammo in player_ammo_sprites_list:

        # Create a list of intruders not already exploding and check collisions with ammo
        intruders_not_exploding = [intruder for intruder in intruders_sprites_list if intruder.exploded is False]
        intruders_hit_list = pygame.sprite.spritecollide(ammo, intruders_not_exploding, False)  # Do kill set to False

        # Set intruders hit to explode (then explosion managed)
        [intruder.explode() for intruder in intruders_hit_list]

        # Ammo must be destroyed too if has hit
        if len(intruders_hit_list) > 0:
            ammo.explode()

        # Increase score
        score.increase_score(len(intruders_hit_list))

    # If player's ammo hit an intruder's ammo
    for player_ammo in player_ammo_sprites_list:

        # Create a list of intruders not already exploding and check collisions with ammo
        # intruders_not_exploding = [intruder for intruder in intruders_sprites_list if intruder.exploded is False]
        intruders_ammo_hit_list = pygame.sprite.spritecollide(player_ammo, intruders_ammo_sprites_list, False)

        # Set intruders hit to explode (then explosion managed)
        # [ammo.explode() for ammo in intruders_ammo_hit_list]
        for ammo in intruders_ammo_hit_list:
            if ammo.exploded is False:
                print "MUST EXPLODE"
                ammo.explode()

        if len(intruders_ammo_hit_list) > 0:
            player_ammo.explode()
        # FIXME: One of the two ammunition must explode, the other one be killed.

    # If intruder's ammo hit player
    if player.exploded is False:

        for ammo in intruders_ammo_sprites_list:

            # Create a list of intruders not already exploding and check collisions with ammo
            player_hits_list = pygame.sprite.spritecollide(ammo, [player], False)  # Do kill set to False

            # Player loose life or explode
            if len(player_hits_list) > 0 and player.sparkle is False:
                # player.explode()
                score.decrease_lives(1)
                player.lost_life()

            # Ammo must be destroyed too if has hit (or ammo kill and player explode)
            if len(player_hits_list) > 0:
                if int(score.lives) >= 0:
                    ammo.explode()
                else:
                    ammo.kill()

    # If intruder invade earth decrease score
    for intruder in intruders_sprites_list:
        if intruder.rect.y >= SCREEN_HEIGHT:
            score.decrease_score(1)
            intruder.kill()  # intruder.remove()

    # If intruder hits player
    intruders_able_to_hit = [intruder for intruder in intruders_sprites_list if intruder.has_hit_player is False]
    intruders_hitting_player = pygame.sprite.spritecollide(player, intruders_able_to_hit, False)
    if len(intruders_hitting_player) > 0 and player.sparkle is False:  # Loose life only if not sparkling
        score.decrease_lives(1)
        player.lost_life()
    for intruder in intruders_hitting_player:
        if intruder.__class__.__name__ != 'Boss':
            intruder.has_hit_player = True
            if int(score.lives) >= 0:  # Intruder explode if player still has lives otherwise player explode.
                intruder.explode()
            else:
                intruder.kill()

    # Loosing conditions
    if ((int(score.lives) < 0) or (int(score.score) < 0)) and LOOSE is False:
        LOOSE = True
        player.explode()

    # If player died then we go to loosing screen
    if player.died is True:
        manager.go_to(LoosingScreen())

    # Winning conditions depending on scene max score:
    if int(score.score) >= manager.scene.max_score and LOOSE is False and player.exploded is False:
        manager.go_to(WinningScreen())
    # Winning boss
    for intruder in intruders_sprites_list:
        if intruder.__class__.__name__ == 'Boss':
            if intruder.died is True:
                manager.go_to(WinningScreenFinal())


def move_sprites():
    for sprite in all_sprites_list:
        # Move ammo
        if sprite.__class__.__name__ == 'Ammunition':
            sprite.move()
        if sprite.__class__.__name__ == 'IntruderAmmunition':
            sprite.move()

        # Move intruders
        if sprite.__class__.__name__ == 'Intruder':
            sprite.move()
        if sprite.__class__.__name__ == 'IntruderCrazy':
            sprite.move()
        if sprite.__class__.__name__ == 'IntruderShooting':
            sprite.move()
        if sprite.__class__.__name__ == 'Boss':
            sprite.move()


def make_intruders_appear(type_of_intruder):
    global INTRUSIONS_COUNT

    if INTRUSIONS_COUNT == 0:  # If intruders allowed to appear

        # Empty intruders coordinates list used for intruders to do not overlap
        intruders_coordinates_x, intruders_coordinates_y = [], []

        for i in xrange(random.randint(0, RATE_OF_INTRUSIONS)):  # Create random number of intruders

            # Create x, y random value not already in the appearing list (overlapping)
            x_values = [i for i in xrange(SCREEN_WIDTH - INTRUDER_PICTURE_WIDTH) if i not in intruders_coordinates_x]
            y_values = [i for i in xrange(-60 - INTRUDER_PICTURE_HEIGHT, -5 - INTRUDER_PICTURE_HEIGHT)
                        if i not in intruders_coordinates_y]

            x = random.choice(x_values)
            y = random.choice(y_values)

            # Update intruders appearing coordinates list to not place another one overlapping
            for ii in xrange(INTRUDER_PICTURE_WIDTH + 2):  # Add a margin
                intruders_coordinates_x.append(x + (ii+1))
                intruders_coordinates_x.append(x - (ii+1))

            for ii in xrange(INTRUDER_PICTURE_HEIGHT + 2):  # Add a margin
                intruders_coordinates_y.append(y + (ii+1))
                intruders_coordinates_y.append(y - (ii+1))

            # Create an intruder with made coordinates
            if type_of_intruder == "Intruder":
                intruder = Intruder(x, y, "pictures/intruder.png", speed=1)
            elif type_of_intruder == "IntruderCrazy":
                intruder = IntruderCrazy(x, y, "pictures/intruder.png", speed=1)
            elif type_of_intruder == "IntruderShooting":
                intruder = IntruderShooting(x, y, "pictures/intruder.png", speed=1)
            intruders_sprites_list.add(intruder)
            all_sprites_list.add(intruder)

        INTRUSIONS_COUNT += 1

    elif INTRUSIONS_COUNT < random.randint(100, 200):
        INTRUSIONS_COUNT += 1
    else:
        INTRUSIONS_COUNT = 0


def make_boss_appear():
    """
    Initiate the boss
    """
    intruder = Boss(SCREEN_WIDTH / 2, -60, "pictures/boss_v1_v2.png", speed=4)
    intruders_sprites_list.add(intruder)
    all_sprites_list.add(intruder)


def reset_lists():
    """
    Reset all sprites lists
    """
    # Remove objects from sprites list except player
    for a_sprite in all_sprites_list:
        if a_sprite.__class__.__name__ != 'Spaceship':
            all_sprites_list.remove(a_sprite)
    [intruders_sprites_list.remove(intruder) for intruder in intruders_sprites_list]
    [player_ammo_sprites_list.remove(ammo) for ammo in player_ammo_sprites_list]
    [player_ammo_sprites_list.remove(ammo) for ammo in intruders_ammo_sprites_list]


class StartupScreen(object):
    """
    Scene: The startup screen
    """
    def __init__(self):
        super(StartupScreen, self).__init__()

        # Create buttons for start screen
        self.buttons_list = [
            Button(window.screen, 100, 600, 100, 30, (WHITE, LIGHT_GREY), "Start", action=self.change_scene),
            Button(window.screen, 100, 640, 100, 30, (WHITE, LIGHT_GREY), "Exit", action=quit_game)
        ]

        # Be sure the background image is the good one
        window.modify_background_image("pictures/interface_bg_v1_800x800.png")

    def render(self, the_window):

        # Prepare draw
        the_window.prepare_draw()

        # Draw everything
        for button in self.buttons_list:
            button.draw()

        # Create main title text
        font = pygame.font.SysFont('Agency FB', 100, True, False)
        title_text = font.render("Space Intruders", True, WHITE)
        the_window.screen.blit(title_text, [(SCREEN_WIDTH / 2) - (title_text.get_width() / 2), 50])

        # Create version text under title
        font = pygame.font.SysFont('Agency FB', 20, True, False)
        version_text = font.render("Version %s" % __version__, True, WHITE)
        the_window.screen.blit(version_text,
                               [(SCREEN_WIDTH / 2) + (title_text.get_width() / 2 - version_text.get_width()),
                                50 + title_text.get_height() + 5])

    def update(self):
        pass

    def handle_events(self, events):
        pass

    @staticmethod
    def change_scene():
        """
        Scene manager change scene
        """
        manager.go_to(Level1())  # FIXME: Must go to level 1 only for testing


class LoosingScreen(object):
    """
    Scene: The screen displayed when player loose.
    """
    def __init__(self):
        super(LoosingScreen, self).__init__()

        self.max_score = None

        reset_lists()

        # Make sure the background image is the good one
        window.modify_background_image("pictures/sky_1024x768.jpg")

        # Mouse invisible
        pygame.mouse.set_visible(True)

        # Create the button to go back to startup screen
        self.go_back_button = Button(window.screen, SCREEN_WIDTH / 2 + - 50, 400, 100, 30, (WHITE, LIGHT_GREY),
                                     "Continue", action=self.change_scene)

    def render(self, the_window):

        the_window.prepare_draw()

        # Draw button
        self.go_back_button.draw()

        # Display score
        font = pygame.font.SysFont('Agency FB', 100, True, False)
        loose_text = font.render("YOU LOOSE", True, WHITE)

        font = pygame.font.SysFont('Agency FB', 50, True, False)
        if int(score.score) < 0:  # Score can't be negative
            score.score = "0"
        loose_text_score = font.render("Your score is %s pts." % score.score, True, WHITE)

        the_window.screen.blit(loose_text, [(SCREEN_WIDTH / 2) - (loose_text.get_width() / 2), 50])
        the_window.screen.blit(loose_text_score, [(SCREEN_WIDTH / 2) - (loose_text_score.get_width() / 2), 180])

    def update(self):
        pass

    def handle_events(self, events):
        pass

    @staticmethod
    def change_scene():
        global LOOSE

        # Reset player
        player.reset()

        # Reset score before exiting
        score.score = "0"
        score.lives = str(PLAYER_STARTING_LIVES)
        LOOSE = False

        # Go back to startup screen
        manager.go_to(StartupScreen())


class WinningScreen(object):
    """
    Scene: The screen displayed when player win.
    """
    def __init__(self):
        super(WinningScreen, self).__init__()

        reset_lists()

        # Reset player
        player.reset()

        # Make sure the background image is the good one
        window.modify_background_image("pictures/sky_1024x768.jpg")

        # Mouse invisible
        pygame.mouse.set_visible(True)

        # Create the buttons
        self.exit_button = Button(window.screen,
                                  SCREEN_WIDTH / 4 + - 50, 400, 100, 30,
                                  (WHITE, LIGHT_GREY), "Exit", action=self.change_scene_exit)
        self.next_level = Button(window.screen,
                                 SCREEN_WIDTH / 4 * 3 + - 50, 400, 100, 30,
                                 (WHITE, LIGHT_GREY), "Next level", action=self.change_scene_next_level)

    def render(self, the_window):

        the_window.prepare_draw()

        # Draw button
        self.exit_button.draw()
        self.next_level.draw()

        # Display score
        font = pygame.font.SysFont('Agency FB', 100, True, False)
        loose_text = font.render("YOU WIN", True, WHITE)

        font = pygame.font.SysFont('Agency FB', 50, True, False)
        if int(score.score) < 0:  # Score can't be negative
            score.score = "0"
        loose_text_score = font.render("Score :%s pts." % score.score, True, WHITE)

        the_window.screen.blit(loose_text, [(SCREEN_WIDTH / 2) - (loose_text.get_width() / 2), 50])
        the_window.screen.blit(loose_text_score, [(SCREEN_WIDTH / 2) - (loose_text_score.get_width() / 2), 180])

    def update(self):
        pass

    def handle_events(self, events):
        pass

    @staticmethod
    def change_scene_exit():

        # Reset score before exiting
        score.score = "0"
        score.lives = str(PLAYER_STARTING_LIVES)

        # Go back to startup screen
        manager.go_to(StartupScreen())

    @staticmethod
    def change_scene_next_level():
        global LEVEL
        LEVEL = LEVEL

        # Reset score before exiting  # FIXME: Must have function to reset score.
        score.score = "0"

        # Find next level
        if LEVEL == 1:
            manager.go_to(Level2())
        elif LEVEL == 2:
            manager.go_to(Level3())
        elif LEVEL == 3:
            manager.go_to(Level4())


class WinningScreenFinal(object):
    """
    Scene: The screen displayed when player win.
    """
    def __init__(self):
        super(WinningScreenFinal, self).__init__()

        reset_lists()

        # Reset player
        player.reset()

        # Make sure the background image is the good one
        window.modify_background_image("pictures/sky_1024x768.jpg")

        # Mouse invisible
        pygame.mouse.set_visible(True)

        # Create the buttons
        self.exit_button = Button(window.screen,
                                  SCREEN_WIDTH / 2 + - 50, 400, 100, 30,
                                  (WHITE, LIGHT_GREY), "Exit", action=self.change_scene_exit)

    def render(self, the_window):

        the_window.prepare_draw()

        # Draw button
        self.exit_button.draw()

        # Display score
        font = pygame.font.SysFont('Agency FB', 100, True, False)
        loose_text = font.render("Congratulations", True, WHITE)

        the_window.screen.blit(loose_text, [(SCREEN_WIDTH / 2) - (loose_text.get_width() / 2), 50])

    def update(self):
        pass

    def handle_events(self, events):
        pass

    @staticmethod
    def change_scene_exit():

        # Reset score before exiting
        score.score = "0"
        score.lives = str(PLAYER_STARTING_LIVES)

        # Go back to startup screen
        manager.go_to(StartupScreen())


class Level4(object):
    """
    Scene: Second level.
    """
    def __init__(self):
        global INTRUSIONS_COUNT
        global RATE_OF_INTRUSIONS
        global LEVEL

        super(Level4, self).__init__()

        LEVEL = 4  # Update global var recording level
        RATE_OF_INTRUSIONS = RATE_OF_INTRUSIONS


        # Mouse invisible
        pygame.mouse.set_visible(False)

        # Make sure the background image is the good one
        window.modify_background_image("pictures/bg4_v2.png")

        # Create level name ready for render
        self.level_name = "LEVEL 4"
        self.font = pygame.font.SysFont('Agency FB', 25, True, False)
        self.level_text = self.font.render(self.level_name, True, WHITE)
        self.level_text_width = self.level_text.get_width()

        self.max_score = 50  # Score to win this scene, Not used here (must kill boss)

        # Make the boss appear only once.
        make_boss_appear()

    def render(self, the_window):
        the_window.prepare_draw()
        the_window.screen.blit(self.level_text, [SCREEN_WIDTH - (self.level_text_width + 10), 10])
        all_sprites_list.draw(window.screen)
        score.draw()

    @staticmethod
    def update():
        # --- Game logic
        move_sprites()

        # FIXME: The manage events and player events order is VERY important. Put in functions?
        manage_events()  # If sprites collides
        [intruder.manage_explosion() for intruder in intruders_sprites_list]  # Manage possible intruders explosion
        player.manage_sparkling()
        player.manage_explosion()

    @staticmethod
    def handle_events(events):
        manage_inputs(events)

    @staticmethod
    def change_scene():
        manager.go_to(LoosingScreen())


class Level3(object):
    """
    Scene: Second level.
    """
    def __init__(self):
        global INTRUSIONS_COUNT
        global RATE_OF_INTRUSIONS
        global LEVEL

        super(Level3, self).__init__()

        LEVEL = 3  # Update global var recording level

        # Mouse invisible
        pygame.mouse.set_visible(False)

        # Make sure the background image is the good one
        window.modify_background_image("pictures/bg4_v2.png")

        # Create level name ready for render
        self.level_name = "LEVEL 3"
        self.font = pygame.font.SysFont('Agency FB', 25, True, False)
        self.level_text = self.font.render(self.level_name, True, WHITE)
        self.level_text_width = self.level_text.get_width()

        self.max_score = 50  # Score to win this scene

        # Reset intrusions count and set rate of intrusions
        INTRUSIONS_COUNT = 0
        RATE_OF_INTRUSIONS = 3

    def render(self, the_window):
        the_window.prepare_draw()
        the_window.screen.blit(self.level_text, [SCREEN_WIDTH - (self.level_text_width + 10), 10])
        all_sprites_list.draw(window.screen)
        score.draw()

    @staticmethod
    def update():
        # --- Game logic
        make_intruders_appear("IntruderShooting")
        move_sprites()

        # FIXME: The manage events and player events order is VERY important. Put in functions?
        manage_events()  # If sprites collides
        [intruder.manage_explosion() for intruder in intruders_sprites_list]  # Manage possible intruders explosion
        player.manage_sparkling()
        player.manage_explosion()

    @staticmethod
    def handle_events(events):
        manage_inputs(events)

    @staticmethod
    def change_scene():
        manager.go_to(LoosingScreen())


class Level2(object):
    """
    Scene: Second level.
    """
    def __init__(self):
        global INTRUSIONS_COUNT
        global RATE_OF_INTRUSIONS
        global LEVEL

        super(Level2, self).__init__()

        LEVEL = 2  # Update global var recording level

        # Mouse invisible
        pygame.mouse.set_visible(False)

        # Make sure the background image is the good one
        window.modify_background_image("pictures/space_bg3_v2.png")

        # Create level name ready for render
        self.level_name = "LEVEL 2"
        self.font = pygame.font.SysFont("Agency FB", 25, True, False)
        self.level_text = self.font.render(self.level_name, True, WHITE)
        self.level_text_width = self.level_text.get_width()

        self.max_score = 25  # Score to win this scene

        # Reset intrusions count and set rate of intrusions
        INTRUSIONS_COUNT = 0
        RATE_OF_INTRUSIONS = 3

    def render(self, the_window):
        the_window.prepare_draw()
        the_window.screen.blit(self.level_text, [SCREEN_WIDTH - (self.level_text_width + 10), 10])
        all_sprites_list.draw(window.screen)
        score.draw()

    @staticmethod
    def update():
        # --- Game logic
        make_intruders_appear("IntruderCrazy")
        move_sprites()

        # FIXME: The manage events and player events order is VERY important. Put in functions?
        manage_events()  # If sprites collides
        [intruder.manage_explosion() for intruder in intruders_sprites_list]  # Manage possible intruders explosion
        player.manage_sparkling()
        player.manage_explosion()

    @staticmethod
    def handle_events(events):
        manage_inputs(events)

    @staticmethod
    def change_scene():
        manager.go_to(LoosingScreen())


class Level1(object):
    """
    Scene: First level.
    """
    def __init__(self):
        global INTRUSIONS_COUNT
        global RATE_OF_INTRUSIONS
        global LEVEL

        super(Level1, self).__init__()

        # Update global var recording level
        LEVEL = 1

        # Make sure the background image is the good one
        window.modify_background_image("pictures/sky_1024x768.jpg")

        # Mouse invisible
        pygame.mouse.set_visible(False)

        # Create level name ready for render
        self.level_name = "LEVEL 1"
        self.font = pygame.font.SysFont("Agency FB", 25, True, False)
        self.level_text = self.font.render(self.level_name, True, WHITE)
        self.level_text_width = self.level_text.get_width()

        self.max_score = 25  # Score to win this scene

        # Reset intrusions count and set rate of intrusions
        INTRUSIONS_COUNT = 0
        RATE_OF_INTRUSIONS = 3

    def render(self, the_window):
        the_window.prepare_draw()
        the_window.screen.blit(self.level_text, [SCREEN_WIDTH - (self.level_text_width + 10), 10])
        all_sprites_list.draw(window.screen)
        score.draw()

    @staticmethod
    def update():
        # --- Game logic
        make_intruders_appear("Intruder")
        move_sprites()

        # FIXME: The manage events and player events order is VERY important. Put in functions?
        manage_events()  # If sprites collides
        [intruder.manage_explosion() for intruder in intruders_sprites_list]  # Manage possible intruders explosion
        player.manage_sparkling()
        player.manage_explosion()

    @staticmethod
    def handle_events(events):
        manage_inputs(events)

    @staticmethod
    def change_scene():
        manager.go_to(LoosingScreen())


class SceneManager(object):
    """
    Use this class to create a scene object and run it in main script
    """
    def __init__(self):
        self.scene = None  # Initialize variables in the init class to be clean
        self.go_to(StartupScreen())  # Select the first scene of the game at init

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


if __name__ == "__main__":

    # Initialize pygame, sounds and display
    window = Display(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Intruders", bg_picture="pictures/interface_bg_v1_800x800.png")

    # Creates player
    player = Spaceship(PLAYER_START_POS_X, PLAYER_START_POS_Y, "pictures/alienblaster.png",
                       sparkle_image="pictures/alienblaster_sparkle.png")
    all_sprites_list.add(player)

    # Create score board
    score = ScoreBoard("0", str(PLAYER_STARTING_LIVES), window)

    # Initialize a running variable
    running = True

    # Create the scene manager
    manager = SceneManager()

    # While game running
    while running:
        # timer.tick(60)

        # Always manage quit event
        if pygame.event.get(pygame.QUIT):
            running = False

        # Run actual scene
        manager.scene.handle_events(pygame.event.get())  # Manage events of the scene
        manager.scene.update()  # Do scene's screen updates
        manager.scene.render(window)  # Render scene objects

        # Update display
        window.update()

# Cleanly exit game
quit_game()