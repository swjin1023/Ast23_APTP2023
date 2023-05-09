import tkinter as tk
import sys
import Game
import variables
class UI(tk.Frame):
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
