import sys
import mainwindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = mainwindow.MainWindow()
    ui.show()
    sys.exit(app.exec_())
