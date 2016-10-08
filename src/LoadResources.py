import pygame
from enum import Enum

gImages = []
gSounds = []
gFonts = []

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

    KEY_WOOD = 17
    KEY_BLUE = 18
    KEY_COPPER = 19
    KEY_SILVER = 20
    KEY_GOLD = 21
    KEY_DARK = 22
    KEY_MAGIC = 23

    LOCK_WOOD = 24
    LOCK_BLUE = 25
    LOCK_COPPER = 26
    LOCK_SILVER = 27
    LOCK_GOLD = 28
    LOCK_DARK = 29
    LOCK_MAGIC = 30

    WEAPON_BOW = 31
    AMMO_ARROW = 32
    WEAPON_GUN = 33
    AMMO_BULLET = 34

    BLINK_DOT = 35

    WEAPON_SHORTSWORD = 36

    PLAYER1_STABLEFT = 37
    PLAYER1_STABRIGHT = 38
    PLAYER1_STRIKELEFT = 39
    PLAYER1_STRIKERIGHT = 40

    CAN_BLINK = 41
    NO_BLINK = 42

    SKELETON_WALKLEFT = 43
    SKELETON_WALKRIGHT = 44
    SKELETON_STABLEFT = 45
    SKELETON_STABRIGHT = 46

class SoundEnum(Enum):
    JUMP = 0
    HIT = 1
    POWERUP = 2
    UNLOCK = 3
    ARROW_SHOOT = 4
    ARROW_HIT_ENEMY = 5
    ARROW_HIT_STONE = 6
    METAL_MEDIUM_SLICE_METAL = 7
    METAL_MEDIUM_SLICE_STONE = 8
    BLINK = 9

gImagePaths = [
    r"..\raw\Sprites\player\guy_left.png",
    r"..\raw\Sprites\player\guy_right.png",
    r"..\raw\Sprites\explorer_jumpleft.png",
    r"..\raw\Sprites\explorer_jumpright.png",
    r"..\raw\Sprites\wall_block.png",
    r"..\raw\Sprites\wall_background.png",
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
    r"..\raw\Sprites\key_wood.png",
    r"..\raw\Sprites\key_blue.png",
    r"..\raw\Sprites\key_copper.png",
    r"..\raw\Sprites\key_silver_sparkle_strip32.png",
    r"..\raw\Sprites\key_gold_sparkle_strip32.png",
    r"..\raw\Sprites\key_black.png",
    r"..\raw\Sprites\key_magic.png",
    r"..\raw\Sprites\lock_wood.png",
    r"..\raw\Sprites\lock_blue.png",
    r"..\raw\Sprites\lock_copper.png",
    r"..\raw\Sprites\lock_silver_sparkle_strip32.png",
    r"..\raw\Sprites\lock_gold_sparkle_strip32.png",
    r"..\raw\Sprites\lock_black.png",
    r"..\raw\Sprites\lock_magic.png",
    r"..\raw\Sprites\weapons\bow.png",
    r"..\raw\Sprites\arrow_left.png",
    r"..\raw\Sprites\gun.png",
    r"..\raw\Sprites\bullet_left.png",
    r"..\raw\Sprites\red_dot.png",
    r"..\raw\Sprites\weapons\short_sword.png",
    r"..\raw\Sprites\player\stab_left.png",
    r"..\raw\Sprites\player\stab_right.png",
    r"..\raw\Sprites\player\strike_left.png",
    r"..\raw\Sprites\player\strike_right.png",
    r"..\raw\Sprites\custom_sprites\can_blink.png",
    r"..\raw\Sprites\custom_sprites\no_blink.png",
    r"..\raw\Sprites\skeleton\walk_left.png",
    r"..\raw\Sprites\skeleton\walk_right.png",
    r"..\raw\Sprites\skeleton\stab_left.png",
    r"..\raw\Sprites\skeleton\stab_right.png",
]
gSoundPaths = [
    r"..\raw\Sounds\jump.wav",
    r"..\raw\Sounds\hit.wav",
    r"..\raw\Sounds\curious_up.wav",
    r"..\raw\Sounds\open.wav",
    r"..\raw\Sounds\miss.wav",
    r"..\raw\Sounds\DryadMissile1.wav",
    r"..\raw\Sounds\DryadMissile2.wav",
    r"..\raw\Sounds\MetalMediumSliceMetal2.wav",
    r"..\raw\Sounds\MetalMediumSliceStone3.wav",
    r"..\raw\Sounds\BlinkBirth1.wav"
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

def load_fonts():
    #global gFont
    #nonlocal gFont
    font = pygame.font.Font(r"..\raw\fonts\OxygenMono.ttf", 18)
    if font is None:
        print("ERROR: unable to load font")
        return False
    gFonts.append(font)
    return True

def load_resources():
    return load_images() and load_sounds() and load_fonts()

def play_sound(soundenum):
    gSounds[soundenum.value].play()
