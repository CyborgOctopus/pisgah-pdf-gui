import sys
import PyQt5
#from PyQt5.QtGui import
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog
from app import App


def main():
    app = QApplication([])
    pisgah_app = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
