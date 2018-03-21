#!/usr/bin/env python
"""
Define different spaceships
"""

import random
from game_vars import *
from spritesheet_functions import create_frames


class Ammunition(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed=4, rate_of_fire=200):
        super(Ammunition, self).__init__()  # Call the parent class (Sprite) constructor

        self.image = pygame.image.load(image)  # .convert()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.rect = self.image.get_rect()  # Get the image size to create rectangle
        self.rect.x = x  # Position at init
        self.rect.y = y  # Position at init

        self.speed = speed
        self.rate_of_fire = rate_of_fire  # Used with fire_timer of a spaceship

        self.launch_sound = pygame.mixer.Sound("sounds/Bottle_Rocket_v2.wav")
        self.launch_sound.set_volume(0.1)

    def move(self):
        """
        If sprite exploding manage it, else move
        """
        self.rect.y -= self.speed

        # Ammunition must die if out of screen:
        if (self.rect.y + self.height) < 0 or (self.rect.y > SCREEN_HEIGHT):
            self.kill()

    def explode(self):
        self.kill()


class IntruderAmmunition(Ammunition):
    def __init__(self, image, x, y, speed=6, rate_of_fire=200):
        super(IntruderAmmunition, self).__init__(image, x, y, speed=4, rate_of_fire=200)

        self.image = pygame.transform.flip(self.image, False, True)  # Flip image to be in the good sens

        # Explosion vars
        self.exploded = False
        self.explosion_count = 0
        self.explosion_time = 5
        self.explosion_time_count = self.explosion_time
        self.exploding_frames = create_frames("pictures/explosion_300x200.png", 3, 4)  # Add images for exploding frames
        self.explosion_sound = pygame.mixer.Sound("sounds/Pen_Clicks_v2.wav")
        self.explosion_sound.set_volume(0.2)
        self.died = False

    def explode(self):
        self.exploded = True

    def manage_explosion(self):
        if self.explosion_count < len(self.exploding_frames) - 1:
            self.image = pygame.transform.scale(  # Load explosion image resizing it to be centered
                self.exploding_frames[self.explosion_count], (self.width, self.height))

            # Deals with timers
            if self.explosion_time_count == 0:
                self.explosion_count += 1
                self.explosion_time_count = self.explosion_time
            else:
                self.explosion_time_count -= 1
        else:
            self.died = True
            self.kill()

    def move(self):
        """
        If sprite exploding manage it, else move
        """
        if self.exploded is False:
            self.rect.y += self.speed
        else:
            self.manage_explosion()

        # Ammunition must die if out of screen:
        if (self.rect.y + self.height) < 0 or (self.rect.y > SCREEN_HEIGHT):
            self.kill()


