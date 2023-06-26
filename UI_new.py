from datetime import datetime
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5 import QtGui
import csv
import Game
import var
import pygame
import consts

global ItemMode, volume
ItemMode = True

volume = 0.5


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


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __lt__(self, other):
        # 숫자 비교를 위한 재정의된 작은 값 비교 메서드

        try:
            return float(self.data(Qt.EditRole)) < float(other.data(Qt.EditRole))
        except ValueError:
            return super().__lt__(other)


class GameSettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(508, 363)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(70, 160, 371, 151))
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")

        self.ItemModeCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.ItemModeCheckBox.setGeometry(QtCore.QRect(40, 40, 96, 19))
        self.ItemModeCheckBox.setObjectName("checkBox")
        self.ItemModeCheckBox.setChecked(True)
        self.ItemModeCheckBox.stateChanged.connect(self.setItemMode)

        self.arrowSpeedBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.arrowSpeedBox.setGeometry(QtCore.QRect(220, 70, 91, 22))
        self.arrowSpeedBox.setMaximum(10.0)
        self.arrowSpeedBox.setMinimum(0.1)
        self.arrowSpeedBox.setSingleStep(0.1)
        self.arrowSpeedBox.setProperty("value", 1.0)
        self.arrowSpeedBox.setObjectName("doubleSpinBox")
        self.arrowSpeedBox.valueChanged.connect(self.changeArrowSpeed)

        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(40, 72, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(40, 102, 101, 16))
        self.label_3.setObjectName("label_3")

        self.lvupTimeBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.lvupTimeBox.setGeometry(QtCore.QRect(220, 100, 91, 22))
        self.lvupTimeBox.setMaximum(16)
        self.lvupTimeBox.setSingleStep(1)
        self.lvupTimeBox.setMinimum(1)
        self.lvupTimeBox.setProperty("value", 8)
        self.lvupTimeBox.setObjectName("doubleSpinBox_2")
        self.lvupTimeBox.valueChanged.connect(self.changeLevelUpTime)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(70, 50, 371, 91))
        self.groupBox.setObjectName("groupBox")

        self.volumeSlider = QtWidgets.QSlider(self.groupBox)
        self.volumeSlider.setGeometry(QtCore.QRect(180, 40, 160, 22))
        self.volumeSlider.setSliderPosition(50)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setInvertedAppearance(False)
        self.volumeSlider.setInvertedControls(False)
        self.volumeSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.volumeSlider.setTickInterval(10)
        self.volumeSlider.setObjectName("horizontalSlider")
        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 40, 101, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_2.setTitle(_translate("Dialog", "Difficulty"))
        self.ItemModeCheckBox.setText(_translate("Dialog", "Item"))
        self.arrowSpeedBox.setToolTip(_translate("Dialog", "<html><head/><body><p>dx, dy value</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Arrow Speed"))
        self.label_3.setText(_translate("Dialog", "Level Up Time"))
        self.lvupTimeBox.setToolTip(_translate("Dialog", "<html><head/><body><p>seconds</p></body></html>"))
        self.groupBox.setTitle(_translate("Dialog", "Sound"))
        self.label.setText(_translate("Dialog", "Master Volume"))

    def changeArrowSpeed(self):
        var.arrow_speed[0] = self.arrowSpeedBox.value()

    def changeLevelUpTime(self):
        var.level_up_time[0] = self.lvupTimeBox.value() * 1000

    def setItemMode(self):
        global ItemMode
        if self.ItemModeCheckBox.isChecked():
            ItemMode = True
        else:
            ItemMode = False

    def changeVolume(self):
        global volume
        volume = self.volumeSlider.value() / 100.0
        pygame.mixer.music.set_volume(volume)

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

        # self.setWhatsThis("This is a help text for the dialog.")
        self.load_records()
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)

    def write_in_table(self, data):
        self.table_widget.setRowCount(len(data))
        for row, record in enumerate(data):
            for column, value in enumerate(record):
                if column == 0:
                    # minutes = (int(value) // 1000) // 60
                    seconds = (int(value) // 1000) % 60 + ((int(value) // 1000) // 60) * 60
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


class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)
        self.setWindowTitle("죽림고수")

        file_path = "main_bg.mp3"
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume)

        self.dodge_game = Game.DodgeGame()

        self.headers = ["score", "level", "time"]
        self.create_csv_file("game_records.csv", self.headers)
        self.game_record_dialog = GameRecordDialog(self)
        self.game_setting_widget = GameSettingDialog(self)

        self.best_score = 0
        self.best_level = 0
        self.best_time = 0
        label_color = "white"
        style_sheet = f"color: {label_color};"
        # self.set_transparent_image("background2.png", 0.5)  # 이미지 파일 경로와 투명도를 설정합니다.
        self.set_background_image("background.jpg")

        self.timer = QTimer(self)
        self.show_today_date()
        self.timer.start(1000)
        self.timer.timeout.connect(self.show_today_date)

        self.font = QtGui.QFont()
        self.font.setFamily("맑은 고딕")
        self.font.setPointSize(14)

        self.setObjectName("MainWindow")
        self.resize(798, 585)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 60, 471, 91))
        self.label.setStyleSheet(style_sheet)

        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(28)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(400, 200, 291, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gameStartButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.gameStartButton.clicked.connect(self.game_start)
        # font = QtGui.QFont()
        # font.setFamily("맑은 고딕")
        # font.setPointSize(16)
        self.gameStartButton.setFont(self.font)
        self.gameStartButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.gameStartButton)
        self.recordButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.recordButton.clicked.connect(self.show_game_records)
        # font = QtGui.QFont()
        # font.setFamily("맑은 고딕")
        # font.setPointSize(16)
        self.recordButton.setFont(self.font)
        self.recordButton.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.recordButton)
        self.settingButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.settingButton.clicked.connect(self.show_game_setting)
        # font = QtGui.QFont()
        # font.setFamily("맑은 고딕")
        # font.setPointSize(16)
        self.settingButton.setFont(self.font)
        self.settingButton.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.settingButton)
        self.exitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.exitButton.clicked.connect(self.close)
        # font = QtGui.QFont()
        # font.setFamily("맑은 고딕")
        # font.setPointSize(16)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(90, 230, 241, 141))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.time_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        scoreGroupLabelFont = QtGui.QFont()
        scoreGroupLabelFont.setFamily("맑은 고딕")
        scoreGroupLabelFont.setPointSize(13)
        scoreGroupLabelFont.setBold(True)

        self.time_label.setFont(scoreGroupLabelFont)
        self.time_label.setObjectName("label_2")
        self.time_label.setStyleSheet(style_sheet)
        self.verticalLayout_2.addWidget(self.time_label)

        self.level_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.level_label.setFont(scoreGroupLabelFont)
        self.level_label.setObjectName("label_3")
        self.level_label.setStyleSheet(style_sheet)
        self.verticalLayout_2.addWidget(self.level_label)

        self.score_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.score_label.setFont(scoreGroupLabelFont)
        self.score_label.setObjectName("label_4")
        self.score_label.setStyleSheet(style_sheet)
        self.verticalLayout_2.addWidget(self.score_label)
        self.setCentralWidget(self.centralwidget)

        self.exitButton.setFont(self.font)
        self.exitButton.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.exitButton)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 26))
        self.menubar.setDefaultUp(True)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setEnabled(True)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)


    def set_transparent_image(self, image_path, opacity):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), aspectRatioMode=QtCore.Qt.IgnoreAspectRatio)

        palette = self.palette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)

        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(transparent_pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        label = QtWidgets.QLabel(self)
        label.setPixmap(transparent_pixmap)
        label.setGeometry(50, 50, pixmap.width(), pixmap.height())

    def game_start(self):
        global ItemMode
        self.dodge_game.game_start(var.level_up_time[0], ItemMode)
        score = var.current_score[0]
        level = var.level[0]
        time = var.elapsed_time[0]
        Game.save_score()
        # self.update_best_score(score, level)
        self.add_record(time, level, score)
        self.update_best_score(var.top_score[0], var.max_level[0], var.max_time[0])
        Game.reset_var()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "죽림고수"))
        self.label.setText(_translate("MainWindow", "죽림고수"))
        self.gameStartButton.setText(_translate("MainWindow", "Game Start"))
        self.recordButton.setText(_translate("MainWindow", "Records"))
        self.settingButton.setText(_translate("MainWindow", "Settings"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.time_label.setText(_translate("MainWindow", "Best Time: None"))
        self.level_label.setText(_translate("MainWindow", "Best score: None"))
        self.score_label.setText(_translate("MainWindow", "Best level: None"))

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        background = pixmap.scaled(self.size(), aspectRatioMode=QtCore.Qt.IgnoreAspectRatio)

        palette = self.palette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(background))
        self.setPalette(palette)

    def update_best_score(self, score, level, time):
        if score >= self.best_score:
            self.best_score = score
            self.score_label.setText(f"Best score: {self.best_score}")
        if level >= self.best_level:
            self.best_level = level
            self.level_label.setText(f"Best level: {self.best_level}")
        if time >= self.best_time:
            self.best_time = time
            self.time_label.setText(
                f"Best time: {(self.best_time // 1000) % 60 + ((self.best_time // 1000) // 60) * 60}.{self.best_time % 1000}초")

    def add_record(self, millitime, level, score):
        with open('game_records.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([millitime, level, score])

    def show_game_records(self):
        self.game_record_dialog.load_records()
        self.game_record_dialog.exec_()

    def show_game_setting(self):
        self.game_setting_widget.exec_()

    def create_csv_file(self, filename, headers=None):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)

    def on_closing(self):
        with open('game_records.csv', 'w') as file:
            file.truncate()

    def close(self):
        msgBox = QMessageBox()
        reply = msgBox.question(
            None,
            "Exit",
            "종료 하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            super().close()

    def show_today_date(self):
        self.statusBar().showMessage(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    app.aboutToQuit.connect(ui.on_closing)
    sys.exit(app.exec_())
