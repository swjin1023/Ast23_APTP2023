from UI_new import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    app.aboutToQuit.connect(ui.on_closing)
    sys.exit(app.exec_())
