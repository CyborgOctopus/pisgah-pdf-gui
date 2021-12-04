import os
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from mouse_hover_detecting_button import MouseHoverDetectingButton


# Class for a dialog prompting the user on what to do if a specified output file already exists
class OutputFileExistsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.output_file_dir = parent.output_file_dir
        self.path = parent.output_file_path
        self.get_path()
        self.setWindowModality(2)
        self.setLayout(QVBoxLayout())
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Oh no!')

        # Create UI elements
        self.create_label()
        self.create_replace()
        self.create_rename()
        self.create_cancel()

    def create_label(self):
        label = QLabel()
        label.setText('The specified output file already exists. Would you like to replace it or rename your new '
                      'output file?')
        label.adjustSize()
        self.layout().addWidget(label)

    def create_replace(self):
        replace_button = MouseHoverDetectingButton('Replace')
        replace_button.clicked.connect(lambda: self.done(1))
        replace_button.mouse_entered.connect(self.on_replace_mouse_entry)
        replace_button.mouse_exited.connect(self.on_replace_mouse_exit)
        self.layout().addWidget(replace_button)

    def create_rename(self):
        rename_label = QLabel()
        rename_label.setText('Rename to:')
        rename_label.adjustSize()
        rename_label.setObjectName('rename label')

        rename_textbox = QLineEdit()
        rename_textbox.setPlaceholderText(os.path.basename(self.path))
        rename_textbox.setObjectName('rename textbox')

        rename_button = QPushButton('Rename')
        rename_button.clicked.connect(self.on_rename_clicked)
        rename_button.setObjectName('rename button')

        self.layout().addWidget(rename_label)
        self.layout().addWidget(rename_textbox)
        self.layout().addWidget(rename_button)

    def create_cancel(self):
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(lambda: self.done(0))
        self.layout().addWidget(cancel_button)

    #def resizeEvent(self, event):
     #   self.resize_textbox()
        #self.resize_buttons()

    def resize_textbox(self):
        textbox = self.findChild(QLineEdit, 'textbox')
        #textbox.setGeometry(10, 10, 100, 100)

    def on_replace_mouse_entry(self):
        self.findChild(QLabel, 'rename label').setEnabled(False)
        self.findChild(QLineEdit, 'rename textbox').setEnabled(False)
        self.findChild(QPushButton, 'rename button').setEnabled(False)

    def on_replace_mouse_exit(self):
        self.findChild(QLabel, 'rename label').setEnabled(True)
        self.findChild(QLineEdit, 'rename textbox').setEnabled(True)
        self.findChild(QPushButton, 'rename button').setEnabled(True)

    def on_rename_clicked(self):
        self.get_path_from_user_input()
        self.done(2)

    def get_path_from_user_input(self):
        file_name = self.findChild(QLineEdit, 'rename textbox').text()
        if file_name:
            self.path = os.path.join(self.output_file_dir, file_name)

    def get_path(self):
        i = 1
        while True:
            path = self.path + ' (' + str(i) + ')'
            if not os.path.exists(path + '.txt'):
                self.path = path
                return
            i += 1
