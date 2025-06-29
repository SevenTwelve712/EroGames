from typing import Union

from PySide6.QtCore import QPropertyAnimation, QRect, QByteArray, QSize, QEasingCurve, QSequentialAnimationGroup, \
    QObject, QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget, QGraphicsDropShadowEffect, QSizePolicy


class Animations:
    def press_animation(self, obj_geometry: QSize, scale_factor: float, duration: int) -> QSequentialAnimationGroup:
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
        anim_there = QPropertyAnimation(self, QByteArray(b"geometry"))
        anim_there.setStartValue(obj_geometry)
        anim_there.setEndValue(new_geometry)
        anim_there.setDuration(duration)

        # Делаем анимацию обратно
        anim_back = QPropertyAnimation(self, QByteArray(b"geometry"))
        anim_back.setStartValue(new_geometry)
        anim_back.setEndValue(obj_geometry)
        anim_back.setDuration(duration)

        # Группируем
        seq = QSequentialAnimationGroup()
        seq.addAnimation(anim_there)
        seq.addAnimation(anim_back)
        return seq

    def img_opacity_animation(self, duration: int, start_opacity: float, end_opacity: float) -> QPropertyAnimation:
        effect = QGraphicsOpacityEffect(self, opacity=start_opacity)
        self.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, QByteArray(b'opacity'))
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        return animation

    def img_glowing_pulsar_animation(self, duration: int, start_radius: float, end_radius: float) -> QSequentialAnimationGroup:
        effect = FixedShadowEffect(self, blurRadius=start_radius, color=QColor('#FFCF48'))
        effect.setOffset(QPoint(0, 0))
        self.setGraphicsEffect(effect)

        anim_seq_ = QSequentialAnimationGroup()

        animation_there = QPropertyAnimation(effect, QByteArray(b'blurRadius'))
        animation_there.setDuration(duration)
        animation_there.setStartValue(start_radius)
        animation_there.setEndValue(end_radius)

        animation_back = QPropertyAnimation(effect, QByteArray(b'blurRadius'))
        animation_back.setDuration(duration)
        animation_back.setStartValue(end_radius)
        animation_back.setEndValue(start_radius)

        anim_seq_.addAnimation(animation_there)
        anim_seq_.addAnimation(animation_back)
        anim_seq_.setLoopCount(-1)

        return anim_seq_


class FixedShadowEffect(QGraphicsDropShadowEffect):
    def boundingRectFor(self, rect):
        return rect.adjusted(0, 0, 200, 200)
