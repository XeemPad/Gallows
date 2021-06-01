import sqlite3

COL_NAMES = ['easy_words', 'medium_words', 'hard_words']
TXT_FILE_NAMES = ['easy_words.txt', 'medium_words.txt', 'hard_words.txt']
DB_FILE_NAME = 'words.db'


def add_words(column_names, text_file_names, db_file_name):
    with open(text_file_names[0]) as f:
        easy_words = f.read().split('\n')
    with open(text_file_names[1]) as f:
        medium_words = f.read().split('\n')
    with open(text_file_names[2]) as f:
        hard_words = f.read().split('\n')
    print(len(easy_words), len(medium_words), len(hard_words))
    ans = input('Продолжить? ')
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    print('Начало')
    k = 1
    for i in range(len(hard_words)):
        print(k)
        col_1 = column_names[0]
        col_2 = column_names[1]
        col_3 = column_names[2]

        easy = easy_words[i] if i < 564 else ''
        medium = medium_words[i] if i < 8456 else ''
        hard = hard_words[i]

        cur.execute(f"INSERT INTO words('{col_1}', '{col_2}', '{col_3}') "
                    f"VALUES('{easy}', '{medium}', '{hard}')")
        k += 1
    print('Конец')
    con.commit()
    print('Сохранено')


add_words(COL_NAMES, TXT_FILE_NAMES, DB_FILE_NAME)
