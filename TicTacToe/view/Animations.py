from typing import Union

from PySide6.QtCore import QPropertyAnimation, QRect, QByteArray, QSize, QEasingCurve, QSequentialAnimationGroup, \
    QObject, QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget, QGraphicsDropShadowEffect, QSizePolicy


class Animations:
    def do_press_animation_there(self, obj_geometry: QRect, scale_factor: float, duration: int) -> None:
        # Рассчитываем новый размер виджета
        center = obj_geometry.center()
        new_width = int(obj_geometry.width() * scale_factor)
        new_height = int(obj_geometry.height() * scale_factor)
        new_geometry = QRect(
            center.x() - new_width // 2,
            center.y() - new_height // 2,
            new_width,
            new_height
        )

        # Делаем анимацию туда
        self.press_animation_there = QPropertyAnimation(self, QByteArray(b"geometry"))
        self.press_animation_there.setStartValue(obj_geometry)
        self.press_animation_there.setEndValue(new_geometry)
        self.press_animation_there.setDuration(duration)
        self.press_animation_there.setEasingCurve(QEasingCurve.InQuad)

    def do_press_animation_back(self, obj_geometry: QRect, old_geometry: QRect, duration: int) -> None:
        # Старый размер нужен, чтобы все размер возвращался в норму, если заново его считать, будут мини погрешности,
        # которые изменят размер виджета.
        # Делаем анимацию обратно
        self.press_animation_back = QPropertyAnimation(self, QByteArray(b"geometry"))
        self.press_animation_back.setStartValue(obj_geometry)
        self.press_animation_back.setEndValue(old_geometry)
        self.press_animation_back.setDuration(duration)
        self.press_animation_back.setEasingCurve(QEasingCurve.OutQuad)

    def do_img_opacity_animation(self, duration: int, start_opacity: float, end_opacity: float) -> None:
        # Делаем эффект
        opacity_effect = QGraphicsOpacityEffect(self, opacity=0.35)
        self.setGraphicsEffect(opacity_effect)

        self.img_opacity_animation = QPropertyAnimation(opacity_effect, QByteArray(b'opacity'))
        self.img_opacity_animation.setDuration(duration)
        self.img_opacity_animation.setStartValue(start_opacity)
        self.img_opacity_animation.setEndValue(end_opacity)

    def do_img_glowing_pulsar_animation(self, duration: int, start_radius: float, end_radius: float) -> None:
        effect = QGraphicsDropShadowEffect(self, blurRadius=start_radius, color=QColor('#FFCF48'))
        effect.setOffset(QPoint(0, 0))
        self.setGraphicsEffect(effect)

        self.img_glowing_pulsar_animation = QSequentialAnimationGroup(self)

        animation_there = QPropertyAnimation(effect, QByteArray(b'blurRadius'))
        animation_there.setDuration(duration)
        animation_there.setStartValue(start_radius)
        animation_there.setEndValue(end_radius)

        animation_back = QPropertyAnimation(effect, QByteArray(b'blurRadius'))
        animation_back.setDuration(duration)
        animation_back.setStartValue(end_radius)
        animation_back.setEndValue(start_radius)

        self.img_glowing_pulsar_animation.addAnimation(animation_there)
        self.img_glowing_pulsar_animation.addAnimation(animation_back)
        self.img_glowing_pulsar_animation.setLoopCount(-1)
