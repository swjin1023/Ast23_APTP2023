import tkinter as tk

root = tk.Tk()  # tkinter root

# 전역 변수
current_score = [0]  # 점수 (매 게임 마다)
top_score = [0]  # 최고점
show_score = tk.StringVar()  # tkinter에 보여줄 최고점수 (tk.Stringvar() 형)

elapsed_time = [0]  # 경과 시간 (매 게임마다)
max_time = [0]  # 최고 경과 시간
show_time = tk.StringVar()  # tkinter에 보여줄 최고 경과 시간 (tk.Stringvar() 형)

level = [1]
max_level = [1]
show_level = tk.StringVar()

probability = [60]
