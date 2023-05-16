import tkinter as tk
import sys
import Game
import variables
import pygame
import consts

class StartUI(tk.Frame):
    """메인 화면(tkinter) UI class"""

    def __init__(self, master):
        super().__init__(master)

        master.geometry("350x350")
        master.title("화살 피하기")
        self.master = master

        title_label = tk.Label(master, text="짭림고수", width=9, font=("Helvetica", 14))
        title_label.pack(side="top")
        game_start_button = tk.Button(master, height=4, width=8, text="게임 시작!", font=("Helvetica", 14),
                                      command=Game.game_start)
        game_start_button.pack(side="left")

        exit_button = tk.Button(master, height=4, width=8, text="게임 종료", font=("Helvetica", 14),
                                command=self.terminate)
        exit_button.pack(side="right")

        variables.show_score.set(f"최고 점수: {variables.top_score[0]}")
        score_label = tk.Label(master, textvariable=variables.show_score, font=("Helvetica", 14))
        score_label.pack(side="bottom")

        variables.show_time.set("최고 시간: {:02d}:{:02d}".format(variables.max_time[0] // 60, variables.max_time[0] % 60))
        time_label = tk.Label(master, textvariable=variables.show_time, font=("Helvetica", 14))
        time_label.pack(side="bottom")

        variables.show_level.set(f"최고 레벨: {variables.max_level[0]}")
        level_label = tk.Label(master, textvariable=variables.show_level, font=("Helvetica", 14))
        level_label.pack(side="bottom")

    def terminate(self):
        """tkinter 종료 (전체 프로그램 종료) 함수"""
        self.master.destroy()
        sys.exit()

class PygameUI():
    def __init__(self, screen, background, font):
        self.screen = screen
        self.bg_img = background
        self.font = font

    def draw_background(self):
        # 배경 이미지
        self.screen.blit(self.bg_img, (0, 0))

    def draw_circle(self):
        # 가운데 원 그리기
        pygame.draw.circle(self.screen, consts.const["circle_color"], consts.const["center"], consts.const["radius"],
                           consts.const["circle_width"])
        pygame.draw.circle(self.screen, (0, 0, 0), consts.const["center"],
                           consts.const["radius"] - consts.const["circle_width"])

    def show_score(self):
        score_text = self.font.render("Score: " + str(variables.current_score[0]), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_time(self, start_time, current_time):
        # 현재 경과 시간 표시

        variables.elapsed_time[0] = (current_time - start_time) // 1000  # 밀리초를 초 단위로 변환
        minutes = variables.elapsed_time[0] // 60  # 분 계산
        seconds = variables.elapsed_time[0] % 60  # 초 계산
        text = self.font.render("{:02d}:{:02d}".format(minutes, seconds), True, (255, 255, 255))
        self.screen.blit(text, (10, 40))

        return seconds

    def show_level(self):
        # 현재 레벨 표시
        level_text = self.font.render(f"Level: {variables.level[0]}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 70))