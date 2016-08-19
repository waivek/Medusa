from src.LoadResources import *
from enum import Enum
class BlinkState(Enum):
    CAN_BLINK = 0
    SHOWING_LINE = 1
    BLINKING = 2
    COOLING_DOWN = 3

class Blink_Component:
    def __init__(self, player):
        from src.Timer import Timer
        from src.Sprite import Sprite
        self.valid_blink_points = []
        self.dot_spr =Sprite(ImageEnum.BLINK_DOT)
        self.dot_spr.bounds = (0, 0, 4, 4)
        self.can_blink = False
        self.player = player

        self.blink_frames = 3
        self.is_blinking = False
        self.frame_displacement = (None, None)
        self.frames_passed = None
        self.timer = Timer()
        self.cooldown_ms = 2500
        self.cooldown_passed = False

        self.state = BlinkState.CAN_BLINK

    def get_actual_mouse_pos(self):
        from src.WorldConstants import CONST_CAMERA_PLAYER_OFFSET_X, CONST_CAMERA_PLAYER_OFFSET_Y
        import pygame
        x, y = pygame.mouse.get_pos()
        player_x, player_y = self.player.sprite.sprite_rect().topleft
        # x_origin = 0
        # y_origin = 0
        x_origin = player_x - CONST_CAMERA_PLAYER_OFFSET_X
        y_origin = player_y - CONST_CAMERA_PLAYER_OFFSET_Y

        mouse_x = x+x_origin
        mouse_y = y+y_origin

        return mouse_x, mouse_y

    def fill_valid_blink_points(self):
        player_x, player_y = self.player.sprite.sprite_rect().center
        mouse_x, mouse_y = self.get_actual_mouse_pos()
        if mouse_x == player_x:
            mouse_x = mouse_x + 1
        m = (player_y - mouse_y) / (player_x - mouse_x)
        c = player_y - (m * player_x)

        self.valid_blink_points = []

        step = 0

        if player_x <= mouse_x:
            step = 1
        elif mouse_x < player_x:
            step = -1

        for x in range(player_x, mouse_x, step):
            y = m*x + c
            if self.pos_is_tile(x, y):
                break
            self.valid_blink_points.append((x, y))

    def pos_is_tile(self, x, y):
        i = int(x/32)
        j = int(y/32)

        if self.player.level.tiles[j][i]:
            return True
        else:
            return False

    def draw(self, screen, camera):
        if self.state == BlinkState.SHOWING_LINE:
            self.fill_valid_blink_points()
            for x, y in self.valid_blink_points:
                self.dot_spr.set_location((x, y))
                self.dot_spr.draw(screen, camera)

    def handle_event(self, event):
        pass

    def update(self, deltaTime):

        keys = pygame.key.get_pressed()
        mice = pygame.mouse.get_pressed()
        left_pressed = bool(mice[0])
        from src.WorldConstants import BLINK_KEY

        if False:
            pass

        elif self.state == BlinkState.CAN_BLINK :
            if keys[BLINK_KEY]:
                self.state = BlinkState.SHOWING_LINE

        elif self.state == BlinkState.SHOWING_LINE :
            if not keys[BLINK_KEY]:
                self.state = BlinkState.CAN_BLINK
            elif left_pressed:
                self.state = BlinkState.BLINKING
                play_sound(SoundEnum.BLINK)

        elif self.state == BlinkState.BLINKING :
            is_first_blink_frame = self.frames_passed == None
            if is_first_blink_frame:

                self.frames_passed = 0

                player_x, player_y = self.player.sprite.sprite_rect().center
                valid_x, valid_y = self.valid_blink_points[-1]
                d_x = (valid_x - player_x)
                d_y = (valid_y - player_y)

                self.frame_displacement = (d_x / self.blink_frames,
                                           d_y / self.blink_frames)
                self.player.moving_component.move(self.frame_displacement)

                self.frames_passed = self.frames_passed + 1
            elif not is_first_blink_frame:
                if self.frames_passed < self.blink_frames:
                    self.player.moving_component.move(self.frame_displacement)
                    self.frames_passed = self.frames_passed + 1
                elif self.frames_passed >= self.blink_frames:
                    self.frames_passed = None
                    self.frame_displacement = (None, None)
                    self.timer.reset()
                    self.state = BlinkState.COOLING_DOWN
        elif self.state == BlinkState.COOLING_DOWN :
            cooldown_passed = self.timer.get_time() > self.cooldown_ms
            if cooldown_passed:
                self.state = BlinkState.CAN_BLINK

