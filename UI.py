import enum
import tkinter as tk
import sys
import Game
import var
import pygame
import consts


class StartUI(tk.Frame):
    """메인 화면(tkinter) UI class"""

    def __init__(self, master):
        super().__init__(master)
        self.dodge_game = Game.DodgeGame()

        master.geometry("350x350")
        master.title("화살 피하기")
        self.master = master

        title_label = tk.Label(master, text="짭림고수", width=9, font=("Helvetica", 14))
        title_label.pack(side="top")
        game_start_button = tk.Button(master, height=4, width=8, text="게임 시작!", font=("Helvetica", 14),
                                      command=self.dodge_game.game_start)
        game_start_button.pack(side="left")

        exit_button = tk.Button(master, height=4, width=8, text="게임 종료", font=("Helvetica", 14),
                                command=self.terminate)
        exit_button.pack(side="right")

        var.show_level.set(f"최고 레벨: {var.max_level[0]}")
        level_label = tk.Label(master, textvariable=var.show_level, font=("Helvetica", 14))
        level_label.pack(side="bottom")

        var.show_time.set("최고 시간: {:02d}:{:02d}".format(var.max_time[0] // 60, var.max_time[0] % 60))
        time_label = tk.Label(master, textvariable=var.show_time, font=("Helvetica", 14))
        time_label.pack(side="bottom")

        var.show_score.set(f"최고 점수: {var.top_score[0]}")
        score_label = tk.Label(master, textvariable=var.show_score, font=("Helvetica", 14))
        score_label.pack(side="bottom")

    def terminate(self):
        """tkinter 종료 (전체 프로그램 종료) 함수"""
        self.master.destroy()
        sys.exit()


class PygameUI:
    def __init__(self, screen, background, font):
        self.screen = screen
        self.bg_img = background
        self.font = font


class MainGameUI(PygameUI):
    def draw_background(self):
        # 배경 이미지
        self.screen.blit(self.bg_img, (0, 0))

    def draw_circle(self):
        # 가운데 원 그리기
        pygame.draw.circle(self.screen, consts.color["white"], consts.const["center"], consts.const["radius"])
        pygame.draw.circle(self.screen, consts.color["black"], consts.const["center"],
                           consts.const["radius"] - consts.const["circle_width"])

    def show_score(self):
        score_text = self.font.render("Score: " + str(var.current_score[0]), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_time(self, start_time, current_time):
        # 현재 경과 시간 표시

        var.elapsed_time[0] = (current_time - start_time) // 1000  # 밀리초를 초 단위로 변환
        minutes = var.elapsed_time[0] // 60  # 분 계산
        seconds = var.elapsed_time[0] % 60  # 초 계산
        text = self.font.render("{:02d}:{:02d}".format(minutes, seconds), True, (255, 255, 255))
        self.screen.blit(text, (10, 40))

        return seconds

    def show_level(self):
        # 현재 레벨 표시
        level_text = self.font.render(f"Level: {var.level[0]}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 70))


class EndUI(PygameUI):
    def game_over_screen(self):
        # Game over screen
        game_over_text = self.font.render("Game Over", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (consts.const["screen_width"] / 2, consts.const["screen_height"] / 2 - 50)
        self.screen.blit(game_over_text, game_over_rect)

    def show_score(self):
        # 이번 게임 score
        score_text = self.font.render(f"Score: {var.current_score[0]}", True, (0, 0, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (consts.const["screen_width"] / 2 - 8,
                                         consts.const["screen_height"] / 2 + 10)
        self.screen.blit(score_text, score_text_rect)

    def show_time(self):
        # 이번 게임 경과 시간
        time_text = self.font.render("time: {:02d}:{:02d}".format(var.elapsed_time[0] // 60,
                                                                  var.elapsed_time[0] % 60),
                                     True, (0, 0, 0))
        time_text_rect = time_text.get_rect()
        time_text_rect.center = (consts.const["screen_width"] / 2 - 13,
                                        consts.const["screen_height"] / 2 + 50)
        self.screen.blit(time_text, time_text_rect)

    def show_level(self):
        # 이번 게임 최대 레벨
        level_text = self.font.render(f"Level: {var.level[0]}", True, (0, 0, 0))
        level_text_rect = level_text.get_rect()
        level_text_rect.center = (consts.const["screen_width"] / 2 - 26,
                                         consts.const["screen_height"] / 2 + 90)
        self.screen.blit(level_text, level_text_rect)


class PlayerStatus(PygameUI):
    def __init__(self, screen, player, font):
        super().__init__(screen, None, font)
        self.player = player

    def invincible(self):
        if self.player.invincible:
            invincible_text = self.font.render("INVINCIBLE!!", True, (255, 255, 255))
            self.screen.blit(invincible_text, (10, 100))
