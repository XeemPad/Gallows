def division_by_difficulty():
    easy_words = []
    medium_words = []
    hard_words = []

    with open('3-10_length_words.txt') as f:
        for word in f.read().split('\n'):
            if len(word) == 3 or len(word) == 4:
                easy_words.append(word)
            elif 5 <= len(word) <= 7:
                medium_words.append(word)
            elif 8 <= len(word) <= 10:
                hard_words.append(word)

    with open('easy_words.txt', 'w') as easy:
        easy.write('\n'.join(easy_words))
    with open('medium_words.txt', 'w') as medium:
        medium.write('\n'.join(medium_words))
    with open('hard_words.txt', 'w') as hard:
        hard.write('\n'.join(hard_words))


def cleaning(file):
    with open(file, 'r') as f:
        file_text = f.read()
    formatted_text = list(filter(lambda symbol: not symbol.isdigit() and symbol != '\t', file_text))
    with open(file, 'w') as f:
        f.write(''.join(formatted_text))


def counting_words(file):
    with open(file, 'r') as f:
        file_text = f.read().split('\n')
        print(len(file_text))


def delete_long(file):
    with open(file, 'r') as f:
        file_text = f.read()
    formatted_text = list(filter(lambda word: len(word) < 7, file_text.split('\n')))
    with open(file, 'w') as f:
        f.write('\n'.join(formatted_text))


def check_and_add(old, new):
    with open(old, 'r') as f:
        old_text = f.read()
    old_words = old_text.split('\n')
    with open(new, 'r') as f:
        new_text = f.read()
    formatted_new_text = list(filter(lambda symbol: symbol.isalpha() or symbol == '\n', new_text))
    print(''.join(formatted_new_text))
    for new_word in ''.join(formatted_new_text).split('\n'):
        if len(new_word) < 7:
            if new_word not in old_words:
                old_words.append(new_word)
    with open(old, 'w') as f:
        f.write('\n'.join(old_words))


counting_words('easy_words.txt')
