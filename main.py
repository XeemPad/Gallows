import sys
import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# Интерфейс главного окна:
from interface import Ui_MainWindow
# Работа с базой слов
import getting_words_from_db


EASY = 1
MEDIUM = 2
HARD = 3
column_names_of_difficulties = {EASY: 'easy_words', MEDIUM: 'medium_words',
                                HARD: 'hard_words'}
STAGES_PICTURES_DIRECTORIES = {0: 'pictures/stage_0.png', 1: 'pictures/stage_1.png',
                               2: 'pictures/stage_2.png', 3: 'pictures/stage_3.png',
                               4: 'pictures/stage_4.png', 5: 'pictures/stage_5.png',
                               6: 'pictures/stage_6.png', 7: 'pictures/stage_7.png',
                               8: 'pictures/stage_8.png', 9: 'pictures/stage_9.png',
                               10: 'pictures/stage_10.png', }
GALLOWS_STAGES_PICTURE_DIRECTORY = 'pictures/gallows_stages.png'
LOGO_DIRECTORY = 'pictures/logo.png'
ABOUT_FILE_DIRECTORY = 'about.txt'
RULES_FILE_DIRECTORY = 'rules.txt'
difficulties_to_names = {EASY: 'Лёгкая', MEDIUM: 'Средняя', HARD: 'Сложная'}
names_to_difficulties = {'Лёгкая': EASY, 'Средняя': MEDIUM, 'Сложная': HARD}
ENTERED_LETTERS_DEFAULT_TEXT = 'Список введённых букв: '
RUSSIAN_LETTERS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
ABOUT_WINDOW_SIZE = [400, 200]
MAIN_WINDOW_SIZE = [600, 700]
GALLOWS_WINDOW_SIZE = [800, 440]
RULES_WINDOW_SIZE = [700, 700]
LOGO_SCALE_SIZE = [256, 40]
STANDARD_FONT = 'Tahoma'


# Класс ошибки отстутствия базы данных в файлах игры:
class DataBaseNotFound(FileExistsError):
    pass


# Три класса побочных окон:
class AboutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global ABOUT_WINDOW_SIZE, LOGO_DIRECTORY, LOGO_SCALE_SIZE, STANDARD_FONT

        self.setGeometry(500, 500, *ABOUT_WINDOW_SIZE)
        self.setWindowTitle('О программе')

        font = QFont()
        font.setFamily(STANDARD_FONT)
        font.setPointSize(12)

        self.about_text = QLabel(self)
        self.setFont(font)
        self.about_text.setGeometry(20, 10, ABOUT_WINDOW_SIZE[0] - 20, ABOUT_WINDOW_SIZE[1] - 10)
        self.about_text.setWordWrap(True)
        self.about_text.setAlignment(Qt.AlignHCenter)
        self.about_text.setText(self.read_text_from_file())
        self.about_text.setTextInteractionFlags(Qt.TextSelectableByMouse)


        self.logo = QLabel(self)
        self.logo.move((ABOUT_WINDOW_SIZE[0] - LOGO_SCALE_SIZE[0]) // 2,
                       (ABOUT_WINDOW_SIZE[1] - LOGO_SCALE_SIZE[1]) - 15)
        try:
            logo = open(LOGO_DIRECTORY)
        except FileNotFoundError:
            error = (f'Директория "{LOGO_DIRECTORY}" не найдена. '
                     'Проверьте целостность файлов игры')
            QMessageBox.critical(self, 'Ошибка', error)
        else:
            logo.close()
            self.logo_pixmap = QPixmap(LOGO_DIRECTORY).scaled(*LOGO_SCALE_SIZE)
            self.logo.setPixmap(self.logo_pixmap)

    def read_text_from_file(self):
        global ABOUT_FILE_DIRECTORY
        try:
            about_text = open(ABOUT_FILE_DIRECTORY)
        except FileNotFoundError:
            error = (f'Директория "{ABOUT_FILE_DIRECTORY}" не найдена. '
                     'Проверьте целостность файлов игры')
            QMessageBox.critical(self, 'Ошибка', error)
        else:
            text = about_text.read()
            about_text.close()
            return text


class GallowsStagesPictureWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global GALLOWS_STAGES_PICTURE_DIRECTORY

        self.setGeometry(300, 300, *GALLOWS_WINDOW_SIZE)
        self.setWindowTitle('Этапы виселицы (Число - количество совершённых ошибок)')

        self.picture = QLabel(self)
        self.picture.move(0, 0)

        try:
            picture = open(GALLOWS_STAGES_PICTURE_DIRECTORY)
        except FileNotFoundError:
            error = (f'Директория "{GALLOWS_STAGES_PICTURE_DIRECTORY}" не найдена. '
                     'Проверьте целостность файлов игры')
            QMessageBox.critical(self, 'Ошибка', error)
        else:
            picture.close()
            self.pixmap = QPixmap(GALLOWS_STAGES_PICTURE_DIRECTORY)
            self.picture.setPixmap(self.pixmap)


class RulesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global RULES_FILE_DIRECTORY, STANDARD_FONT

        self.setGeometry(300, 100, *RULES_WINDOW_SIZE)
        self.setWindowTitle('Правила игры')

        font = QFont()
        font.setFamily(STANDARD_FONT)
        font.setPointSize(14)

        self.rules_text = QLabel(self)
        self.setFont(font)
        self.rules_text.setGeometry(20, 10, RULES_WINDOW_SIZE[0] - 20, RULES_WINDOW_SIZE[1] - 10)
        self.rules_text.setWordWrap(True)
        self.rules_text.setText(self.read_rules_from_file())

    def read_rules_from_file(self):
        global RULES_FILE_DIRECTORY

        try:
            rules_text = open(RULES_FILE_DIRECTORY)
        except FileNotFoundError:
            error = (f'Директория "{RULES_FILE_DIRECTORY}" не найдена. '
                     'Проверьте целостность файлов игры')
            QMessageBox.critical(self, 'Ошибка', error)
        else:
            text = rules_text.read()
            rules_text.close()
            return text


