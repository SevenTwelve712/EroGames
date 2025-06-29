from PySide6.QtCore import Property, QPoint, QSequentialAnimationGroup
from PySide6.QtCore import QByteArray, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PySide6.QtGui import QColor, QMouseEvent, QPixmap
from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect, QGraphicsDropShadowEffect

from TicTacToe.view.PressableWidget import PressableWidget


class TicTacWidget(QLabel):
    def __init__(self, coords: tuple[int, int], parent=None):
        super().__init__(parent)

        self.setObjectName('tictac')
        self.coords = coords
        self.filled = False
        self.border_size = 2
        self.border_color_start = QColor('black')
        self.border_color_stop = QColor('#315b6d')

        self.main_wnd = self.window()
        self.game = self.main_wnd.game

    def getBorderColor(self):
        return self.border_color_start

    def setBorderColor(self, color: QColor):
        style = f'border: 2px solid {color.name()}; border-radius: 8px; background-color: #688fa6)'
        self.setStyleSheet(style)

    def do_border_animation(self, duration: int, start_val, end_val, property_name: QByteArray) -> QPropertyAnimation:
        animation = QPropertyAnimation(self, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_val)
        animation.setEndValue(end_val)
        return animation

    def animate_img_opacity(self, duration: int, start_opacity: float, end_opacity: float) -> QPropertyAnimation:
        effect = QGraphicsOpacityEffect(self, opacity=start_opacity)
        self.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, QByteArray(b'opacity'))
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        return animation

    def animate_img_glowing_pulsar(self, duration: int, start_radius: float, end_radius: float) -> QSequentialAnimationGroup:
        effect = QGraphicsDropShadowEffect(self, blurRadius=start_radius, color=QColor('#FFCF48'))
        effect.setOffset(QPoint(0, 0))
        self.setGraphicsEffect(effect)

        anim_seq = QSequentialAnimationGroup()

        animation_there = QPropertyAnimation(effect, QByteArray(b'blurRadius'))
        animation_there.setDuration(duration)
        animation_there.setStartValue(start_radius)
        animation_there.setEndValue(end_radius)

        animation_back = QPropertyAnimation(effect, QByteArray(b'blurRadius'))
        animation_back.setDuration(duration)
        animation_back.setStartValue(end_radius)
        animation_back.setEndValue(start_radius)

        anim_seq.addAnimation(animation_there)
        anim_seq.addAnimation(animation_back)
        anim_seq.setLoopCount(-1)

        return anim_seq

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.filled or self.game.ended:
            event.ignore()
            return
        else:
            self.filled = True
            event.accept()
            player = self.game.current_player

            # Задаем картинку
            img = 'tits.png' if player == 'tits' else 'ass.png'
            self.setPixmap(QPixmap(img))
            self.setScaledContents(True)

            # Делаем анимации
            self.img_animation = self.animate_img_opacity(1000, 0.35, 1.0)
            self.animation_border = self.do_border_animation(500, self.border_color_start, self.border_color_stop,
                                                             QByteArray(b'color'))

            # Объединяем анимации
            self.animation_group = QParallelAnimationGroup(self)
            self.animation_group.addAnimation(self.img_animation)
            self.animation_group.addAnimation(self.animation_border)
            self.animation_group.start()

            self.animation_group.finished.connect(lambda: self.do_border_animation(500, self.border_color_stop,
                                                                                   self.border_color_start,
                                                                                   QByteArray(b'color')))

            # Обновляем игровую логику. По идее, это нужно делать в начале,
            # но тогда анимация финиша будет играть до анимации самой ячейки, и произойдет накладка
            res = self.game.step(self.coords)
            if res:
                win_positions = self.game.get_win_positions()
                self.main_wnd.finish(res, win_positions)
            else:
                step_counter = self.main_wnd.step_counter
                step_counter.setText(f'Ход игрока {self.game.current_player}')

    def clear(self, /) -> None:
        self.setPixmap(QPixmap())
        self.filled = False
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        effect.setOpacity(1.0)

    borderColor = Property(QColor, getBorderColor, setBorderColor)