class Spaceship(pygame.sprite.Sprite):
    """
    Default space ship specifications.
    """
    def __init__(self, x, y, image, speed=4, sparkle_image=""):
        super(Spaceship, self).__init__()

        self.image = pygame.image.load(image)  # .convert()
        self.image_orig = image  # To revert if image change
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.rect = self.image.get_rect()  # Get the image size to create rectangle
        self.rect.x = x  # Position at init
        self.rect.y = y  # Position at init

        self.can_move = True
        self.speed = speed
        self.fire_timer = 0  # Used with rate_of_fire of ammunition

        # Explosion vars
        self.exploded = False
        self.explosion_count = 0
        self.explosion_time = 5
        self.explosion_time_count = self.explosion_time
        self.exploding_frames = create_frames("pictures/explosion_300x200.png", 3, 4)  # Add images for exploding frames
        self.explosion_sound = pygame.mixer.Sound("sounds/Grenade_Explosion_v2.wav")
        self.explosion_sound.set_volume(0.2)

        # Sparkling vars
        self.sparkle_image = sparkle_image
        self.sparkle = False
        self.sparkle_timer = 0
        self.sparkle_time = 3000
        self.sparkle_rate = 5
        self.sparkle_rate_count = 0
        self.sparkle_image_active = False
        self.hit_sound = pygame.mixer.Sound("sounds/Hockey_Puck_Slap.wav")
        self.hit_sound.set_volume(0.2)

        self.died = False

    def adjust_position(self):
        """
        If out of screen adjust on the border
        :return: Nothing
        """
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < SCREEN_HEIGHT / 2:
            self.rect.y = SCREEN_HEIGHT / 2
        if self.rect.x > SCREEN_WIDTH - self.width:
            self.rect.x = SCREEN_WIDTH - self.width
        if self.rect.y > SCREEN_HEIGHT - self.height:
            self.rect.y = SCREEN_HEIGHT - self.height

    def move(self, direction):
        """
        Move according to speed and a given direction
        :param direction: text
        :return: Nothing
        """
        if self.can_move is True:
            if direction == "forward":
                self.rect.y -= self.speed
            if direction == "backward":
                self.rect.y += self.speed
            if direction == "left":
                self.rect.x -= self.speed
            if direction == "right":
                self.rect.x += self.speed

            self.adjust_position()

    def shoot(self):
        """
        Create an ammo.
        If fire_timer and ammo's rate_of_fire are ok shoot it
        :return: An ammo in sprites lists if fired.
        """
        if self.exploded is False:
            ammo = Ammunition("pictures/missile_1_10x29.png",
                              self.rect.x + self.width / 2,
                              self.rect.y - 20,
                              speed=4,
                              rate_of_fire=400)

            if self.fire_timer == 0 or pygame.time.get_ticks() > self.fire_timer + ammo.rate_of_fire:
                ammo.launch_sound.play()
                player_ammo_sprites_list.add(ammo)
                all_sprites_list.add(ammo)
                self.fire_timer = pygame.time.get_ticks()

    def explode(self):
        if self.exploded is False:
            self.explosion_sound.play()
            self.exploded = True
            self.can_move = False

    def manage_explosion(self):
        if self.exploded is True:
            if self.explosion_count < len(self.exploding_frames) - 1:
                self.image = pygame.transform.scale(  # Load explosion image resizing it to be centered
                    self.exploding_frames[self.explosion_count], (self.width, self.height))

                # Deals with timers
                if self.explosion_time_count == 0:
                    self.explosion_count += 1
                    self.explosion_time_count = self.explosion_time
                else:
                    self.explosion_time_count -= 1
            else:
                self.died = True  # Mainly used for player
                self.kill()  # For the image to not reappear after explosion

    def lost_life(self):
        """
        Player sparkle n seconds and must not be hit by another enemy.
        The timer is managed by self.manage_sparkling()
        """
        # FIXME: The fact that the player can't be hit is managed in an outside function. Should be inside class.
        if self.sparkle is False:  # If player is not invulnerable and has lives ...
            self.hit_sound.play()
            self.sparkle = True  # ... We make it invulnerable
            self.image = pygame.image.load(self.sparkle_image)  # Change the image IMPORTANT: Must be same size
            self.sparkle_image_active = True
            self.sparkle_timer = pygame.time.get_ticks() + self.sparkle_time  # Create invulnerability timer

    def manage_sparkling(self):
        # If player invulnerable ...
        if pygame.time.get_ticks() > self.sparkle_timer:  # ... and timer ended
            self.image = pygame.image.load(self.image_orig)
            self.sparkle = False  # Make player vulnerable again
            self.sparkle_timer = 0  # Reset invulnerability timer.
            self.sparkle_rate_count = 0  # Use to cycle between images to simulate sparkle
        else:
            # If image must change to simulate sparkle
            if self.sparkle_rate_count >= self.sparkle_rate:
                self.sparkle_rate_count = 0
                if self.sparkle_image_active is True:
                    self.image = pygame.image.load(self.image_orig)
                    self.sparkle_image_active = False
                else:
                    self.image = pygame.image.load(self.sparkle_image)
                    self.sparkle_image_active = True
            else:
                self.sparkle_rate_count += 1

    def reset(self):
        all_sprites_list.add(self)
        self.can_move = True
        self.exploded = False
        self.explosion_count = 0
        self.died = False
        self.image = pygame.image.load(self.image_orig)
        self.rect.x = PLAYER_START_POS_X
        self.rect.y = PLAYER_START_POS_Y


