import consts
import var

import pygame
import random
import time

from player import check_collision


class Item(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("star.png"), (30, 30))  # 기본값: 별 (무적 아이템)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.tempx = 0
        self.tempy = 0
        while ((self.tempx - consts.const["center"][0]) ** 2 + (self.tempy - consts.const["center"][1]) ** 2 >=
               consts.const["radius"] ** 2):
            self.tempx = random.randint(500 - (consts.const["radius"] - self.rect.width),
                                        500 + (consts.const["radius"] - self.rect.width))
            self.tempy = random.randint(400 - (400 + consts.const["radius"] - self.rect.height),
                                        (400 + consts.const["radius"] - self.rect.height))
        self.rect.center = self.tempx, self.tempy

        self.player = player


# 이거 위치 조정해야됨.
class InvincibleItem(Item):
    """3초 동안 무적"""
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        if pygame.sprite.spritecollide(self, var.player_group, False, collided=check_collision):
            if not self.player.invincible:
                self.player.invincible = True
                self.player.invincible_end_time = time.time() + 3
            else:
                self.player.invincible_end_time += 3
            self.kill()


class InstantkillItem(Item):
    """"즉사 아이템"""
    def __init__(self, player):
        # self.image = pygame.transform.scale(pygame.image.load("questionbox.png"), (30, 30))
        super().__init__(player)
        self.added_time = time.time()

    def update(self):
        # 충돌 검사
        if pygame.sprite.spritecollide(self, var.player_group, False, collided=check_collision):
            self.player.kill()
        if time.time() - self.added_time > 3:
            self.kill()

class FreezeItem(Item):
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        if pygame.sprite.spritecollide(self, var.player_group, False, collided=check_collision):
            for item in var.arrows:
                if not item.freeze:
                    item.freeze = True
                    item.freeze_end_time = time.time() + 3
                else:
                    item.freeze_end_time += 3
            self.kill()

