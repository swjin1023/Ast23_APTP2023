import UI
import pygame
import random

import player as pl
import Item
import arrow

import var
import consts


def save_score():
    # 충돌 후, 최고 점수 및 최고 시간 전역 변수에 기록
    if var.current_score[0] > var.top_score[0]:
        var.top_score[0] = var.current_score[0]
    if var.elapsed_time[0] > var.max_time[0]:
        var.max_time[0] = var.elapsed_time[0]
    if var.level[0] > var.max_level[0]:
        var.max_level[0] = var.level[0]


def reset_var():
    var.show_level.set(f"최고 레벨: {var.max_level[0]}")
    var.show_score.set(f"최고 점수: {str(var.top_score[0])}")
    var.show_time.set("최고 시간: {:02d}:{:02d}".format(var.max_time[0] // 60, var.max_time[0] % 60))

    var.probability[0] = 60
    var.level[0] = 1
    var.current_score[0] = 0
    var.elapsed_time[0] = 0


class Game:
    def __init__(self):
        self.screen = None
        self.bg_img = pygame.transform.scale(pygame.image.load("background.jpg"),
                                             (consts.const["screen_width"], consts.const["screen_height"]))

    def game_over(self):
        pass

    def game_start(self):
        pygame.init()

    def add_player(self):
        player = pl.Player()
        var.player_group.add(player)
        var.all_sprites.add(player)
        return player

    def make_arrow(self, player):
        pass

    def add_item(self, sprite, sprite_group):
        new_item = sprite
        var.all_sprites.add(new_item)
        var.items.add(new_item)
        sprite_group.add(new_item)


class DodgeGame(Game):

    def __init__(self):
        super().__init__()
        self.player = None

    def make_arrow(self, player):
        arrow_select = random.randint(1, var.probability[0])
        if len(var.arrows.sprites()) < var.level[0] * 10:
            if arrow_select == 1:
                new_arrow = arrow.TopArrow(player)
            elif arrow_select == 2:
                new_arrow = arrow.LeftArrow(player)
            elif arrow_select == 3:
                new_arrow = arrow.RightArrow(player)
            elif arrow_select == 4:
                new_arrow = arrow.BottomArrow(player)
            else:
                return
            var.arrows.add(new_arrow)
            var.all_sprites.add(new_arrow)

    def game_over(self):
        """게임 종료 함수"""
        self.screen.fill(consts.color["white"])
        font = pygame.font.SysFont(None, 50)
        baseUI = UI.EndUI(self.screen, None, font)

        UI.EndUI.game_over_screen(baseUI)
        UI.EndUI.show_time(baseUI)
        UI.EndUI.show_level(baseUI)
        UI.EndUI.show_score(baseUI)

        pygame.display.update()
        pygame.time.wait(2000)

        # Quit pygame
        pygame.quit()
        reset_var()

    def game_start(self):
        """게임 시작 함수"""
        super().game_start()
        self.player = self.add_player()
        self.screen = pygame.display.set_mode(
            (consts.const["screen_width"], consts.const["screen_height"]))  # pygame screen
        pygame.display.set_caption("화살 피하기 게임")
        self.screen.blit(self.bg_img, (0, 0))

        # save start time, set level-up time
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()  # 경과 시간 표시하기 위해 가져옴.
        level_up_time = 7000

        # event
        running = True
        while running:
            var.all_sprites.update()
            var.all_sprites.draw(self.screen)
            pygame.display.update()

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # UI
            font = pygame.font.SysFont(None, 30)
            baseUI = UI.MainGameUI(self.screen, self.bg_img, font)
            UI.MainGameUI.draw_background(baseUI)
            UI.MainGameUI.draw_circle(baseUI)
            UI.MainGameUI.show_score(baseUI)
            UI.MainGameUI.show_level(baseUI)
            current_time = pygame.time.get_ticks()
            seconds = UI.MainGameUI.show_time(baseUI, start_time, current_time)

            # FPS
            clock.tick(60)

            # make arrow
            self.make_arrow(self.player)

            # level up
            if seconds > 0 and (current_time - start_time) >= level_up_time:
                var.level[0] += 1

                tempnum = random.randint(0, 10)  # 난이도 올라갈떄마다 아이템 추가하도록 업데이트
                if tempnum == 4 or 5 or 6 or 7:
                    invincible_item = Item.InvincibleItem(self.player)
                    self.add_item(invincible_item, var.invincible_group)
                else:
                    instantkill_item = Item.InstantkillItem(self.player)
                    self.add_item(instantkill_item, var.instantkill_group)

                if var.probability[0] > 15:
                    var.probability[0] -= 3
                level_up_time += 7000

            if self.player.invincible:
                invincible_text = font.render("INVINCIBLE!!", True, (255, 255, 255))
                self.screen.blit(invincible_text, (10, 100))

            # 플레이어가 죽으면 중지
            if len(var.player_group.sprites()) == 0:
                running = False

            # 게임 로직 및 게임 화면 update & draw


        save_score()
        var.all_sprites.empty()
        var.arrows.empty()
        self.game_over()
