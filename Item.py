import pygame
import consts

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("star.png"), (30, 30))  # 기본값: 별 (무적 아이템)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()


# 이거 위치 조정해야됨.
class InvincibleItem(Item):
    """3초 동안 무적"""
    def __init__(self):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = consts.data_constant["center"][0] + 40
        self.rect.y = consts.data_constant["center"][1] + 40


class InvincbleItemCollision(pygame.sprite.Sprite):
    def __init__(self, player, player_group, item_group):
        super().__init__(player_group)  # player group으로부터 상속
        self.player_sprite = player
        self.collision_time = 0
        self.invincible_item_group = item_group

    def update(self):
        # 충돌 검사
        if pygame.sprite.spritecollide(self.player_sprite, self.invincible_item_group, True):
            # 충돌이 발생한 시간 저장
            self.collision_time = pygame.time.get_ticks()

            # 충돌한 sprite2(Item) 찾기
            for sprite2 in pygame.sprite.spritecollide(self.player_sprite, self.invincible_item_group, False):
                sprite2.kill()

        # 일정 시간이 지나면 속성 변경
        if self.collision_time > 0 and pygame.time.get_ticks() - self.collision_time < 4000:  # 4초 지속
            self.player_sprite.invincible = True
        else:
            self.player_sprite.invincible = False



