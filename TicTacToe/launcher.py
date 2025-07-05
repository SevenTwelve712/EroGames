from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from TicTacToe.game_logic import Game
from TicTacToe.view.MainWindow import MainWnd

game = Game()

app = QApplication([])

# Подгружаем стили
with open('styles.qss', 'r') as styles:
    app.setStyleSheet(styles.read())

main_wnd = MainWnd(game)
main_wnd.setWindowTitle('TicTacToe')
main_wnd.setWindowIcon(QPixmap('nsfw_rp/tits.png'))
main_wnd.move(600, 100)
main_wnd.show()

app.exec()