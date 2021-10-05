import PyQt5.QtWidgets as qtw
import pisgah_pdf
from button import Button


# The main class for the Pisgah PDF GUI program
class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.output_filename = 'comparison'
        self.init_ui()

    # Initializes the program user interface. Inspiration from here: https://zetcode.com/gui/pyqt5/
    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Pisgah PDF File Comparison')
        self.setFixedSize(750, 650)

        # Create UI elements
        self.create_buttons()
        self.create_textbox()
        self.create_submit_button()

        # Display
        self.show()

    # Create buttons
    def create_buttons(self):
        button1 = Button('Drag and drop first file or click to select', self)
        button1.setGeometry(50, 50, 300, 300)
        button1.setObjectName('button1')
        button2 = Button('Drag and drop second file or click to select', self)
        button2.setGeometry(400, 50, 300, 300)
        button2.setObjectName('button2')

    # Create textbox to enter output filename
    def create_textbox(self):
        textbox = qtw.QLineEdit(self)
        textbox.setGeometry(50, 400, 650, 40)
        textbox.setPlaceholderText('Enter name of output file (default: \'comparison\')')
        textbox.setObjectName('textbox')

    # Create submission button
    def create_submit_button(self):
        submit = qtw.QPushButton('Submit', self)
        submit.setGeometry(50, 500, 650, 100)
        submit.setObjectName('submit')
        submit.clicked.connect(self.generate_outfile)

    # Runs the output file generator in 'pisgah_pdf.py'
    def generate_outfile(self):
        input_filename_1 = self.findChild(Button, 'button1').filename
        input_filename_2 = self.findChild(Button, 'button2').filename
        output_filename = self.findChild(qtw.QLineEdit, 'textbox').text()
        if output_filename:
            self.output_filename = output_filename
        pisgah_pdf.main(input_filename_1, input_filename_2, self.output_filename)
