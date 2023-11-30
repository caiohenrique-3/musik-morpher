from PyQt6 import QtWidgets, QtCore, QtGui
import subprocess
import os
import sys


class SongProcessor(QtCore.QThread):
    processingFinished = QtCore.pyqtSignal()
    errorOccurred = QtCore.pyqtSignal(str)

    def __init__(self, path, value, pitch):
        super().__init__()
        self.path = path
        self.value = value
        self.pitch = pitch

    def run(self):
        try:
            file_name_without_extension = QtCore.QFileInfo(
                self.path).baseName()
            modification_type = "Nightcore" if self.pitch != 1.0 else "Slowed Down"
            new_file_name = f"{file_name_without_extension} - {modification_type}.mp3"

            # Check if the new file already exists, and append a number to make it unique
            counter = 1
            while os.path.exists(new_file_name):
                new_file_name = f"{file_name_without_extension} - {modification_type}_{counter}.mp3"
                counter += 1

            filters = []
            filters.append(f"asetrate=44100*{self.pitch}")
            filters.append(f"atempo={self.value/100}")

            result = subprocess.run(
                ['ffmpeg', '-i', self.path, '-filter:a',
                    ','.join(filters), new_file_name],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                self.errorOccurred.emit(result.stderr)
            else:
                self.processingFinished.emit()

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            self.errorOccurred.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MusikMorpher")
        self.setStyleSheet("""
            QWidget {
                background-color: #2C2C2C;
                color: #FFFFFF;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                padding: 15px 32px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #CD5C5C;
                width: 20px;
            }
        """)

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.add_widget_to_layout(self.label)

        self.descLabel1 = QtWidgets.QLabel()
        self.descLabel1.setText("SONG SPEED")
        self.descLabel1.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.add_widget_to_layout(self.descLabel1)

        self.tempoLabel = QtWidgets.QLabel()
        self.tempoLabel.setText("Normal (unchanged)")
        self.add_widget_to_layout(self.tempoLabel)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(50, 200)
        self.slider.setValue(100)
        self.slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.update_tempo_label)
        self.add_widget_to_layout(self.slider)

        self.pitch_label = QtWidgets.QLabel("SONG PITCH:")
        self.pitch_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.add_widget_to_layout(self.pitch_label)

        self.pitch_combobox = QtWidgets.QComboBox()
        self.pitch_combobox.addItem("Normal (unchanged)", 1.0)
        self.pitch_combobox.addItem("1.25", 1.25)
        self.pitch_combobox.addItem("1.5", 1.5)
        self.pitch_combobox.addItem("1.75", 1.75)
        self.pitch_combobox.addItem("2.0", 2.0)
        self.add_widget_to_layout(self.pitch_combobox)

        self.button = QtWidgets.QPushButton("Select a song")
        self.button.clicked.connect(self.button_clicked)
        self.add_widget_to_layout(self.button)

        self.modify_button = QtWidgets.QPushButton("Modify song")
        self.modify_button.clicked.connect(self.modify_button_clicked)
        self.add_widget_to_layout(self.modify_button)

        self.progress = QtWidgets.QProgressBar()
        self.add_widget_to_layout(self.progress)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def add_widget_to_layout(self, widget):
        """Add a widget to the main layout with horizontal center alignment."""
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(widget)
        h_layout.addStretch()
        self.layout.addLayout(h_layout)

    def update_tempo_label(self, value):
        if value == 0:
            label_text = "Normal (unchanged)"
        else:
            percentage_change = value - 100
            label_text = f"Song Speed: {'+' if percentage_change > 0 else ''}{percentage_change}%"
        self.tempoLabel.setText(label_text)

    def button_clicked(self):
        default_folder = os.path.expanduser("~/Music")

        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open a file', default_folder, 'Audio files (*.mp3 *.wav)'
        )

        if self.path:
            self.label.setText(f"Selected song: {self.path}")

    def modify_button_clicked(self):
        value = self.slider.value()
        pitch = self.pitch_combobox.currentData()
        if hasattr(self, 'path'):
            self.progress.setRange(0, 0)
            self.processor = SongProcessor(self.path, value, pitch)
            self.processor.processingFinished.connect(
                self.on_processing_finished)
            self.processor.errorOccurred.connect(self.on_error_occurred)
            self.processor.start()

    @QtCore.pyqtSlot()
    def on_processing_finished(self):
        self.progress.setRange(0, 1)
        self.progress.setValue(1)

    @QtCore.pyqtSlot(str)
    def on_error_occurred(self, error_message):
        QtWidgets.QMessageBox.critical(self, "Error", error_message)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
