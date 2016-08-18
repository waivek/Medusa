from src.Line import *
from src.LoadResources import *

class BlinkComponent:
    def __init__(self, player):
        from src.Sprite import Sprite
        self.valid_blink_points = []
        self.dot_spr =Sprite(ImageEnum.BLINK_DOT)
        self.dot_spr.bounds = (0, 0, 4, 4)
        self.can_blink = False
        self.player = player

    def get_actual_mouse_pos(self):
        from src.WorldConstants import CONST_CAMERA_PLAYER_OFFSET_X, CONST_CAMERA_PLAYER_OFFSET_Y
        import pygame
        x, y = pygame.mouse.get_pos()
        player_x, player_y = self.player.sprite.sprite_rect().topleft
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

    def draw(self, screen, camera):
        if self.can_blink:
            self.fill_valid_blink_points()
            for x, y in self.valid_blink_points:
                self.dot_spr.set_location((x, y))
                self.dot_spr.draw(screen, camera)

    def blink(self):
        player_x, player_y = self.player.sprite.sprite_rect().center
        valid_x, valid_y = self.valid_blink_points[-1]

        damper_x = 8
        damper_y= 0

        d_x = (valid_x - player_x) - damper_x
        d_y = (valid_y - player_y) - damper_y

        self.player.moving_component.move((d_x, d_y))

    def handle_event(self, event):
        from src.WorldConstants import BLINK_KEY
        if event.type == pygame.KEYDOWN:
            if event.key == BLINK_KEY:
                self.can_blink = True

        elif event.type == pygame.KEYUP:
            if event.key == BLINK_KEY:
                self.can_blink = False

        if event.type == pygame.MOUSEBUTTONDOWN and self.can_blink:
            self.blink()

    def pos_is_tile(self, x, y):
        i = int(x/32)
        j = int(y/32)

        if self.player.level.tiles[j][i]:
            return True
        else:
            return False