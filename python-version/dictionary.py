import json
from random import sample, shuffle

TEST = False
N_WORDS = 1000


def load_dict(file_path, random=False):
    print(">> Loading Dictionary")
    with open(file_path, 'r', encoding="utf8") as file:
        full_dictionary = json.load(file)
    if random:
        shuffle(full_dictionary)
    dictionary = {item['word']: sample(item['definitions'], 1)[0] for item in full_dictionary if item['definitions']}
    print("Founded dictionary with %d words. \nHead:" % len(dictionary))
    for i, (word, definition) in enumerate(dictionary.items()):
        if i < 20:
            print("    %s: %s" % (word, definition))
    return dictionary


def get_dictionary(test=TEST, n_words=N_WORDS, random=False, origin_file='../words_test.json'):
    file_full = '../words.json'
    file_test = origin_file
    dict_full = load_dict(file_full, random=random and not test)
    dict_test = load_dict(file_test, random=random and not test)
    n = len(dict_test)
    if test:
        dictionary_list = list()
        for i, (word, definition) in enumerate(dict_full.items()):
            if i >= n_words - n:
                break
            dictionary_list.append((word, definition))
        for i, (word, definition) in enumerate(dict_test.items()):
            if i >= n:
                break
            dictionary_list.append((word, definition))
        if random and not test:
            shuffle(dictionary_list)
        dictionary = {x[0]: x[1] for x in dictionary_list}
    else:
        dictionary = dict_full
    return dictionary




