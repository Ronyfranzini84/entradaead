from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ui_main import Ui_EntradaEAD
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_EntradaEAD()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/icons/Imagem1.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())