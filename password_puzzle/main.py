import os
import sys

from PyQt6.QtCore import QPoint, Qt, QTimer, QUrl
from PyQt6.QtGui import QKeyEvent, QFont
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QSlider,
    QVBoxLayout,
    QWidget,
)

PASSWORD = os.getenv("PUZZLE_CODE")


class PasswordInput(QMainWindow):
    def __init__(self):
        super().__init__()

        self.password_input = ""
        self.input_allowed = True

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.cx, self.cy = qr.center().x(), qr.center().y()

        self.label = QLabel("Enter Password:", self)
        f = self.label.font()
        f.setPointSize(30)
        self.label.setFont(f)
        self.label.adjustSize()
        self.label.move(self.cx - self.label.width()//2, self.cy - 75)

        self.password_display = QLabel("- - - - - - -", self)
        f = QFont("Monospace", 30)
        self.password_display.setFont(f)
        self.password_display.adjustSize()
        self.password_display.move(self.cx - self.password_display.width()//2, self.cy)

        self.error = QLabel("", self)
        self.error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = self.error.font()
        f.setPointSize(25)
        self.error.setFont(f)
        self.error.adjustSize()
        self.error.move(self.cx, self.cy + 75)
        self.error.setStyleSheet("color: red")
        self.error.setVisible(False)

        self.video_player = VideoPlayer(self)

    def submit_text(self):
        if self.password_input.lower() == PASSWORD:
            self.video_player.start_video()
        else:
            self.start_error_timer()

    def set_input_allowed(self, input_allowed: bool):
        self.input_allowed = input_allowed
        self.password_display.setStyleSheet(f"color: {"black" if input_allowed else "grey"}")

    def start_error_timer(self):
        self.set_input_allowed(False)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.iterator = 10
        self.timer.timeout.connect(self.update_error)
        self.error.setVisible(True)
        self.update_error()
        self.timer.start()

    def update_error(self):
        if self.iterator == 0:
            self.timer.stop()
            self.clear_password_input()
            self.set_input_allowed(True)
            self.error.setText("")
            self.error.setVisible(False)
        else:
            self.error.setText(f"Password incorrect; please wait {self.iterator} second(s)")
            self.error.adjustSize()
            self.error.width()
            self.error.move(self.cx - self.error.width()//2, self.cy + 75)
            self.iterator -= 1

    def add_character(self, char: str):
        self.password_input = self.password_input + char
        self.update_password_display()
        if len(self.password_input) == 7:
            self.submit_text()

    def remove_last_character(self):
        self.password_input = self.password_input[:-1]
        self.update_password_display()

    def clear_password_input(self):
        self.password_input = ""
        self.update_password_display()

    def update_password_display(self):
        padded_password = ("{:-<7}".format(self.password_input))
        self.password_display.setText(" ".join(padded_password))
        self.password_display.adjustSize()
        self.password_display.move(self.cx - self.password_display.width()//2, self.cy)

    def keyReleaseEvent(self, event: QKeyEvent):
        print(event.key())
        if self.input_allowed:
            if event.key() >= 65 and event.key() <= 90:
                self.add_character(event.text())
            if event.key() == Qt.Key.Key_Backspace and self.password_input:
                self.remove_last_character()


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
