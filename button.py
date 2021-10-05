from PyQt5.QtCore import QMimeDatabase
from PyQt5.QtWidgets import QPushButton, QFileDialog


# Custom button class which accepts drag and drop events and clicks
class Button(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.filename = None
        self.clicked.connect(self.get_file)

    def dragEnterEvent(self, e):
        paths = e.mimeData().urls()
        if len(paths) == 1 and QMimeDatabase().mimeTypeForUrl(paths[0]).name() == 'application/pdf':
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.filename = e.mimeData().urls()[0].toLocalFile()

    # Opens a QFileDialog and stores the user-selected filename
    def get_file(self):
        self.filename = QFileDialog.getOpenFileName(self, filter='*.pdf')[0]
