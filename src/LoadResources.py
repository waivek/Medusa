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

class SoundEnum(Enum):
    JUMP = 0
    HIT = 1

gImagePaths = [
    r"..\raw\Sprites\explorer_left_strip8.png",  #0
    r"..\raw\Sprites\explorer_right_strip8.png", #1
    r"..\raw\Sprites\explorer_jumpleft.png",     #2
    r"..\raw\Sprites\explorer_jumpright.png",    #3
    r"..\raw\Sprites\wall_block.png",            #4
    r"..\raw\Sprites\sky.png",                   #5
    r"..\raw\Sprites\skeleton.png", #6
    r"..\raw\Sprites\skeleton_walking_strip10.png" # 7
]
gSoundPaths = [r"..\raw\Sounds\jump.wav",r"..\raw\Sounds\hit.wav"]

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