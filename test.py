from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QRadioButton, QCheckBox, QToolButton, QCommandLinkButton, QSpinBox, QSlider, QScrollBar, QComboBox, QAction
import sys

class ButtonExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # QPushButton 예시
        pushButton = QPushButton("Push Button")
        pushButton.clicked.connect(self.pushButtonClicked)
        layout.addWidget(pushButton)

        # QRadioButton 예시
        radioButton = QRadioButton("Radio Button")
        radioButton.toggled.connect(self.radioButtonToggled)
        layout.addWidget(radioButton)

        # QCheckBox 예시
        checkBox = QCheckBox("Check Box")
        checkBox.stateChanged.connect(self.checkBoxStateChanged)
        layout.addWidget(checkBox)

        # QToolButton 예시
        toolButton = QToolButton()
        toolButton.setText("Tool Button")
        toolButton.clicked.connect(self.toolButtonClicked)
        layout.addWidget(toolButton)

        # QCommandLinkButton 예시
        commandLinkButton = QCommandLinkButton("Command Link Button", "Detailed description")
        commandLinkButton.clicked.connect(self.commandLinkButtonClicked)
        layout.addWidget(commandLinkButton)

        # QSpinBox 예시
        spinBox = QSpinBox()
        spinBox.valueChanged.connect(self.spinBoxValueChanged)
        layout.addWidget(spinBox)

        # QSlider 예시
        slider = QSlider()
        slider.valueChanged.connect(self.sliderValueChanged)
        layout.addWidget(slider)

        # QScrollBar 예시
        scrollBar = QScrollBar()
        scrollBar.valueChanged.connect(self.scrollBarValueChanged)
        layout.addWidget(scrollBar)

        # QComboBox 예시
        comboBox = QComboBox()
        comboBox.addItem("Item 1")
        comboBox.addItem("Item 2")
        comboBox.currentIndexChanged.connect(self.comboBoxIndexChanged)
        layout.addWidget(comboBox)

        # QAction 예시
        action = QAction("Action Button", self)
        action.triggered.connect(self.actionButtonTriggered)
        self.addAction(action)

        self.setLayout(layout)

    def pushButtonClicked(self):
        print("Push Button Clicked")

    def radioButtonToggled(self, checked):
        print("Radio Button Toggled:", checked)

    def checkBoxStateChanged(self, state):
        print("Check Box State Changed:", state)

    def toolButtonClicked(self):
        print("Tool Button Clicked")

    def commandLinkButtonClicked(self):
        print("Command Link Button Clicked")

    def spinBoxValueChanged(self, value):
        print("Spin Box Value Changed:", value)

    def sliderValueChanged(self, value):
        print("Slider Value Changed:", value)

    def scrollBarValueChanged(self, value):
        print("Scroll Bar Value Changed:", value)

    def comboBoxIndexChanged(self, index):
        print("Combo Box Index Changed:", index)

    def actionButtonTriggered(self):
        print("Action Button Triggered")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = ButtonExample()
    example.show()
    sys.exit(app.exec_())
