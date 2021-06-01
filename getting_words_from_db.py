def get_words(column_name):
    import sqlite3

    db_file_name = 'words/words.db'
    lengths_of_words_lists = {'easy_words': 564, 'medium_words': 8456, 'hard_words': 11935}

    try:
        f = open(db_file_name)
    except FileNotFoundError:
        return 'no_db', db_file_name
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()

    length = lengths_of_words_lists[column_name]
    words = cur.execute(f'SELECT {column_name} FROM words '
                        f'WHERE {column_name} is not NULL').fetchmany(length)
    
    # Представление слов в виде строк, вместо кортежей
    words = list(map(lambda tpl: tpl[0], words))
    
    return words
