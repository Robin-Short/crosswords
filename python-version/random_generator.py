from random import shuffle, random, sample
from crosswords import Crosswords, HORIZONTAL, VERTICAL
from dictionary import get_dictionary
from tree import Tree
from time import time
import re
import os

SLOW = False

def matches_pattern(word, pattern):
    for wp, pp in zip(word, pattern):
        if pp != '.' and wp != pp:
            return False
    return True

def clear_console():
    # Imposta la variabile TERM se non è già impostata
    if 'TERM' not in os.environ:
        os.environ['TERM'] = 'xterm-256color'

    # Per Windows
    if os.name == 'nt':
        os.system('cls')
    # Per macOS e Linux (os.name è 'posix')
    else:
        os.system('clear')


class Cache:
    def __init__(self):
        self.re = dict()
        self.scores = dict()
        self.paths = dict()
        self.RE = {"keys": 0, "uses": 0}
        self.SCORES = {"keys": 0, "uses": 0}
        self.PATHS = {"keys": 0, "uses": 0}

    def get_re(self, key):
        if key in self.re:
            self.RE["uses"] += 1
            return self.re[key]
        return None

    def get_scores(self, key):
        if key in self.scores:
            self.SCORES["uses"] += 1
            return self.scores[key]
        return None

    def get_paths(self, key):
        if key in self.paths:
            self.PATHS["uses"] += 1
            return self.paths[key]
        return None

    def add_re(self, key, value):
        if not key in self.re:
            self.re[key] = value
            self.RE["keys"] += 1

    def add_scores(self, key, value):
        if not key in self.re:
            self.scores[key] = value
            self.SCORES["keys"] += 1

    def add_paths(self, key, value):
        if not key in self.re:
            self.paths[key] = value
            self.PATHS["keys"] += 1

    def __str__(self):
        txt = "CACHE USES:" \
            "\n                             KEYS\t\t\tUSES" \
            "\n----------------------------------------------------------------" \
            "\n - REGOULAR EXPRESSIONS:     %d\t\t\t%d" \
            "\n - SCORES:                   %d\t\t\t%d" \
            "\n - PATHS:                    %d\t\t\t%d" \
            "\n" % (self.RE["keys"], self.RE["uses"], self.SCORES["keys"],
                    self.SCORES["uses"], self.PATHS["keys"], self.PATHS["uses"])
        return txt


