from PySide6.QtCore import Property, QPropertyAnimation
from PySide6.QtCore import QRect, QByteArray, QSize, QParallelAnimationGroup
from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QAbstractButton

from TicTacToe.resourse_pack import ResourcePack


class ToggleSwitchWidget(QAbstractButton):
    def __init__(self, width: int, height: int, parent=None):
        super().__init__(parent=parent)

        self.blocked = False

        self.sfw_pack = ResourcePack('sfw')
        self.nsfw_pack = ResourcePack('nsfw')
        self.curr_pack = self.sfw_pack

        self.state = 'sfw'
        self.w = width
        self.h = height
        self.setGeometry(0, 0, width, height)
        self.anim_is_playing = False

        # Рассчитываем круг
        gap = round(height * 0.1)  # 10% от высоты
        r = round(height * 0.4)  # 40% от высоты

        self.round_x = gap
        self.round_y = gap
        self.r = r

        # round positions
        self.curr_round_x = gap
        self.other_round_x = self.w - self.r * 2 - gap

        # colors
        self.curr_switch_color = QColor('#354D73')
        self.other_switch_col = QColor('#87CEEB')
        self.curr_round_color = QColor('#ADD8E6')
        self.other_round_color = QColor('#225587')

        self.pressed.connect(self.switch)

    def paintEvent(self, e: QPaintEvent, /) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QBrush('#082567'), 0.4))

        painter.setBrush(QBrush(self.curr_switch_color))
        painter.drawRoundedRect(QRect(0, 0, self.w, self.h), self.r, self.r)

        painter.setBrush(QBrush(self.curr_round_color))
        painter.drawEllipse(self.round_x, self.round_y, self.r * 2, self.r * 2)

    def switch(self):
        if self.anim_is_playing or self.blocked:
            return

        self.state = 'sfw' if self.state == 'nsfw' else 'nsfw'
        self.curr_pack = self.sfw_pack if self.state == 'sfw' else self.nsfw_pack
        dur = 200
        self.switch_anim = QParallelAnimationGroup()

        round_col_anim = QPropertyAnimation(self, QByteArray(b'roundColor'))
        round_col_anim.setStartValue(self.curr_round_color)
        round_col_anim.setEndValue(self.other_round_color)
        round_col_anim.setDuration(dur)
        self.curr_round_color, self.other_round_color = self.other_round_color, self.curr_round_color

        round_pos_anim = QPropertyAnimation(self, QByteArray(b'roundX'))
        round_pos_anim.setStartValue(self.curr_round_x)
        round_pos_anim.setEndValue(self.other_round_x)
        round_pos_anim.setDuration(dur)
        self.curr_round_x, self.other_round_x = self.other_round_x, self.curr_round_x

        switch_col_anim = QPropertyAnimation(self, QByteArray(b'switchColor'))
        switch_col_anim.setStartValue(self.curr_switch_color)
        switch_col_anim.setEndValue(self.other_switch_col)
        switch_col_anim.setDuration(dur)
        self.curr_switch_color, self.other_switch_col = self.other_switch_col, self.curr_switch_color

        self.switch_anim.addAnimation(round_col_anim)
        self.switch_anim.addAnimation(round_pos_anim)
        self.switch_anim.addAnimation(switch_col_anim)

        self.anim_is_playing = True
        self.switch_anim.finished.connect(lambda: self.set_anim_state(False))
        self.switch_anim.start()

    def set_anim_state(self, val):
        self.anim_is_playing = val

    def set_blocked(self, var: bool):
        if var:
            self.setToolTip('Режим можно переключать только после окончания игры')
            # перерисовываем, чтобы все обновилось
            self.parent().layout().update()
            self.blocked = var
        else:
            self.setToolTip("")
            self.blocked = var

    def sizeHint(self, /) -> QSize:
        return QSize(self.w, self.h)

    def getRoundX(self):
        return self.round_x

    def setRoundX(self, val):
        self.round_x = val
        self.update()

    def getSwitchColor(self):
        return self.curr_switch_color

    def setSwitchColor(self, val):
        self.curr_switch_color = val
        self.update()

    def getRoundColor(self):
        return self.curr_round_color

    def setRoundColor(self, val):
        self.curr_round_color = val
        self.update()

    switchColor = Property(QColor, getSwitchColor, setSwitchColor)
    roundColor = Property(QColor, getRoundColor, setRoundColor)
    roundX = Property(int, getRoundX, setRoundX)
