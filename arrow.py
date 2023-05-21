import pygame
import random
import consts
import var
from player import check_collision
import time
class Arrow(pygame.sprite.Sprite):
    """화살 객체 Parent"""

    def __init__(self, player):
        super().__init__()
        self.image = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load("arrow.png").convert_alpha(), (10, 25)), False, True)  # 이미지 가져오기
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  # 화살 이미지 좌측 상단 모서리의 x, y 좌표 가져옴
        self.width = self.image.get_width()  # 화살 너비
        self.height = self.image.get_height()  # 화살 높이

        self.screen_height = consts.const["screen_height"]
        self.screen_width = consts.const["screen_width"]
        self.screen_radius = consts.const["radius"]
        self.screen_center = consts.const["center"]
        # self.speed = consts.const["arrow_speed"]  # 화살 이동 속도
        self.level = var.level[0]

        # 화살 delta값
        # self.dx = self.speed
        # self.dy = self.speed

        self.player = player

        self.freeze = False
        self.freeze_end_time = 0

    def update(self):
        if pygame.sprite.spritecollide(self.player, var.arrows, True, collided=check_collision):
            if self.player.invincible:
                var.current_score[0] += 1
            else:
                self.player.kill()
        if self.freeze:
            if time.time() >= self.freeze_end_time:
                var.arrow_speed[0] = 1
                self.freeze = False
            else:
                var.arrow_speed[0] = 0



class TopArrow(Arrow):
    """화살 객체 (위->아래)"""

    def __init__(self, player):
        super().__init__(player)
        self.rect.centerx = random.randint(self.screen_center[0] - self.screen_radius,
                                           self.screen_center[0] + self.screen_radius - self.width)  # 화살 x좌표 변경
        self.rect.centery = 0  # 화살 y좌표 변경

    def update(self):  # 게임 frame당 변화
        # 화살 이동
        for i in range(0, self.level):
            self.rect.centery += var.arrow_speed[0] #self.dy  # 기본값은 위에서 아래로 내려오는 것.
            if self.rect.y > self.screen_height:  # 화면 밖으로 나갔는지 확인
                self.kill()  # 객체 삭제
                var.current_score[0] += 1
        super().update()

        # 왼쪽 위가 (0,0)이다!


class LeftArrow(Arrow):
    """화살 객체 (왼쪽->오른쪽)"""

    def __init__(self, player):
        super().__init__(player)
        self.image = pygame.transform.rotate(self.image, 90)  # 이미지 회전
        self.width = self.image.get_width()  # 화살 너비
        self.height = self.image.get_height()  # 화살 높이
        self.rect.centerx = 0  # 화살 x좌표 변경
        self.rect.centery = random.randint(self.screen_center[1] - self.screen_radius,
                                           self.screen_center[1] + self.screen_radius - self.height)  # 화살 y좌표 변경

    def update(self):
        for i in range(0, self.level):
            self.rect.centerx += var.arrow_speed[0]#self.dx
            if self.rect.x > self.screen_width:
                self.kill()
                var.current_score[0] += 1
        super().update()


class RightArrow(Arrow):
    """화살 객체 (오른쪽->왼쪽)"""

    def __init__(self, player):
        super().__init__(player)
        self.image = pygame.transform.rotate(self.image, -90)
        self.width = self.image.get_width()  # 화살 너비
        self.height = self.image.get_height()  # 화살 높이
        self.rect.centerx = self.screen_width - self.width  # 화살 x좌표 변경
        self.rect.centery = random.randint(self.screen_center[1] - self.screen_radius,
                                           self.screen_center[1] + self.screen_radius - self.height)  # 화살 y좌표 변경

    def update(self):
        for i in range(0, self.level):
            self.rect.centerx -= var.arrow_speed[0]#self.dx
            if self.rect.x < 0:
                self.kill()
                var.current_score[0] += 1
        super().update()


class BottomArrow(Arrow):
    """화살 객체 (아래->위)"""

    def __init__(self, player):
        super().__init__(player)
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect.centerx = random.randint(self.screen_center[0] - self.screen_radius,
                                           self.screen_center[0] + self.screen_radius - self.width)  # 화살 x좌표 변경
        self.rect.centery = self.screen_height - self.height  # 화살 y좌표 변경

    def update(self):
        # 화살 이동
        for i in range(0, self.level):
            self.rect.centery -= var.arrow_speed[0]#self.dy
            # 화면 밖으로 나갔는지 확인
            if self.rect.y < 0:
                self.kill()
                var.current_score[0] += 1
        super().update()
