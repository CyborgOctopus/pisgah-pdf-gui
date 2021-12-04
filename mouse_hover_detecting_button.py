from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtWidgets import QPushButton


class MouseHoverDetectingButton(QPushButton):
    mouse_entered = pyqtSignal()
    mouse_exited = pyqtSignal()

    def __init__(self, default_text, parent=None):
        super().__init__(default_text, parent)

    def enterEvent(self, a0: QEvent):
        self.mouse_entered.emit()

    def leaveEvent(self, a0: QEvent):
        self.mouse_exited.emit()
