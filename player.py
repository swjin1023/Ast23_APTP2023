import pygame
import consts
import time


def check_collision(player, other_sprite):
    # 원형 히트박스를 고려한 충돌 감지 로직
    # if isinstance(other_sprite, Player):
    #     # 플레이어와 플레이어 사이의 충돌을 처리할 경우
    #     distance = player.rect.center - other_sprite.rect.center
    #     return distance.length() <= player.radius + other_sprite.radius
    # else:
    # 플레이어와 다른 스프라이트 사이의 충돌을 처리할 경우
    # offset_x = other_sprite.rect.x - player.rect.centerx
    # offset_y = other_sprite.rect.y - player.rect.centery
    # overlap = player.mask.overlap(other_sprite.mask, (offset_x, offset_y))
    # return overlap is not None
    return pygame.sprite.collide_mask(player, other_sprite)


class Player(pygame.sprite.Sprite):
    """player 객체"""

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("target.png").convert_alpha(), (20, 20))
        self.surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.center = self.center = consts.const["center"]
        self.radius = self.image.get_width() // 2

        pygame.draw.circle(self.surface, consts.color["black"], self.center, self.radius)
        self.surface.blit(self.image, (0, 0))
        self.mask = pygame.mask.from_surface(self.surface)

        self.player_speed = consts.const["player_speed"]
        self.screen_radius = consts.const["radius"]

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
        if keys[pygame.K_LEFT] and status < self.screen_radius ** 2:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and status < self.screen_radius ** 2:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and status < self.screen_radius ** 2:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and status < self.screen_radius ** 2:
            self.rect.y += self.speed

        status = (self.rect.centerx - self.center[0]) ** 2 + (self.rect.centery - self.center[1]) ** 2
        if status >= self.screen_radius ** 2:
            self.rect.center = before

        # invincible 속성 update 기준
        if self.invincible and time.time() >= self.invincible_end_time:
            self.invincible = False


