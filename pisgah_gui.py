import os
from PyQt5.QtCore import QSettings, Qt
import PyQt5.QtWidgets as qtw
from pisgah_pdf import file_comparison
from file_selection_button import FileSelectionButton
from output_file_exists_dialog import OutputFileExistsDialog


# The main class for the Pisgah PDF GUI program
class PisgahGui(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.input_file_path_lexis = ''
        self.input_file_path_ciprs = ''
        self.output_file_dir = ''
        self.output_file_path = ''
        self.default_output_file_name = 'comparison'
        self.default_output_file_path = ''
        self.load_settings()
        self.output_file_display = qtw.QTextEdit()
        self.output_file_display.resize(1000, 500)
        self.dynamic_font = self.font()
        self.init_ui()

    # Initializes the program user interface. Inspiration from here: https://zetcode.com/gui/pyqt5/
    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Pisgah PDF File Comparison')
        self.setMinimumSize(750, 650)
        #self.setBaseSize(750, 650)

        # Create UI elements
        self.create_save_directory_config()
        self.create_file_selection_buttons()
        self.create_textbox()
        self.create_submit_button()

        # Display
        self.show()

    # Create save directory configuration informational text and button
    def create_save_directory_config(self):
        config_label = qtw.QLabel('Files will be saved in ' + os.path.abspath(self.output_file_dir), self)
        config_label.setAlignment(Qt.AlignCenter)
        config_label.setObjectName('config label')

        config_button = qtw.QPushButton('Choose where to save output files', self)
        config_button.setObjectName('config button')
        config_button.clicked.connect(self.update_settings)

    # Create buttons
    def create_file_selection_buttons(self):
        button1 = FileSelectionButton('Drag and drop LEXIS file or click to select', self)
        button1.setObjectName('button1')
        button1.file_selected.connect(self.on_selection)

        button2 = FileSelectionButton('Drag and drop CIPRS file or click to select', self)
        button2.setObjectName('button2')
        button2.file_selected.connect(self.on_selection)

    # Create textbox to enter output file_path
    def create_textbox(self):
        textbox = qtw.QLineEdit(self)
        textbox.setPlaceholderText('Enter name/path of output file. (default: \'comparison\')')
        textbox.setObjectName('textbox')

    # Create submission button
    def create_submit_button(self):
        submit = qtw.QPushButton('Submit', self)
        submit.setObjectName('submit')
        submit.setEnabled(False)
        submit.clicked.connect(self.on_submit)

    # Dynamically adjusts the size of all window elements as the window is resized
    def resizeEvent(self, event):
        self.resize_font()
        self.resize_save_directory_config()
        self.resize_file_selection_buttons()
        self.resize_textbox()
        self.resize_submit_button()

    # Resizes the config button based on the current size of the window and other elements
    def resize_save_directory_config(self):
        config_label = self.findChild(qtw.QLabel, 'config label')
        config_label.setGeometry(50, 10, self.width() - 100, self.height() * 30 / 650)
        config_label.setFont(self.dynamic_font)

        config_button = self.findChild(qtw.QPushButton, 'config button')
        top_height = config_label.y() + config_label.height() + 10
        config_button.setGeometry(100, top_height, self.width() - 200, self.height() * 30 / 650)
        config_button.setFont(self.dynamic_font)

    # Resize buttons based on the current size of the window
    def resize_file_selection_buttons(self):
        config_button = self.findChild(qtw.QPushButton, 'config button')

        button1 = self.findChild(FileSelectionButton, 'button1')
        top_height = config_button.y() + config_button.height() + 30
        button1.setGeometry(50, top_height, (self.width() - 150) / 2, self.height() * 300 / 650)
        button1.setFont(self.dynamic_font)
        button2 = self.findChild(FileSelectionButton, 'button2')
        button2.setGeometry(100 + button1.width(), top_height, button1.width(), button1.height())
        button2.setFont(self.dynamic_font)

    # Resize textbox based on the current size of the window and other elements
    def resize_textbox(self):
        button1 = self.findChild(FileSelectionButton, 'button1')
        top_height = button1.y() + button1.height() + 50
        self.findChild(qtw.QLineEdit, 'textbox').setGeometry(50, top_height, self.width() - 100, 40)

    # Resizes the submit button based on the current size of the window and other elements
    def resize_submit_button(self):
        textbox = self.findChild(qtw.QLineEdit, 'textbox')
        top_height = textbox.y() + textbox.height() + 50
        submit = self.findChild(qtw.QPushButton, 'submit')
        submit.setGeometry(50, top_height, self.width() - 100, self.height() - top_height - 50)
        submit.setFont(self.dynamic_font)

    # Resizes font for all elements that use dynamic font
    def resize_font(self):
        self.dynamic_font.setPointSizeF(5 + self.width() * 2.5 / 750)

    def on_selection(self):
        self.input_file_path_lexis = self.findChild(FileSelectionButton, 'button1').file_path
        self.input_file_path_ciprs = self.findChild(FileSelectionButton, 'button2').file_path
        if self.input_file_path_lexis and self.input_file_path_ciprs:
            self.findChild(qtw.QPushButton, 'submit').setEnabled(True)

    # Attempts to generate the outfile, prompting the user if errors occur
    def on_submit(self):
        if self.get_output_file_name():
            error_message = qtw.QMessageBox()
            error_message.setWindowTitle('Oh no!')

            # If the outfile generation fails, it's probably because of an invalid filename
            try:
                # If the filename is a path, disallow it
                if os.path.split(self.output_file_path)[0] != self.output_file_dir:
                    error_message.setText('Filename should not be a path')
                else:
                    self.generate_outfile()
                    return
            except OSError:
                error_message.setText('Output file generation failed! This may be due to an illegal filename. Make sure'
                                      ' you enter a valid name for your output file.')
            error_message.exec()

    # Gets the output filename, either from default or the user, and checks whether a file with that name already
    # exists. If so, prompts the user to rename or replace the file, and continues to do so until an existing file is
    # replaced or a not-existing name is chosen. Returns a boolean of whether or not the filename selection was
    # successful or cancelled by the user
    def get_output_file_name(self):
        success = True

        output_file_name = self.findChild(qtw.QLineEdit, 'textbox').text()

        # Check if an output filename has been provided
        if output_file_name:
            self.output_file_path = os.path.join(self.output_file_dir, output_file_name)
        else:
            self.output_file_path = self.default_output_file_path

        while os.path.exists(self.output_file_path + '.txt'):
            dialog = OutputFileExistsDialog(self)
            result = dialog.exec()
            if result == 0:
                success = False
                break
            elif result == 1:
                break
            elif result == 2:
                self.output_file_path = dialog.path

        return success

    # Runs the output file generator in 'pisgah_pdf.py'
    def generate_outfile(self):
        if os.path.exists(self.input_file_path_lexis) and os.path.exists(self.input_file_path_ciprs):
            file_comparison(self.input_file_path_lexis, self.input_file_path_ciprs, self.output_file_path + '.txt')
            comparison_text = open(self.output_file_path + '.txt').read()
            self.output_file_display.setWindowTitle(os.path.split(self.output_file_path)[1])
            self.output_file_display.setPlainText(comparison_text)
            self.output_file_display.show()

    # Reads settings from the settings object
    def load_settings(self):
        self.output_file_dir = str(QSettings('CyborgOctopus', 'Pisgah Legal Services PDF GUI').value('dir'))
        self.default_output_file_path = os.path.join(self.output_file_dir, self.default_output_file_name)

    # Creates and saves default save directory settings, then sets them as the default
    def update_settings(self):
        dir_selector = qtw.QFileDialog(self)
        directory = dir_selector.getExistingDirectory(self)

        if directory:
            settings = QSettings('CyborgOctopus', 'Pisgah Legal Services PDF GUI')
            settings.setValue('dir', directory)

            self.load_settings()
            self.set_save_directory_label()

    # Sets the label for the save directory to reflect the current output file directory
    def set_save_directory_label(self):
        label = self.findChild(qtw.QLabel, 'config label')
        label.setText('Files will be saved in ' + os.path.abspath(self.output_file_dir))
