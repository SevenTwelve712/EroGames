from PySide6.QtCore import QSize, Qt, QParallelAnimationGroup, QPoint
from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout

from TicTacToe.game_logic import Game
from TicTacToe.view.PressableButtonWidget import PressableButtonWidget
from TicTacToe.view.TicTacToeWidget import TicTacWidget
from TicTacToe.view.ToggleSwitchWidget import ToggleSwitchWidget


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

        # Делаем свитч здесь, чтобы определить ресурс пак
        self.switch = ToggleSwitchWidget(200, 80, parent=self)

        self.do_name()
        self.do_step_counter()
        self.do_field()
        self.do_menu()
        self.do_count_tab()
        self.do_resource_pack_choose()

        # Чтоб окно не расползалось по ширине, тк поле у меня не в layout. В теории его нужно было завернуть в виджет,
        # и затем нормально центрировать
        self.setFixedWidth(658)

    def do_name(self):
        self.name = QLabel('Крестики-нолики')
        self.name.setObjectName('name')
        self.center_layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignCenter)

    def do_step_counter(self):
        self.step_counter = QLabel(f'Ход игрока {self.switch.curr_pack.tits_name if self.game.current_player == "tits" else self.switch.curr_pack.ass_name}')
        self.step_counter.setObjectName('step_counter')
        self.center_layout.addWidget(self.step_counter, alignment=Qt.AlignmentFlag.AlignCenter)

    def do_field(self):
        # Добавляем виджет поля (со своей сеткой) в главную сетку
        self.field_widget = QWidget(self)
        self.field_widget.setObjectName('field_widget')
        self.field_widget.setParent(self.center_widget)
        self.center_layout.addWidget(self.field_widget)

        space = 10
        size = 200

        self.field_widget.setMinimumSize(space * 4 + size * 3, space * 4 + size * 3)

        for i in range(3):
            for j in range(3):
                w = TicTacWidget((i, j), parent=self.field_widget)
                w.resize(QSize(200, 200))
                w.move(QPoint(space * (j + 1) + size * j, space * (i + 1) + size * i))

    def do_menu(self):
        self.menu_widget = QWidget()
        menu_layout = QHBoxLayout()
        self.menu_widget.setLayout(menu_layout)

        # Делаем кнопку перезагрузки игры
        reset_shell = QWidget(parent=self.menu_widget)
        reset_shell.setMinimumSize(200, 65)
        self.menu_widget.layout().addWidget(reset_shell, alignment=Qt.AlignCenter)

        reset = PressableButtonWidget('Перезапустить', parent=reset_shell)
        reset.clicked.connect(self.do_reset)
        reset.resize(QSize(200, 65))

        # Делаем кнопку сброса счета
        clear_count_shell = QWidget(parent=self.menu_widget)
        clear_count_shell.setMinimumSize(200, 65)
        self.menu_widget.layout().addWidget(clear_count_shell, alignment=Qt.AlignCenter)

        clear_count = PressableButtonWidget('Очистить счет', parent=clear_count_shell)
        clear_count.clicked.connect(self.do_clear_count)
        clear_count.resize(QSize(200, 65))

        self.center_layout.addWidget(self.menu_widget)

    def do_count_tab(self):
        self.count_tab_widget = QWidget()
        count_tab_layout = QHBoxLayout()
        self.count_tab_widget.setLayout(count_tab_layout)

        # Делаем счет для tits
        tits_count = QLabel(f'{self.switch.curr_pack.tits_name}: 0')
        tits_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_tab_layout.addWidget(tits_count)

        # Делаем счет для ass
        ass_count = QLabel(f'{self.switch.curr_pack.ass_name}: 0')
        ass_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_tab_layout.addWidget(ass_count)

        self.center_layout.addWidget(self.count_tab_widget)

    def do_resource_pack_choose(self):
        self.center_layout.addWidget(self.switch, alignment=Qt.AlignCenter)

        # Блокируем свитч
        self.switch.set_blocked(True)

    def do_reset(self):
        # Остановим анимации победы (если еще идут)
        self.blackout_animations.stop()
        self.border_glowing_animations.stop()

        self.switch.set_blocked(True)

        # Обновим логику игры и поле
        self.game.new_game()
        for widget in self.field_widget.children():
            widget.setGraphicsEffect(None)
            widget.clear()

        self.step_counter.setText(f'Ход игрока {self.switch.curr_pack.tits_name if self.game.current_player == "tits" else self.switch.curr_pack.ass_name}')
        # на всякий случай перезапишем текст в виджетах счета
        self.count_tab_widget.layout().itemAt(0).widget().setText(
            f'{self.switch.curr_pack.tits_name}: {self.game.tits_win}')
        self.count_tab_widget.layout().itemAt(1).widget().setText(
            f'{self.switch.curr_pack.ass_name}: {self.game.ass_win}')

    def do_clear_count(self):
        self.game.reset_count()
        self.count_tab_widget.layout().itemAt(0).widget().setText(f'{self.switch.curr_pack.tits_name}: 0')
        self.count_tab_widget.layout().itemAt(1).widget().setText(f'{self.switch.curr_pack.ass_name}: 0')

    def finish(self, res: str, win_positions: list):
        text = 'Ничья' if res == 'nobody' else f'Выиграл игрок {self.switch.curr_pack.tits_name if res == "tits" else self.switch.curr_pack.ass_name}'
        self.step_counter.setText(text)
        # Если ничья, то больше ничего не надо делать
        if res == 'nobody':
            return
        # Обновим счетчик выигрышей
        self.count_tab_widget.layout().itemAt(0).widget().setText(f'{self.switch.curr_pack.tits_name}: {self.game.tits_win}')
        self.count_tab_widget.layout().itemAt(1).widget().setText(f'{self.switch.curr_pack.ass_name}: {self.game.ass_win}')

        # Затемняем невыигрышные ячейки, подсвечиваем выигрышные
        for widget in self.field_widget.children():
            if widget.coords not in win_positions:
                widget.do_img_opacity_animation(2000, 1.0, 0.4)
                self.blackout_animations.addAnimation(widget.img_opacity_animation)
            else:
                widget.do_img_glowing_pulsar_animation(1000, 20.0, 70.0)
                self.border_glowing_animations.addAnimation(widget.img_glowing_pulsar_animation)

        self.blackout_animations.start()
        self.border_glowing_animations.start()

        # Разблокируем свитч
        self.switch.set_blocked(False)