class Generator:
    def __init__(self, crossword, dictionary):
        self.crossword = crossword
        self.dictionary = dictionary
        self.moves = []
        for i, j in self.crossword.numbers_list:
            if self.crossword[i, j].horizontal_length > 0:
                self.moves.append((i, j, HORIZONTAL))
            if self.crossword[i, j].vertical_length > 0:
                self.moves.append((i, j, VERTICAL))
        self.sort_criterya = {
            "long_column_first": lambda x: 100 * x[2] + len(self.crossword.get_word(x)),
            "long_rows_first": lambda x: 100 * (1 - x[2]) + len(self.crossword.get_word(x)),
            "short_column_first": lambda x: 100 * x[2] - len(self.crossword.get_word(x)),
            "short_rows_first": lambda x: 100 * (1 - x[2]) - len(self.crossword.get_word(x)),
            "long_first": lambda x: len(self.crossword.get_word(x)),
            "short_first": lambda x: 100 - len(self.crossword.get_word(x)),
            "more_intersections_first": lambda x: len(self.crossword.crosses[x]),
            "less_intersection_first": lambda x: 100 - len(self.crossword.crosses[x])
        }
        self.moves.sort(key=self.sort_criterya["long_first"])
        self.cache = Cache()
        self.optimized_dictionary = self.get_optimized_dictionary()
        # CONTROL PARAMETERS
        self.START_TIME = None

    def get_optimized_dictionary(self):
        res = dict()
        lengths = set()
        for move in self.moves:
            lengths.add(len(self.crossword.move_word_map[move]))
        for word in self.dictionary.keys():
            n = len(word)
            if n in lengths:
                if n in res:
                    res[n].append(word)
                else:
                    res[n] = [word]
        for length in lengths:
            if res[length] == list():
                raise ValueError("Non ci sono parole lunghe %d" % length)
        return res

    def find_possible_words(self, pattern):
        pattern_re = re.compile(pattern)
        res, n  = [], len(pattern)
        iterable = self.optimized_dictionary[n]
        for word in iterable:
            #if matches_pattern(word, pattern):
            if pattern_re.fullmatch(word):
                res.append(word)
        return res

    def get_score(self, move, word):
        res = 1
        pattern = self.crossword.get_word(move)
        self.crossword.set_word(move, word)
        for m in self.crossword.crosses[move]:
            cross_pattern = self.crossword.get_word(m)
            words = self.cache.get_re(cross_pattern)
            if words is None:
                self.cache.add_re(cross_pattern, self.find_possible_words(cross_pattern))
                words = self.cache.get_re(pattern)
            res *= len(words)
            if res == 0:
                break
        self.crossword.set_word(move, pattern)
        return res

    def get_scores(self, move, words, reverse=True):
        scores, total = list(), 0
        for word in words:
            score = self.get_score(move, word)
            scores.append((word, score))
            total += score
        scores.sort(key=lambda x: x[1], reverse=reverse)
        return scores, total

    def choose_random_word(self, move, words, naive=False):
        if naive:
            if words:
                word = sample(words, 1)[0]
            else:
                word = None
            return word
        else:
            scores, total = self.get_scores(move, words)
            if total == 0:
                return None
            x = random() * total
            left = 0
            for word, score in scores:
                right = left + score
                if left <= x <= right:
                    return word
                left = right


    def visit_random(self, view=False):
        if not self.moves:
            print(str(self.crossword))
            self.crossword.show(self.dictionary)
            return True
        #shuffle(self.moves)
        used_moves = list()
        stop, found_solution = False, False
        while self.moves != [] and not stop:
            move = self.moves.pop()
            pattern = self.crossword.get_word(move)
            used_moves.insert(0, move)
            words = self.cache.get_re(pattern)
            if words is None:
                self.cache.add_re(pattern, self.find_possible_words(pattern))
                words = self.cache.get_re(pattern)
            word = self.choose_random_word(move, words)
            stop = word is None
            if not stop:
                self.crossword.set_word(move, word)
                found_solution = self.moves == []
        if view:
            self.crossword.sync()
            print(self.crossword)
        self.moves += used_moves
        if found_solution:
            return True
        else:
            # Clean
            for move in used_moves:
                self.crossword.del_word(move, consistency=False)
            return False

    def visit(self, max_attempts=float('inf'), observe=float('inf')):
        self.START_TIME = time()
        solution, attempts = False, 0
        while not solution and attempts < max_attempts:
            view = attempts % observe == 0
            solution = self.visit_random(view=view)
            attempts += 1
            if view:
                print()
                print("Paths:                   ", attempts)
                print("Time:                    ", time() - self.START_TIME)
                print("Time per path (ms):      ", ((1000000 * (time() - self.START_TIME)) //
                                                    max(1, attempts)) / 1000)
                print(self.cache)
        print()
        # Details
        print()
        print("Paths:                   ", attempts)
        print("Time:                    ", time() - self.START_TIME)
        print("Time per path (ms):      ", ((1000000 * (time() - self.START_TIME)) //
                                            max(1, attempts)) / 1000)
        print(self.cache)
        # Void crossword and definitions
        if solution:
            print(self.crossword.__str__(numbers=True))
            self.crossword.show(self.dictionary)
        # Last crossword
        print(self.crossword)
        # Words
        print(generator.crossword.move_word_map)
        return solution

if __name__ == "__main__":
    '''crossword = Crosswords(12, 8,
                           [(0, 5), (0, 7), (0, 9), (1, 2), (1, 4), (1, 2), (1, 4), (2, 3), (3, 1), (4, 0), (4, 11),
                            (5, 7), (5, 11), (6, 0), (6, 8), (6, 9), (7, 0), (7, 1), (7, 2), (7, 5)])'''
    crossword = Crosswords(5, 5, [])
    '''[(0, 4), (0, 10),
    (1, 4), (1, 10),
    (3, 3), (3, 7),
    (4, 6), (4, 12), (4, 13), (4, 14),
    (5, 0), (5, 1), (5, 5), (5, 9),
    (6, 4),
    (7, 3), (7, 11),
    (8, 10),
    (9, 5), (9, 9), (9, 13), (9, 14),
    (10, 0), (10, 1), (10, 2), (10, 8),
    (11, 7), (11, 11),
    (13, 4), (13, 10),
    (14, 4), (14, 10),
    ])'''
   # crossword.set_word((0, 0, 0), "CASA")
   # crossword.set_word((0, 5, 0), "CAPRA")
   # crossword.set_word((0, 0, 1), "CAMPO")
   # crossword.set_word((2, 0, 0), "MADAMABUTTERFLY")
    #crossword.set_word((1, 11, 0), "BELA")
   # crossword.set_word((3, 8, 0), "CAPRAIA")
   # crossword.set_word((5, 2, 0), "TRE")
   # crossword.set_word((3, 8, 0), "CAPRAIA")
   # crossword.set_word((6, 0, 0), "TORO")
   # crossword.set_word((7, 12, 0), "CAPRAIA")
   ## crossword.set_word((8, 0, 0), "PIANOFORTE")
    #crossword.set_word((9, 10, 0), "SOS")
   # crossword.set_word((10, 9, 0), "TEATRO")
    #crossword.set_word((11, 0, 0), "PERLATO")
    #crossword.set_word((13, 0, 0), "VASO")
   ## crossword.set_word((14, 11, 0), "ORZO")

    print(crossword.__str__(numbers=True))
    dictionary = get_dictionary(test=False, n_words=4230, random=True)
    generator = Generator(crossword, dictionary=dictionary)
    print(generator.visit(max_attempts=20000, observe=100))