class Intruder(Spaceship):
    """
    Simple intruders derived from Spaceship class
    """
    def __init__(self, x, y, image, speed=1):
        Spaceship.__init__(self, x, y, image, speed=speed)

        self.explosion_sound = pygame.mixer.Sound("sounds/Pen_Clicks_v2.wav")  # Overwrite Spaceship's exploding sound
        self.has_hit_player = False

    def move(self, direction="None"):
        """
        Override Spaceship method, only move in one direction.
        """
        if self.can_move is True:
            self.rect.y += self.speed

    def manage_explosion(self):
        """
        Overwrite Spaceship explosion. Do kill object for it to disappear.
        """
        if self.exploded is True:
            if self.explosion_count < len(self.exploding_frames) - 1:
                self.image = pygame.transform.scale(  # Load explosion image resizing it to be centered
                    self.exploding_frames[self.explosion_count], (self.width, self.height))

                # Deals with timers
                if self.explosion_time_count == 0:
                    self.explosion_count += 1
                    self.explosion_time_count = self.explosion_time
                else:
                    self.explosion_time_count -= 1
            else:
                self.kill()
                self.died = True  # Mainly used for player
                # FIXME: Sprite continues to exist (print self.explosion_count)
                # FIXME: Explosion image doesn't seem to be centered


class IntruderCrazy(Intruder):
    """
    These intruders can change speed.
    """
    def __init__(self, x, y, image, speed=1):
        Intruder.__init__(self, x, y, image, speed=speed)

    def make_crazy(self):
        # Random speed change
        random_chance1, random_chance2 = random.randint(0, 100), random.randint(0, 100)
        if random_chance1 in (10, 20, 30, 40, 50, 60, 70) and random_chance2 in (10, 20, 30, 40, 50, 60, 70):
            if self.speed == 5:
                self.speed = 1
            else:
                self.speed = 5

    def move(self, direction="None"):
        """
        Override Spaceship method, only move in one direction.
        """
        if self.can_move is True:

            self.make_crazy()

            # Make it move
            self.rect.y += self.speed

    def manage_explosion(self):
        """
        Overwrite Spaceship explosion. Do kill object for it to disappear.
        """
        if self.exploded is True:
            if self.explosion_count < len(self.exploding_frames) - 1:
                self.image = pygame.transform.scale(  # Load explosion image resizing it to be centered
                    self.exploding_frames[self.explosion_count], (self.width, self.height))

                # Deals with timers
                if self.explosion_time_count == 0:
                    self.explosion_count += 1
                    self.explosion_time_count = self.explosion_time
                else:
                    self.explosion_time_count -= 1
            else:
                self.kill()
                self.died = True  # Mainly used for player
                # FIXME: Sprite continues to exist (print self.explosion_count)
                # FIXME: Explosion image doesn't seem to be centered


class IntruderShooting(Spaceship):
    """
    This intruder can shoot
    """
    def __init__(self, x, y, image, speed=1):
        Spaceship.__init__(self, x, y, image, speed=speed)

        self.explosion_sound = pygame.mixer.Sound("sounds/Pen_Clicks_v2.wav")  # Overwrite Spaceship's exploding sound
        self.has_hit_player = False

    def shoot(self):
        """
        Create an ammo.
        If fire_timer and ammo's rate_of_fire are ok shoot it
        :return: An ammo in sprites lists if fired.
        """
        if self.exploded is False:
            ammo = IntruderAmmunition("pictures/missile_2_v4.png", self.rect.x + self.width / 2,
                                      self.rect.y + 20, speed=2, rate_of_fire=200)

            if self.fire_timer == 0 or pygame.time.get_ticks() > self.fire_timer + ammo.rate_of_fire:
                ammo.launch_sound.play()
                intruders_ammo_sprites_list.add(ammo)
                all_sprites_list.add(ammo)
                self.fire_timer = pygame.time.get_ticks()

    def move(self, direction="None"):
        """
        Override Spaceship method, only move in one direction.
        """
        if self.can_move is True:
            self.rect.y += self.speed

            # Intruder randomly shoot
            if random.randint(0, 1000) < 4:
                self.shoot()

    def manage_explosion(self):
        """
        Overwrite Spaceship explosion. Do kill object for it to disappear.
        """
        if self.exploded is True:
            if self.explosion_count < len(self.exploding_frames) - 1:
                self.image = pygame.transform.scale(  # Load explosion image resizing it to be centered
                    self.exploding_frames[self.explosion_count], (self.width, self.height))

                # Deals with timers
                if self.explosion_time_count == 0:
                    self.explosion_count += 1
                    self.explosion_time_count = self.explosion_time
                else:
                    self.explosion_time_count -= 1
            else:
                self.kill()
                self.died = True  # Mainly used for player


