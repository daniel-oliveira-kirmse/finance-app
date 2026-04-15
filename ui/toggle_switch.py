from PySide6.QtWidgets import QAbstractButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QPixmap


class ToggleSwitch(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)

        self._circle_position = 3

        self._animation = QPropertyAnimation(self, b"circle_position", self)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._animation.setDuration(250)

        self.setFixedSize(90, 40)

        self.icon_sun = None
        self.icon_moon = None

    def set_icons(self, sun_path: str, moon_path: str):
        self.icon_sun = QPixmap(sun_path)
        self.icon_moon = QPixmap(moon_path)

    def circle_position_getter(self):
        return self._circle_position

    def circle_position_setter(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = Property(int, circle_position_getter, circle_position_setter)

    def start_animation(self):
        if self.isChecked():
            end_pos = self.width() - 35
        else:
            end_pos = 3

        self._animation.stop()
        self._animation.setStartValue(self._circle_position)
        self._animation.setEndValue(end_pos)
        self._animation.start()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())
            self.start_animation()
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isChecked():
            bg_color = QColor("#2c3e50")
        else:
            bg_color = QColor("#dcdde1")

        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)

        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(self._circle_position, 4, 32, 32)

        icon = self.icon_moon if self.isChecked() else self.icon_sun

        if icon:
            scaled = icon.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(self._circle_position + 7, 11, scaled)

        painter.end()