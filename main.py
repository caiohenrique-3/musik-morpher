import sys
from PyQt6 import QtWidgets, QtCore
import subprocess


class SongProcessor(QtCore.QThread):
    processingFinished = QtCore.pyqtSignal()
    errorOccurred = QtCore.pyqtSignal(str)

    def __init__(self, path, value):
        super().__init__()
        self.path = path
        self.value = value

    def run(self):
        try:
            file_name_without_extension = QtCore.QFileInfo(
                self.path).baseName()
            modification_type = "Nightcore" if self.value > 100 else "Slowed Down"
            new_file_name = f"{file_name_without_extension} - {modification_type}.mp3"
            result = subprocess.run(['ffmpeg', '-i', self.path, '-filter:a',
                                    f"atempo={self.value/100}", new_file_name], capture_output=True, text=True)
            if result.returncode != 0:
                self.errorOccurred.emit(result.stderr)
            else:
                self.processingFinished.emit()
        except Exception as e:
            self.errorOccurred.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Speed Changer")

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)

        self.tempoLabel = QtWidgets.QLabel()
        self.layout.addWidget(self.tempoLabel)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(50, 200)
        self.slider.setValue(100)
        self.slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.update_tempo_label)
        self.layout.addWidget(self.slider)

        self.button = QtWidgets.QPushButton("Select a song")
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

        self.modify_button = QtWidgets.QPushButton("Modify song")
        self.modify_button.clicked.connect(self.modify_button_clicked)
        self.layout.addWidget(self.modify_button)

        self.progress = QtWidgets.QProgressBar()
        self.layout.addWidget(self.progress)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def update_tempo_label(self, value):
        self.tempoLabel.setText(f"Tempo: {value}%")

    def button_clicked(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open a file', '', 'Audio files (*.mp3 *.wav)')[0]
        if self.path:
            self.label.setText(f"Selected song: {self.path}")

    def modify_button_clicked(self):
        value = self.slider.value()
        if hasattr(self, 'path'):
            self.progress.setRange(0, 0)
            self.processor = SongProcessor(self.path, value)
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
