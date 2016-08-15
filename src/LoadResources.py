import pygame
from enum import Enum

gImages = []
gSounds = []

class ImageEnum(Enum):
    PLAYER1_LEFT = 0
    PLAYER1_RIGHT = 1
    PLAYER1_JUMPLEFT = 2
    PLAYER1_JUMPRIGHT = 3

    BLOCK = 4
    SKY = 5

    SKELETON_STANDING = 6
    SKELETON_WALKING = 7

    HUD_LIFE = 8
    HUD_ENERGY = 9

    POWERUP_GREEN = 10
    POWERUP_RED = 11
    POWERUP_YELLOW = 12
    POWERUP_BLUE = 13
    POWERUP_PURPLE = 14
    POWERUP_LIGHT = 15
    POWERUP_DARK = 16

    KEY_COPPER = 17
    KEY_SILVER = 18
    KEY_GOLD = 19
    KEY_DARK = 20
    KEY_MAGIC = 21

    LOCK_COPPER = 22
    LOCK_SILVER = 23
    LOCK_GOLD = 24
    LOCK_DARK = 25
    LOCK_MAGIC = 26

    WEAPON_BOW = 27
    AMMO_ARROW = 28
    WEAPON_GUN = 29
    AMMO_BULLET = 30

    BLINK_DOT = 31

class SoundEnum(Enum):
    JUMP = 0
    HIT = 1
    POWERUP = 2
    UNLOCK = 3
    ARROW_SHOOT = 4

gImagePaths = [
    r"..\raw\Sprites\explorer_left_strip8.png",
    r"..\raw\Sprites\explorer_right_strip8.png",
    r"..\raw\Sprites\explorer_jumpleft.png",
    r"..\raw\Sprites\explorer_jumpright.png",
    r"..\raw\Sprites\wall_block.png",
    r"..\raw\Sprites\sky.png",
    r"..\raw\Sprites\skeleton.png",
    r"..\raw\Sprites\skeleton_walking_strip10.png",
    r"..\raw\Sprites\item_life.png",
    r"..\raw\Sprites\item_energy.png",
    r"..\raw\Sprites\gem_green_sparkle_strip32.png",
    r"..\raw\Sprites\gem_red_sparkle_strip32.png",
    r"..\raw\Sprites\gem_yellow_sparkle_strip32.png",
    r"..\raw\Sprites\gem_blue_sparkle_strip32.png",
    r"..\raw\Sprites\gem_purple_sparkle_strip32.png",
    r"..\raw\Sprites\gem_light_sparkle_strip32.png",
    r"..\raw\Sprites\gem_dark_sparkle_strip32.png",
    r"..\raw\Sprites\key_copper.png",
    r"..\raw\Sprites\key_silver_sparkle_strip32.png",
    r"..\raw\Sprites\key_gold_sparkle_strip32.png",
    r"..\raw\Sprites\key_black.png",
    r"..\raw\Sprites\key_magic.png",
    r"..\raw\Sprites\lock_copper.png",
    r"..\raw\Sprites\lock_silver_sparkle_strip32.png",
    r"..\raw\Sprites\lock_gold_sparkle_strip32.png",
    r"..\raw\Sprites\lock_black.png",
    r"..\raw\Sprites\lock_magic.png",
    r"..\raw\Sprites\bow.png",
    r"..\raw\Sprites\arrow_left.png",
    r"..\raw\Sprites\gun.png",
    r"..\raw\Sprites\bullet_left.png",
    r"..\raw\Sprites\red_dot.png"

]
gSoundPaths = [
    r"..\raw\Sounds\jump.wav",
    r"..\raw\Sounds\hit.wav",
    r"..\raw\Sounds\curious_up.wav",
    r"..\raw\Sounds\open.wav",
    r"..\raw\Sounds\miss.wav"
]

def load_images():
    for i in range(len(gImagePaths)):
        img = pygame.image.load(gImagePaths[i])
        if img is None:
            print("ERROR: Unable to load image: %s" % (gImagePaths[i]))
            return False
        gImages.append(img)
    return True

def load_sounds():
    for i in range(len(gSoundPaths)):
        sound = pygame.mixer.Sound(gSoundPaths[i])
        if sound is None:
            print("ERROR: Unable to load sound: %s" % (gSoundPaths[i]))
            return False
        gSounds.append(sound)
    return True

def load_resources():
    return load_images() and load_sounds()

def play_sound(soundenum):
    gSounds[soundenum.value].play()
