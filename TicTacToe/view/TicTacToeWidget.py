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
        self.border_color_start = QColor('black')
        self.border_color_stop = QColor('#315b6d')
        self.old_geometry = None

        self.main_wnd = self.window()
        self.game = self.main_wnd.game

    def getBorderColor(self):
        return self.border_color_start

    def setBorderColor(self, color: QColor):
        style = f'border: 2px solid {color.name()}; border-radius: 8px'
        self.setStyleSheet(style)

    # Эта анимация здесь, т.к. она не переиспользуема из-за нестандартного свойства
    def do_border_animation(self, duration: int, start_val, end_val) -> QPropertyAnimation:
        animation = QPropertyAnimation(self, QByteArray(b'borderColor'))
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

        # Задаем картинку
        img = self.main_wnd.switch.curr_pack.tits_img if self.game.current_player == 'tits' else self.main_wnd.switch.curr_pack.ass_img
        self.setPixmap(QPixmap(img))
        self.setScaledContents(True)

        # Анимации
        self.mouse_release_group = QParallelAnimationGroup(self)

        self.do_img_opacity_animation(1000, 0.35, 1.0)
        self.mouse_release_group.addAnimation(self.img_opacity_animation)

        # Если анимация нажатия уже проиграна, добавляем анимации отжатия. Если нет, этим будет заниматься контроллер
        if self.press_animation_played:
            self.border_animation_back = self.do_border_animation(100, self.border_color_stop, self.border_color_start)
            self.mouse_release_group.addAnimation(self.border_animation_back)

            self.do_press_animation_back(self.geometry(), self.old_geometry, 100)
            self.mouse_release_group.addAnimation(self.press_animation_back)

            self.press_animation_played = False

        self.mouse_release_group.start()

        # Обновляем игровую логику. По идее, это нужно делать в начале,
        # но тогда анимация финиша будет играть до анимации самой ячейки, и произойдет накладка
        res = self.game.step(self.coords)
        if res:
            win_positions = self.game.get_win_positions()
            self.main_wnd.finish(res, win_positions)
        else:
            step_counter = self.main_wnd.step_counter
            step_counter.setText(f'Ход игрока {self.main_wnd.switch.curr_pack.tits_name if self.game.current_player == "tits" else self.main_wnd.switch.curr_pack.ass_name}')
        event.accept()

    def mousePressEvent(self, ev: QMouseEvent, /) -> None:
        if self.filled or self.game.ended:
            ev.ignore()
            return

        self.mouse_press_group = QParallelAnimationGroup(self)

        self.border_animation_there = self.do_border_animation(100, self.border_color_start, self.border_color_stop)
        self.mouse_press_group.addAnimation(self.border_animation_there)

        self.do_press_animation_there(self.geometry(), 0.92, 100)
        self.mouse_press_group.addAnimation(self.press_animation_there)

        self.mouse_press_group.finished.connect(self.release_animation_controller)
        self.mouse_press_group.start()
        ev.accept()

    def clear(self, /) -> None:
        self.setPixmap(QPixmap())
        self.filled = False
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        effect.setOpacity(1.0)

    # Переопределим эти два метода, чтобы динамически менять старую геометрию виджета
    def move(self, arg__1: QPoint, /) -> None:
        super().move(arg__1)
        self.old_geometry = self.geometry()

    def resize(self, arg__1: QSize, /) -> None:
        super().resize(arg__1)
        self.old_geometry = self.geometry()

    def release_animation_controller(self):
        if self.mouse_released:
            # Если так, то мышь была отжата до того, как анимации нажатия проигрались,
            # значит нам надо их проиграть сейчас
            self.mouse_release_group = QParallelAnimationGroup(self)

            self.border_animation_back = self.do_border_animation(100, self.border_color_stop, self.border_color_start)
            self.mouse_release_group.addAnimation(self.border_animation_back)

            self.do_press_animation_back(self.geometry(), self.old_geometry, 100)
            self.mouse_release_group.addAnimation(self.press_animation_back)

            self.mouse_release_group.start()
            self.mouse_released = False

        else:
            # В ином случае анимации нажатия проиграет событие отжатия мыши
            self.press_animation_played = True

    borderColor = Property(QColor, getBorderColor, setBorderColor)
