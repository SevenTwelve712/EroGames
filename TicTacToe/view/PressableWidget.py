from typing import Union

from PySide6.QtCore import QPropertyAnimation, QRect, QByteArray, QSize, QEasingCurve


class PressableWidget:
    def press_animation_there(self, obj_geometry: Union[QRect, QSize], scale_factor: float, duration: int):
        center = obj_geometry.center()
        new_width = int(obj_geometry.width() * scale_factor)
        new_height = int(obj_geometry.height() * scale_factor)
        new_geometry = QRect(
            center.x() - new_width // 2,
            center.y() - new_height // 2,
            new_width,
            new_height
        )
        anim = QPropertyAnimation(self, QByteArray(b"geometry"))
        anim.setStartValue(obj_geometry)
        anim.setEndValue(new_geometry)
        anim.setDuration(duration)
        return anim

    def press_animation_back(self):
        pass