# Класс главного окна:
class MyGame(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        global EASY, MEDIUM, HARD, difficulties_to_names
        self.move(400, 200)
        self.setFixedSize(*MAIN_WINDOW_SIZE)
        self.setWindowTitle('Игра "Виселица"')

        self.difficulty = EASY
        self.current_stage = 0

        self.entered_letters_list = []
        self.entered_words_list = []

        self.is_game_over = False

        self.enter_bind_is_on = True
        self.restart_bind_is_on = False

        self.gallows_picture = QLabel(self)
        self.gallows_picture.move(50, 100)
        self.gallows_picture.resize(400, 400)

        # Перепопределение элементов интерфейса:
        self.difficultyLabel.setText(f'Сложность: {difficulties_to_names[self.difficulty]}')
        self.restartBtn.clicked.connect(self.start_new_game)
        self.action_1.triggered.connect(self.change_difficulty)
        self.action_2.triggered.connect(self.change_difficulty)
        self.action_3.triggered.connect(self.change_difficulty)
        self.action_rules.triggered.connect(self.open_widget_with_rules)
        self.action_stages.triggered.connect(self.open_widget_with_stages)
        self.action_enter_bind.triggered.connect(self.on_off_enter_bind)
        self.action_restart_bind.triggered.connect(self.on_off_restart_bind)
        self.enterLetterBtn.clicked.connect(self.enter_letter)
        self.enterWordBtn.clicked.connect(self.enter_word)
        self.action_about.triggered.connect(self.open_about)

        self.start_new_game()

    def on_off_enter_bind(self):
        if self.action_enter_bind.isChecked():
            self.enter_bind_is_on = True
        else:
            self.enter_bind_is_on = False

    def on_off_restart_bind(self):
        if self.action_restart_bind.isChecked():
            self.restart_bind_is_on = True
        else:
            self.restart_bind_is_on = False

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.enter_bind_is_on:
            self.enter_letter()
        elif event.key() == Qt.Key_F1 and self.restart_bind_is_on:
            self.start_new_game()

    def check_win(self):
        if set(self.hidden_word) <= set(self.entered_letters_list):
            self.is_game_over = True
            self.infoLabel.setText('Вы победили! Поздравляем')

    def change_difficulty(self):
        global names_to_difficulties, difficulties_to_names
        new_dif_text = self.sender().text()
        new_difficulty = names_to_difficulties[new_dif_text]
        if new_difficulty != self.difficulty:
            # Сброс "галочки" прошлой выбранной сложности в меню выбора сложности:
            exec(f'self.action_{self.difficulty}.setChecked(False)')
            # Установка галочки для нужного уровня сложности:
            exec(f'self.action_{new_difficulty}.setChecked(True)')
            self.difficulty = new_difficulty
            self.infoLabel.setText('Сложность будет изменена на'
                                   f' "{difficulties_to_names[self.difficulty]}" '
                                   'в начале следующей игры')
        else:
            # Возврат снятой галочки:
            exec(f'self.action_{new_difficulty}.setChecked(True)')

    def change_picture(self):
        global STAGES_PICTURES_DIRECTORIES
        try:
            f = open(STAGES_PICTURES_DIRECTORIES[self.current_stage])
        except FileNotFoundError:
            error = f'Директория {STAGES_PICTURES_DIRECTORIES[self.current_stage]} не найдена. ' \
                    'Проверьте целостность файлов игры'
            QMessageBox.critical(self, 'Ошибка', error)
        else:
            f.close()
            gallows_pixmap = QPixmap(STAGES_PICTURES_DIRECTORIES[self.current_stage])
            self.gallows_picture.setPixmap(gallows_pixmap)

    def enter_letter(self):
        global RUSSIAN_LETTERS, ENTERED_LETTERS_DEFAULT_TEXT

        if self.is_game_over:
            return
        entered_letter = self.enterLetterLineEdit.text().lower()
        if entered_letter not in RUSSIAN_LETTERS:
            self.infoLabel.setText('Вы ввели букву нерусского алфавита')
        elif entered_letter in self.entered_letters_list:
            self.infoLabel.setText('Вы уже вводили данную букву')
        elif entered_letter.isalpha():
            global ENTERED_LETTERS_DEFAULT_TEXT
            # Добавляем букву в список введённых и отображаем её на соотвествущем QLabel:
            self.entered_letters_list += entered_letter
            self.enteredLettersListLabel.setText(ENTERED_LETTERS_DEFAULT_TEXT +
                                                 ' '.join(self.entered_letters_list))

            if entered_letter in self.hidden_word:
                self.infoLabel.setText(f'Верно! Буква "{entered_letter}" есть в загаданном слове')

                reformatted_hidden_word = list(self.hiddenWordLineEdit.text())
                for i, let in enumerate(self.hidden_word):
                    if let == entered_letter:
                        reformatted_hidden_word[i * 2] = let
                # Изменение отображения загаданного слова:
                self.hiddenWordLineEdit.setText(''.join(reformatted_hidden_word))
                # Проверка победы:
                self.check_win()
            else:
                self.infoLabel.setText(f'Буквы "{entered_letter}" не оказалось в загаданном слове')
                # Переход к следующему этапу виселицы:
                self.current_stage += 1
                self.next_stage()
        else:
            self.infoLabel.setText('Проверьте корректность введённой буквы.')

    def enter_word(self):
        global RUSSIAN_LETTERS

        if self.is_game_over:
            return
        entered_word = self.enterWordLineEdit.text().lower().strip()
        for letter in entered_word:
            if letter not in RUSSIAN_LETTERS:
                self.infoLabel.setText('Введённое слово содержит букву нерусского алфавита')
                return
        if entered_word in self.entered_words_list:
            self.infoLabel.setText('Вы уже вводили данное слово')
        elif entered_word.isalpha():
            if len(entered_word) != len(self.hidden_word):
                self.infoLabel.setText('Длина введённого слова не соответствует длине загаданного')
            elif entered_word == self.hidden_word:
                global ENTERED_LETTERS_DEFAULT_TEXT

                self.entered_letters_list.extend(list(entered_word))
                self.enteredLettersListLabel.setText(ENTERED_LETTERS_DEFAULT_TEXT +
                                                     ' '.join(self.entered_letters_list))
                # Изменение отображения загаданного слова:
                self.hiddenWordLineEdit.setText(' '.join(list(self.hidden_word)))
                # Запуск функции победы:
                self.check_win()
            else:
                self.infoLabel.setText('Вы не угадали слово. Это засчиталось как 2 ошибки')
                self.current_stage += 2
                self.next_stage()
        else:
            self.infoLabel.setText('Проверьте корректность введённого слова.')

    def generate_hidden_word(self, difficulty):
        # Задаём имя столбца(в базе данных), из которого будем брать слова:
        column_name = column_names_of_difficulties[difficulty]
        # Получаем список слов нужной сложности
        words_list = getting_words_from_db.get_words(column_name)
        # Проверяем на ошибки:
        if words_list[0] == 'no_db':
            error = (f'Директория "{words_list[1]}" не найдена. '
                     'Проверьте целостность файлов игры')
            QMessageBox.critical(self, 'Ошибка', error)
            raise DataBaseNotFound(f'База данных в директории "{words_list[1]}" не найдена')
        generated_word = random.choice(words_list)
        return generated_word

    def next_stage(self):
        # Изменение рисунка виселицы:
        self.change_picture()
        # Изменение значения прогресс-бара:
        self.mistakesProgressBar.setValue(self.current_stage)

        if self.current_stage >= 10:
            self.is_game_over = True
            self.hiddenWordLineEdit.setText(' '.join(list(self.hidden_word)))
            self.infoLabel.setText('К сожалению, вы проиграли. Но вы можете сыграть снова!')
            self.current_stage = 0

    def open_about(self):
        self.about_widget = AboutWidget()
        self.about_widget.show()

    def open_widget_with_rules(self):
        self.rules_widget = RulesWidget()
        self.rules_widget.show()

    def open_widget_with_stages(self):
        self.gallows_widget = GallowsStagesPictureWidget()
        self.gallows_widget.show()

    def start_new_game(self):
        global difficulties_to_names, ENTERED_LETTERS_DEFAULT_TEXT

        self.is_game_over = False
        self.difficultyLabel.setText(f'Сложность: {difficulties_to_names[self.difficulty]}')

        self.entered_letters_list = []
        self.entered_words_list = []

        self.current_stage = 0

        # Очистка информационной таблички:
        self.infoLabel.setText('')
        # Очистка полей для ввода буквы и слова:
        self.enterLetterLineEdit.setText('')
        self.enterWordLineEdit.setText('')
        # Очистка прогресс-бара:
        self.mistakesProgressBar.setValue(self.current_stage)
        # Очистка списка введённых букв:
        self.enteredLettersListLabel.setText(ENTERED_LETTERS_DEFAULT_TEXT)

        # Вставляем рисунок для нулевого этапа:
        self.change_picture()
        # Генерация загадываемого слова:
        self.hidden_word = self.generate_hidden_word(self.difficulty)

        # Вставка загадываемого слова в поле вывода в скрытом виде:
        formatted_hidden_word = ' '.join('_' for _ in range(len(self.hidden_word)))
        self.hiddenWordLineEdit.setText(formatted_hidden_word)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyGame()
    window.show()

    sys.exit(app.exec())
