
from settings import *
from random import choice
import pygame as pg
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.last_update = 0
        self.image=pg.image.load("images/right.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (400, HEIGHT - 600)
        self.pos = vec(400, HEIGHT - 600)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # Jump when on a platform only
        self.back_sound = pg.mixer.Sound("sounds/Bounce.ogg")
        self.back_sound.set_volume(3.0)
        self.rect.y += 6
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 6
        if hits and self.vel.y >= 0:
            self.vel.y = -(JUMP_INTENSITY + self.game.level)
            self.back_sound.play()

    def update(self):
        self.vel.x=0
        self.acc = vec(0, GRAVITY)

        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -VELOCITY
            self.image = pg.image.load("images/left.png").convert_alpha()
        if keys[pg.K_RIGHT]:
            self.vel.x = VELOCITY
            self.image = pg.image.load("images/right.png").convert_alpha()

        self.vel += self.acc
        self.pos += self.vel

        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [pg.image.load("images/blue.png").convert_alpha(),
                  pg.image.load("images/green.png").convert_alpha()]

        self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
