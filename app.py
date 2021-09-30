from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QFileDialog
import pisgah_pdf


# The main class for the Pisgah PDF GUI program
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.input_filenames = [''] * 2
        self.output_filename = 'comparison'
        self.init_ui()

    # Initializes the program user interface. Inspiration from here: https://zetcode.com/gui/pyqt5/
    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Pisgah PDF File Comparison')

        # Create buttons
        button_1 = QPushButton('Drag and drop first file or click to select')
        button_1.setFixedSize(300, 300)
        button_1.setAcceptDrops(True)
        button_1.clicked.connect(lambda: self.get_file(0))
        button_2 = QPushButton('Drag and drop second file or click to select')
        button_2.setFixedSize(300, 300)
        button_2.setAcceptDrops(True)
        button_2.clicked.connect(lambda: self.get_file(1))

        # Create horizontal layout to store buttons
        hbox = QHBoxLayout()
        hbox.addSpacing(50)
        hbox.addWidget(button_1)
        hbox.addSpacing(50)
        hbox.addWidget(button_2)
        hbox.addSpacing(50)

        # Create textbox to enter output filename
        textbox = QLineEdit()
        #textbox.setGeometry(100, 100, 300, 20)
        textbox.setPlaceholderText('Enter name of output file (default: \'comparison\')')

        # Create submission button
        submit = QPushButton('Submit')
        submit.clicked.connect(self.generate_outfile)

        # Create vertical layout to hold all elements
        vbox = QVBoxLayout()
        vbox.addSpacing(50)
        vbox.addLayout(hbox)
        vbox.addSpacing(50)
        vbox.addWidget(textbox)
        vbox.addSpacing(50)
        vbox.addWidget(submit)
        vbox.addSpacing(50)

        self.setLayout(vbox)
        self.show()

    # Opens a QFileDialog and stores the user-selected filename in the filenames list at the specified index
    def get_file(self, index):
        self.input_filenames[index] = QFileDialog.getOpenFileName(self, filter='*.pdf')[0]
        print(self.input_filenames)

    # Runs the output file generator in 'pisgah_pdf.py'
    def generate_outfile(self):
        pisgah_pdf.main(*self.input_filenames, self.output_filename)
