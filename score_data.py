import tkinter as tk
from tkinter import ttk
import csv
import os

columns = ["경과 시간", "레벨", "점수"]

data_file = "../data.csv"

def initialize_data_file():
    with open(data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)


def load_data():
    """데이터 파일에서 기록을 로드합니다."""
    try:
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        data = []
    return data

def save_data(data):
    """데이터를 파일에 저장합니다."""
    with open(data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def update_table():
    """표를 업데이트합니다."""
    data = load_data()
    table.delete(*table.get_children())  # 기존 표의 모든 행 삭제
    for record in data:
        table.insert('', 'end', values=record)

def add_record(time, level, score):
    """새로운 기록을 추가합니다."""
    # 예시: 아래 코드는 임의의 랜덤 값을 사용합니다.
    # import random
    # time = random.randint(1, 100)
    # level = random.randint(1, 10)
    # score = random.randint(100, 1000)

    data = load_data()
    data.append([time, level, score])
    save_data(data)
    update_table()

def on_closing():
    """프로그램이 종료될 때 호출되는 함수입니다."""
    os.remove(data_file)  # 데이터 파일 삭제


def show_game_score_recent():
    pass

# 데이터 파일 초기화
initialize_data_file()

# Tkinter 애플리케이션 생성
root = tk.Tk()
root.title("게임 기록")
root.geometry("400x300")

# 표 생성
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
table.pack(pady=10)

# 데이터 로드 및 표 업데이트
update_table()

# 기록 추가 버튼
add_button = ttk.Button(root, text="기록 추가", command=add_record)
add_button.pack()

# 프로그램 종료 시 호출되는 함수 등록
root.protocol("WM_DELETE_WINDOW", on_closing)

# Tkinter 이벤트 루프 시작
root.mainloop()
