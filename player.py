import pygame


class Player(pygame.sprite.Sprite):
    """player 객체"""
    def __init__(self, _center, _player_speed, _radius):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("target.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.center = _center
        self.player_speed = _player_speed
        self.radius = _radius

        # 초기 위치: 중앙
        self.rect.x = self.center[0]
        self.rect.y = self.center[1]
        # 객체 이동속도
        self.speed = self.player_speed

        # 무적 상태 (기본: False)
        self.invincible = False

    def update(self):
        # 목표물 이동
        status = (self.rect.x - self.center[0]) ** 2 + (self.rect.y - self.center[1]) ** 2
        x_before, y_before = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and status < self.radius ** 2:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and status < self.radius ** 2:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and status < self.radius ** 2:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and status < self.radius ** 2:
            self.rect.y += self.speed

        status = (self.rect.x - self.center[0]) ** 2 + (self.rect.y - self.center[1]) ** 2
        if status >= self.radius ** 2:
            self.rect.x = x_before
            self.rect.y = y_before
