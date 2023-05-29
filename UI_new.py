import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QTableWidget, \
    QTableWidgetItem, QGridLayout, QSizePolicy, QWhatsThis
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import csv
import Game
import var


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.ismillitime = ismillitime

    def __lt__(self, other):
        # 숫자 비교를 위한 재정의된 작은 값 비교 메서드
        # if self.ismillitime is not None:
        #     try:
        #         return float(self.ismillitime.data(Qt.EditRole)) < float(other.ismillitime.data(Qt.EditRole))
        #     except ValueError:
        #         return super().__lt__(other)
        # else:
        try:
            return float(self.data(Qt.EditRole)) < float(other.data(Qt.EditRole))
        except ValueError:
            return super().__lt__(other)

class GameRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("게임 기록")
        self.resize(500, 400)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["경과 시간(초)", "레벨", "점수"])
        # self.font = QtGui.QFont("noto", 10)
        # self.table_widget.setFont(self.font)
        self.table_widget.setSortingEnabled(True)
        self.currentSortedStatus = None
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.setWhatsThis("This is a help text for the dialog.")
        self.load_records()
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)

    def write_in_table(self, data):
        self.table_widget.setRowCount(len(data))
        for row, record in enumerate(data):
            for column, value in enumerate(record):
                if column == 0:
                    # minutes = (int(value) // 1000) // 60
                    seconds = (int(value) // 1000) % 60
                    milliseconds = int(value) % 1000
                    item = NumericTableWidgetItem(f"{seconds}.{milliseconds}")
                else:
                    item = NumericTableWidgetItem(value)
                self.table_widget.setItem(row, column, item)
                item.setTextAlignment(Qt.AlignCenter)

    def load_records(self):
        file = open('game_records.csv', 'r')
        reader = csv.reader(file)
        headers = next(reader)  # skip headers
        records = list(reader)
        self.write_in_table(records)

    def sort_table(self, column_index):
        if self.currentSortedStatus == Qt.AscendingOrder:
            self.table_widget.sortItems(column_index, Qt.DescendingOrder)
            self.currentSortedStatus = Qt.DescendingOrder
        else:
            self.table_widget.sortItems(column_index, Qt.AscendingOrder)
            self.currentSortedStatus = Qt.AscendingOrder

    def closeEvent(self, event):
        self.currentSortedStatus = None
        self.load_records()
        self.table_widget.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)  # 정렬 상태 초기화
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)
        self.setWindowTitle("죽림고수")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.score_label = QLabel("최고 점수: None")
        self.score_label.setSizePolicy(size_policy)
        # self.setCentralWidget(self.score_label)
        # self.score_label.font()
        # self.score_label.setGeometry(150, 200, 70, 60)

        self.level_label = QLabel("최고 레벨: None")
        self.level_label.setSizePolicy(size_policy)
        # self.setCentralWidget(self.level_label)
        # self.level_label.font()
        # self.level_label.setGeometry(200, 200, 70, 60)

        self.time_label = QLabel("최고 시간: None")
        self.time_label.setSizePolicy(size_policy)
        # self.setCentralWidget(self.time_label)
        # self.time_label.font()
        # self.time_label.setGeometry(250, 200, 70, 60)

        self.headers = ["score", "level", "time"]
        self.create_csv_file("game_records.csv", self.headers)
        self.game_record_dialog = GameRecordDialog(self)

        self.dodge_game = Game.DodgeGame()
        game_start_button = QPushButton("게임 실행", self)
        game_start_button.clicked.connect(self.game_start)
        game_start_button.setSizePolicy(size_policy)
        # game_start_button.setGeometry(None, None, aw=110, ah=100)

        game_record_button = QPushButton("게임 기록", self)
        game_record_button.clicked.connect(self.show_game_records)
        game_record_button.setSizePolicy(size_policy)
        # game_record_button.setGeometry(None, None, aw=110, ah=100)

        game_exit_button = QPushButton("게임 종료", self)
        game_exit_button.clicked.connect(self.close)
        game_exit_button.setSizePolicy(size_policy)
        # game_exit_button.setGeometry(None, None, aw=110, ah=100)

        # toolbar = self.addToolBar("Toolbar")
        # toolbar.addWidget(game_start_button)
        # toolbar.addWidget(game_record_button)
        # toolbar.addWidget(game_exit_button)

        layout.addWidget(game_start_button, 0, 0)
        layout.addWidget(game_record_button, 0, 1)
        layout.addWidget(game_exit_button, 0, 2)
        layout.addWidget(self.score_label, 2, 0)
        layout.addWidget(self.level_label, 3, 0)
        layout.addWidget(self.time_label, 4, 0)

        font = QtGui.QFont()
        font.setPointSize(11)
        for index in range(layout.count()):
            widget = layout.itemAt(index).widget()
            if widget is not None:
                widget.setFont(font)

        self.best_score = 0
        self.best_level = 0
        self.best_time = 0

    def game_start(self):
        self.dodge_game.game_start()
        score = var.current_score[0]
        level = var.level[0]
        time = var.elapsed_time[0]
        Game.save_score()
        # self.update_best_score(score, level)
        self.add_record(time, level, score)
        self.update_best_score(var.top_score[0], var.max_level[0], var.max_time[0])
        Game.reset_var()

    def update_best_score(self, score, level, time):
        if score >= self.best_score:
            self.best_score = score
            self.score_label.setText(f"최고 점수: {self.best_score}")
        if level >= self.best_level:
            self.best_level = level
            self.level_label.setText(f"최고 레벨: {self.best_level}")
        if time >= self.best_time:
            self.best_time = time
            self.time_label.setText(f"최고 시간: {self.best_time}")

    def add_record(self, millitime, level, score):
        with open('game_records.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # minutes = (millitime // 1000) // 60
            # seconds = (millitime // 1000) % 60
            writer.writerow([millitime, level, score])

    def show_game_records(self):
        self.game_record_dialog.load_records()
        self.game_record_dialog.exec_()

    def create_csv_file(self, filename, headers=None):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)

    def on_closing(self):
        with open('game_records.csv', 'w') as file:
            file.truncate()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    app.aboutToQuit.connect(main_window.on_closing)
    sys.exit(app.exec_())
