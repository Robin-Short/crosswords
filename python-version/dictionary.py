import json
from random import sample, shuffle

TEST = False
N_WORDS = 1000


def load_dict(file_path):
    print(">> Loading Dictionary")
    with open(file_path, 'r', encoding="utf8") as file:
        full_dictionary = json.load(file)
    shuffle(full_dictionary)
    dictionary = {item['word']: sample(item['definitions'], 1)[0] for item in full_dictionary if item['definitions']}
    print("Founded dictionary with %d words. \nHead:" % len(dictionary))
    for i, (word, definition) in enumerate(dictionary.items()):
        if i < 20:
            print("    %s: %s" % (word, definition))
    return dictionary


def get_dictionary(test=TEST, n_words=N_WORDS):
    file_full = '../words.json'
    file_test = '../words_test.json'
    dict_full = load_dict(file_full)
    dict_test = load_dict(file_test)
    if test:
        for i, (word, definition) in enumerate(dict_full.items()):
            if i >= n_words:
                break
            dict_test[word] = definition
        dictionary = dict_test
    else:
        dictionary = dict_full
    return dictionary




