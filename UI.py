import tkinter as tk
from tkinter import ttk
import sys
import Game
import var
import pygame
import consts


# class StartUI(tk.Frame):
#     """메인 화면(tkinter) UI class"""
#
#     def __init__(self, master):
#         super().__init__(master)
#         self.dodge_game = Game.DodgeGame()
#
#         master.geometry("450x450")
#         master.title("화살 피하기")
#         self.master = master
#
#         title_label = tk.Label(master, text="짭림고수", width=9, font=("Helvetica", 14))
#         title_label.pack(side="top")
#         game_start_button = tk.Button(master, height=4, width=8, text="게임 시작!", font=("Helvetica", 14),
#                                       command=self.dodge_game.game_start)
#         game_start_button.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
#
#         game_start_button = tk.Button(master, height=4, width=8, text="최근 결과", font=("Helvetica", 14),
#                                       command=self.game_score_recent)
#         game_start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#
#         exit_button = tk.Button(master, height=4, width=8, text="게임 종료", font=("Helvetica", 14),
#                                 command=self.terminate)
#         exit_button.place(relx=0.8, rely=0.5, anchor=tk.CENTER)
#
#         var.show_level.set(f"최고 레벨: {var.max_level[0]}")
#         level_label = tk.Label(master, textvariable=var.show_level, font=("Helvetica", 14))
#         level_label.pack(side="bottom")
#
#         var.show_time.set("최고 시간: {:02d}:{:02d}".format(var.max_time[0] // 60, var.max_time[0] % 60))
#         time_label = tk.Label(master, textvariable=var.show_time, font=("Helvetica", 14))
#         time_label.pack(side="bottom")
#
#         var.show_score.set(f"최고 점수: {var.top_score[0]}")
#         score_label = tk.Label(master, textvariable=var.show_score, font=("Helvetica", 14))
#         score_label.pack(side="bottom")
#
#     def terminate(self):
#         """tkinter 종료 (전체 프로그램 종료) 함수"""
#         self.master.destroy()
#         sys.exit()
#
#     def game_score_recent(self):
#         new_window = tk.Toplevel(var.root)
#         new_window.title("최근 기록")
#         # 표 생성
#         self.table = ttk.Treeview(new_window)
#
#         # 열 이름 설정
#         self.table["columns"] = ("Name", "Age", "City")
#
#         # 각 열 설정
#         self.table.column("#0", width=50)  # 첫 번째 열(인덱스)의 너비 설정
#         self.table.column("Name", width=100)
#         self.table.column("Age", width=50)
#         self.table.column("City", width=100)
#
#         # 열 이름 표시
#         self.table.heading("#0", text="ID")
#         self.table.heading("Name", text="Name")
#         self.table.heading("Age", text="Age")
#         self.table.heading("City", text="City")
#
#         # 데이터 추가
#         self.table.insert(parent='', index='end', text="0", values=("John Doe", 30, "New York"))
#         self.table.insert(parent='', index='end', text="1", values=("Jane Smith", 25, "London"))
#         self.table.insert(parent='', index='end', text="2", values=("Bob Johnson", 35, "Paris"))
#
#         # 표 배치
#         self.table.pack()

class PygameUI:
    def __init__(self, screen, background, font):
        self.screen = screen
        self.bg_img = background
        self.font = font


class MainGameUI(PygameUI):
    def draw_background(self):
        """배경 이미지 blit"""
        self.screen.blit(self.bg_img, (0, 0))

    def draw_circle_boundary(self):
        """가운데 원 그리기"""
        pygame.draw.circle(self.screen, consts.color["white"], consts.const["center"], consts.const["radius"])
        pygame.draw.circle(self.screen, consts.color["black"], consts.const["center"],
                           consts.const["radius"] - consts.const["circle_width"])

    def show_score(self, x, y):
        """점수 text blit"""
        score_text = self.font.render("Score: " + str(var.current_score[0]), True, (255, 255, 255))
        self.screen.blit(score_text, (x, y))

    def show_time(self, start_time, current_time, x, y):
        """현재 경과 시간 표시"""
        var.elapsed_time[0] = current_time - start_time  # 밀리초를 초 단위로 변환
        minutes = var.elapsed_time[0] // 60000  # 분 계산
        seconds = (var.elapsed_time[0] // 1000) % 60  # 초 계산
        text = self.font.render("{:02d}:{:02d}".format(minutes, seconds), True, (255, 255, 255))
        self.screen.blit(text, (x, y))
        return seconds

    def show_level(self, x, y):
        # 현재 레벨 표시
        level_text = self.font.render(f"Level: {var.level[0]}", True, (255, 255, 255))
        self.screen.blit(level_text, (x, y))

    def show_level_left_time(self, x, y, level_up_time, current_time):
        if level_up_time > current_time:
            left_time = level_up_time - current_time
            level_left_time_text = self.font.render(
                f"Next Level in {(left_time // 1000) % 60:02d}:{left_time % 1000:02d}sec", True, consts.color["white"])
            self.screen.blit(level_left_time_text, (x, y))
        else:
            self.screen.blit(self.font.render("Level Up!", True, consts.color["white"]), (x, y))


class EndUI(PygameUI):
    def game_over_screen(self):
        # Game over screen
        game_over_text = self.font.render("Game Over", True, consts.color["black"])
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (consts.const["screen_width"] / 2, consts.const["screen_height"] / 2 - 50)
        self.screen.blit(game_over_text, game_over_rect)

    def show_score(self):
        """이번 게임 score"""
        score_text = self.font.render(f"Score: {var.current_score[0]}", True, consts.color["black"])
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (consts.const["screen_width"] / 2 - 8,
                                  consts.const["screen_height"] / 2 + 10)
        self.screen.blit(score_text, score_text_rect)

    def show_time(self):
        """이번 게임 경과 시간"""
        time_text = self.font.render("time: {:02d}:{:02d}".format(var.elapsed_time[0] // 60000,
                                                                  (var.elapsed_time[0] // 1000) % 60),
                                     True, (0, 0, 0))
        time_text_rect = time_text.get_rect()
        time_text_rect.center = (consts.const["screen_width"] / 2 - 13,
                                 consts.const["screen_height"] / 2 + 50)
        self.screen.blit(time_text, time_text_rect)

    def show_level(self):
        """이번 게임 최대 레벨"""
        level_text = self.font.render(f"Level: {var.level[0]}", True, consts.color["black"])
        level_text_rect = level_text.get_rect()
        level_text_rect.center = (consts.const["screen_width"] / 2 - 26,
                                  consts.const["screen_height"] / 2 + 90)
        self.screen.blit(level_text, level_text_rect)
