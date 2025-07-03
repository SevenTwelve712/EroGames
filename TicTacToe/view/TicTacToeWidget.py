from PySide6.QtCore import Property, QPoint, QSequentialAnimationGroup, QEvent, QSize, QRect
from PySide6.QtCore import QByteArray, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PySide6.QtGui import QColor, QMouseEvent, QPixmap
from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QWidget

from TicTacToe.view.Animations import Animations


class TicTacWidget(QLabel, Animations):
    def __init__(self, coords: tuple[int, int], parent=None):
        super().__init__(parent)

        self.setObjectName('tictac')
        self.coords = coords
        self.filled = False
        self.mouse_released = False
        self.press_animation_played = False
        self.border_size = 2
        self.border_color_start = QColor('black')
        self.border_color_stop = QColor('#315b6d')
        self.old_geometry = None

        self.main_wnd = self.window()
        self.game = self.main_wnd.game

    def getBorderColor(self):
        return self.border_color_start

    def setBorderColor(self, color: QColor):
        style = f'border: 2px solid {color.name()}; border-radius: 8px; background-color: #688fa6)'
        self.setStyleSheet(style)

    # Эта анимация здесь, т.к. она не переиспользуема из-за нестандартного свойства
    def do_border_animation(self, duration: int, start_val, end_val, property_name: QByteArray) -> QPropertyAnimation:
        animation = QPropertyAnimation(self, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_val)
        animation.setEndValue(end_val)
        return animation

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.mouse_released = True
        if self.filled or self.game.ended:
            event.ignore()
            return

        self.filled = True
        player = self.game.current_player

        # Задаем картинку
        img = 'tits.png' if player == 'tits' else 'ass.png'
        self.setPixmap(QPixmap(img))
        self.setScaledContents(True)

        self.animation_group = QParallelAnimationGroup(self)
        # Определяем анимации и добавляем их в группу
        self.img_animation = self.img_opacity_animation(1000, 0.35, 1.0)
        self.animation_group.addAnimation(self.img_animation)

        self.animation_border = self.do_border_animation(500, self.border_color_start, self.border_color_stop,
                                                         QByteArray(b'color'))
        self.animation_group.addAnimation(self.animation_border)

        if self.press_animation_played:
            self.pressing_animation_back = self.press_animation_back(self.geometry(), self.old_geometry, 100)
            self.animation_group.addAnimation(self.pressing_animation_back)
            self.press_animation_played = False


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
        event.accept()

    def mousePressEvent(self, ev: QMouseEvent, /) -> None:
        if self.filled or self.game.ended:
            ev.ignore()
            return

        self.animation_there = self.press_animation_there(self.geometry(), 0.92, 100)
        self.animation_there.start()
        self.animation_there.finished.connect(self.release_animation_controller)
        ev.accept()

    def clear(self, /) -> None:
        self.setPixmap(QPixmap())
        self.filled = False
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        effect.setOpacity(1.0)

    # Запилим эти два метода, чтобы динамически менять старую геометрию виджета
    def move(self, arg__1: QPoint, /) -> None:
        super().move(arg__1)
        self.old_geometry = self.geometry()

    def resize(self, arg__1: QSize, /) -> None:
        super().resize(arg__1)
        self.old_geometry = self.geometry()

    def release_animation_controller(self):
        if self.mouse_released:
            self.animation_back = self.press_animation_back(self.geometry(), self.old_geometry, 100)
            self.animation_back.start()
            self.mouse_released = False

        else:
            self.press_animation_played = True




    borderColor = Property(QColor, getBorderColor, setBorderColor)

