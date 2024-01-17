import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget


class PasswordInput(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 200)

        self.text_input = QLineEdit(self)
        # self.text_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_input.move(20, 20)
        self.text_input.resize(200, 32)

        self.submit = QPushButton("Submit", self)
        self.submit.move(20, 60)
        self.submit.clicked.connect(self.submit_text)

        self.error = QLabel("", self)
        self.error.move(20, 100)
        self.error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error.adjustSize()
        self.error.setVisible(False)

        self.video_player = VideoPlayer(self)

    def submit_text(self):
        text = self.text_input.text()
        print(f"User entered: {text}")
        if text.lower() == "qwerty":
            self.video_player.start_video()
        else:
            self.start_error_timer()

    def disable_input(self):
        self.text_input.setDisabled(True)
        self.submit.setDisabled(True)

    def start_error_timer(self):
        self.disable_input()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.iterator = 10
        self.timer.timeout.connect(self.update_error)
        self.error.setVisible(True)
        self.update_error()
        self.timer.start()

    def enable_input(self):
        self.text_input.setDisabled(False)
        self.submit.setDisabled(False)

    def update_error(self):
        if self.iterator == 0:
            self.timer.stop()
            self.text_input.setText("")
            self.enable_input()
            self.error.setText("")
            self.error.setVisible(False)
        else:
            self.error.setText(f"Password incorrect; please wait {self.iterator} second(s)")
            self.error.adjustSize()
            self.iterator -= 1


class VideoPlayer(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1024, 768)

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()

        # self.start_button = QPushButton("Start")
        # self.start_button.clicked.connect(self.start_video)

        # self.pause_button = QPushButton("Pause")
        # self.pause_button.clicked.connect(self.pause_video)

        # self.stop_button = QPushButton("Stop")
        # self.stop_button.clicked.connect(self.stop_video)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile("cat-noises.mp4"))
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        # layout.addWidget(self.start_button)
        # layout.addWidget(self.pause_button)
        # layout.addWidget(self.stop_button)
        layout.addWidget(self.slider)

        self.container = QWidget()
        self.container.setLayout(layout)

    def start_video(self):
        self.parentWidget().setCentralWidget(self.container)
        self.media_player.play()

    # def pause_video(self):
    #     self.media_player.pause()

    # def stop_video(self):
    #     self.media_player.stop()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordInput()
    window.showFullScreen()
    sys.exit(app.exec())
