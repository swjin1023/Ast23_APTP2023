import consts
import var

import pygame
import random
import time

class Item(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("star.png"), (30, 30))  # 기본값: 별 (무적 아이템)
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
        self.rect.x = self.tempx
        self.rect.y = self.tempy

        self.player = player


# 이거 위치 조정해야됨.
class InvincibleItem(Item):
    """3초 동안 무적"""
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        if pygame.sprite.spritecollide(self, var.player_group, False):
            if not self.player.invincible:
                self.player.invincible = True
                self.player.invincible_end_time = time.time() + 3
            else:
                self.player.invincible_end_time += 3
            self.kill()


class InstantkillItem(Item):
    """"즉사 아이템"""
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        # 충돌 검사
        if pygame.sprite.spritecollide(self, var.player_group, False):
            self.player.kill()