class Boss(IntruderShooting):
    """
    Big Boss
    """
    def __init__(self, x, y, image, speed=1):
        IntruderShooting.__init__(self, x, y, image, speed=speed)

        self.appear = False

        self.direction_x = 1
        self.direction_y = 1
        self.direction_count = 0
        self.direction_count_max = 30

    def move(self, direction="None"):
        """
        Override Spaceship method, only move in one direction.
        """
        if self.can_move is True:

            # If boss appearing
            if self.appear is False:
                self.rect.y += self.speed
                if self.rect.y > 20:
                    self.appear = True
            else:

                # If can change direction randomize it
                if self.direction_count > self.direction_count_max:
                    self.direction_x = random.randint(-1, 1)
                    self.direction_y = random.randint(-1, 1)
                    self.direction_count = 0
                else:
                    self.direction_count += 1

                # If randomize direction is out of bounds inverse it
                if self.rect.x <= 0 and self.direction_x == -1:
                    self.direction_x = random.randint(0, 1)
                elif self.rect.x + self.width >= SCREEN_WIDTH and self.direction_x == 1:
                    self.direction_x = random.randint(-1, 0)

                if self.rect.y <= 0 and self.direction_y == -1:
                    self.direction_y = random.randint(0, 1)
                elif self.rect.y + self.height >= (2*(SCREEN_HEIGHT/3)) and self.direction_y == 1:
                    self.direction_y = random.randint(-1, 0)

                # Move according to chosen direction
                if self.direction_x == -1:
                    self.rect.x -= self.speed
                elif self.direction_x == 1:
                    self.rect.x += self.speed

                if self.direction_y == -1:
                    self.rect.y -= self.speed
                elif self.direction_y == 1:
                    self.rect.y += self.speed

        # Intruder randomly shoot
        if random.randint(0, 1000) < 20:
            self.shoot()

    def shoot(self):
        if self.exploded is False:
            ammunition_fired = [
                IntruderAmmunition("pictures/missile_2_v4.png", self.rect.x + self.width / 2,
                                      self.rect.y + 20, speed=2, rate_of_fire=100),
                IntruderAmmunition("pictures/missile_2_v4.png", self.rect.x + self.width / 2,
                                      self.rect.y + 40, speed=2, rate_of_fire=100),
                IntruderAmmunition("pictures/missile_2_v4.png", self.rect.x + self.width,
                                      self.rect.y + 20, speed=2, rate_of_fire=100),
                IntruderAmmunition("pictures/missile_2_v4.png", self.rect.x,
                                      self.rect.y + 20, speed=2, rate_of_fire=100)
            ]

            if self.fire_timer == 0 or pygame.time.get_ticks() > self.fire_timer + ammunition_fired[0].rate_of_fire:
                # ammo.launch_sound.play()
                # intruders_ammo_sprites_list.add(ammo)
                # all_sprites_list.add(ammo)
                # self.fire_timer = pygame.time.get_ticks()

                ammunition_fired[0].launch_sound.play()
                for ammo in ammunition_fired:
                    intruders_ammo_sprites_list.add(ammo)
                    all_sprites_list.add(ammo)
                self.fire_timer = pygame.time.get_ticks()

    def manage_explosion(self):
        """
        Overwrite Spaceship explosion. Do kill object for it to disappear.
        """
        if self.exploded is True:
            if self.explosion_count < len(self.exploding_frames) - 1:
                self.image = pygame.transform.scale(  # Load explosion image resizing it to be centered
                    self.exploding_frames[self.explosion_count], (self.width, self.height))

                # Deals with timers
                if self.explosion_time_count == 0:
                    self.explosion_count += 1
                    self.explosion_time_count = self.explosion_time
                else:
                    self.explosion_time_count -= 1
            else:
                self.died = True  # Used to know if player wins