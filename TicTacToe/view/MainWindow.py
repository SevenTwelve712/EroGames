from PySide6.QtCore import QSize, Qt, QByteArray, QParallelAnimationGroup
from PySide6.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, QVBoxLayout, QPushButton, \
    QHBoxLayout

from TicTacToe.view.TicTacToeWidget import TicTacWidget
from TicTacToe.game_logic import Game


class MainWnd(QMainWindow):
    def __init__(self, game: Game) -> None:
        super().__init__()

        # Устанавливаем центральный виджет и добавляем сетку
        self.game = game
        self.center_widget = QWidget()
        self.setCentralWidget(self.center_widget)
        self.center_layout = QVBoxLayout()
        self.center_widget.setLayout(self.center_layout)

        # Устанавливаем класс финишных анимаций (нужно здесь, чтобы в любой момент можно было перезапустить игру)
        self.blackout_animations = QParallelAnimationGroup()
        self.border_glowing_animations = QParallelAnimationGroup()

        self.do_name()
        self.do_step_counter()
        self.do_field()
        self.do_menu()
        self.do_count_tab()

    def do_name(self):
        self.name = QLabel('Крестики-нолики')
        self.name.setObjectName('name')
        self.center_layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignCenter)

    def do_step_counter(self):
        self.step_counter = QLabel(f'Ход игрока {self.game.current_player}')
        self.step_counter.setObjectName('step_counter')
        self.center_layout.addWidget(self.step_counter, alignment=Qt.AlignmentFlag.AlignCenter)

    def do_field(self):
        # Добавляем виджет поля (со своей сеткой) в главную сетку
        self.field_widget = QWidget(self)
        self.field_widget.setObjectName('field_widget')
        self.field_widget.setParent(self.center_widget)

        field = QGridLayout()
        self.field_widget.setLayout(field)
        self.center_layout.addWidget(self.field_widget)

        for i in range(3):
            for j in range(3):
                w = TicTacWidget((i, j), parent=self.field_widget)
                w.setFixedSize(QSize(200, 200))
                field.addWidget(w, i, j)

    def do_menu(self):
        self.menu_widget = QWidget()
        menu_layout = QHBoxLayout()
        self.menu_widget.setLayout(menu_layout)

        # Делаем кнопку перезагрузки игры
        reset = QPushButton('Перезапустить')
        reset.clicked.connect(self.do_reset)
        reset.setMaximumSize(QSize(200, 100))
        self.menu_widget.layout().addWidget(reset)

        # Делаем кнопку сброса счета
        clear_count = QPushButton('Очистить счет')
        clear_count.clicked.connect(self.do_clear_count)
        clear_count.setMaximumSize(QSize(200, 100))
        self.menu_widget.layout().addWidget(clear_count)

        self.center_layout.addWidget(self.menu_widget)

    def do_count_tab(self):
        self.count_tab_widget = QWidget()
        count_tab_layout = QHBoxLayout()
        self.count_tab_widget.setLayout(count_tab_layout)

        # Делаем счет для tits
        tits_count = QLabel('Tits: 0')
        tits_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_tab_layout.addWidget(tits_count)

        # Делаем счет для ass
        ass_count = QLabel('Ass: 0')
        ass_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_tab_layout.addWidget(ass_count)

        self.center_layout.addWidget(self.count_tab_widget)

    def do_reset(self):
        # Остановим анимации победы (если еще идут)
        self.blackout_animations.stop()
        self.border_glowing_animations.stop()

        # Обновим логику игры и поле
        self.game.new_game()
        field_layout = self.center_layout.itemAt(2).widget().layout()
        for i in range(field_layout.count()):
            field_layout.itemAt(i).widget().clear()
        self.step_counter.setText(f'Ход игрока {self.game.current_player}')

    def do_clear_count(self):
        self.game.reset_count()
        self.count_tab_widget.layout().itemAt(0).widget().setText(f'Tits: 0')
        self.count_tab_widget.layout().itemAt(1).widget().setText(f'Ass: 0')

    def finish(self, res: str, win_positions: list):
        text = 'Ничья' if res == 'nobody' else f'Выиграл игрок {res}'
        self.step_counter.setText(text)
        # Если ничья, то больше ничего не надо делать
        if res == 'nobody':
            return
        # Обновим счетчик выигрышей
        self.count_tab_widget.layout().itemAt(0).widget().setText(f'Tits: {self.game.tits_win}')
        self.count_tab_widget.layout().itemAt(1).widget().setText(f'Ass: {self.game.ass_win}')

        field_layout: QGridLayout = self.field_widget.layout()
        # Анимация победы.
        # Затемняем невыигрышные ячейки
        animations = []
        for row in range(3):
            for col in range(3):
                if (row, col) not in win_positions:
                    widget: TicTacWidget = field_layout.itemAtPosition(row, col).widget()
                    animations.append(widget.animate_img_opacity(2000, 1.0, 0.4))
        for animation in animations:
            self.blackout_animations.addAnimation(animation)

        # Делаем анимацию свечения бордера
        for row, col in win_positions:
            widget: TicTacWidget = field_layout.itemAtPosition(row, col).widget()
            self.border_glowing_animations.addAnimation(widget.animate_img_glowing_pulsar(1000, 20.0, 200.0))
        self.blackout_animations.start()
        self.border_glowing_animations.start()
