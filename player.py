import pygame
import consts
import var
import time

class Player(pygame.sprite.Sprite):
    """player 객체"""

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("target.png").convert_alpha(), (20, 20))
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = self.image.get_width() // 2
        self.rect = self.image.get_rect()
        # self.width = self.image.get_width()
        # self.height = self.image.get_height()

        self.rect.center = self.center = consts.const["center"]
        self.player_speed = consts.const["player_speed"]
        self.radius = consts.const["radius"]

        # 객체 이동속도
        self.speed = self.player_speed

        # 무적 상태 (기본: False)
        self.invincible = False
        self.invincible_end_time = 0

    def update(self):
        # 목표물 이동
        status = (self.rect.centerx - self.center[0]) ** 2 + (self.rect.centery - self.center[1]) ** 2
        before = self.rect.center
        # x_before, y_before = self.rect.centerx, self.rect.centery
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and status < self.radius ** 2:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and status < self.radius ** 2:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and status < self.radius ** 2:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and status < self.radius ** 2:
            self.rect.y += self.speed

        status = (self.rect.centerx - self.center[0]) ** 2 + (self.rect.centery - self.center[1]) ** 2
        if status >= self.radius ** 2:
            self.rect.center = before
            # self.rect.x = x_before
            # self.rect.y = y_before

        # invincible 속성 update 기준
        if self.invincible and time.time() >= self.invincible_end_time:
            time.sleep(1)
            self.invincible = False
