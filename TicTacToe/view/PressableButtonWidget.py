from PySide6.QtCore import QSize
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QPushButton

from TicTacToe.view.Animations import Animations


class PressableButtonWidget(Animations, QPushButton):
    def __init__(self, text: str, parent=None):
        self.old_geometry = None
        self.mouse_released = False
        self.press_animation_played = False
        super().__init__(text, parent=parent)

    def resize(self, arg__1: QSize, /) -> None:
        super().resize(arg__1)
        self.old_geometry = self.geometry()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.mouse_released = True
        if self.press_animation_played:
            self.do_press_animation_back(self.geometry(), self.old_geometry, 100)
            self.press_animation_back.start()
            self.press_animation_played = False

        super().mouseReleaseEvent(event)

    def mousePressEvent(self, e: QMouseEvent, /) -> None:
        self.mouse_released = False
        self.do_press_animation_there(self.old_geometry, 0.92, 100)
        self.press_animation_there.finished.connect(self.release_animation_controller)
        self.press_animation_there.start()
        super().mousePressEvent(e)

    def release_animation_controller(self):
        if self.mouse_released:
            self.do_press_animation_back(self.geometry(), self.old_geometry, 100)
            self.press_animation_back.start()
        else:
            self.press_animation_played = True
