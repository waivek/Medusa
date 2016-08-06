import pygame
from enum import Enum

gImages = []
gSounds = []

class ImageEnum(Enum):
    PLAYER1 = 0
    TILE = 1
    SKY = 2

class SoundEnum(Enum):
    JUMP = 0
    HIT = 1

gImagePaths = [r"..\raw\player1.png",r"..\raw\tile.jpg",r"..\raw\sky.png"]
gSoundPaths = [r"..\raw\jump.wav",r"..\raw\hit.wav"]

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