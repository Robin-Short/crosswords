from random import shuffle
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
        self.moves.sort(key=lambda x: 100 * x[2] + len(self.crossword.get_word(x)))
        self.cache = dict()
        self.optimized_dictionary = self.get_optimized_dictionary()
        self.tree = Tree(content=(None, None))
        # CONTROL PARAMETERS
        self.VISITS = 0
        self.LEAVES = 0
        self.CACHE_ACCESSES = 0
        self.CACHE_WORDS = 0
        self.START_TIME = None

    def save_tree(self, filename="tree.txt"):
        with open(filename, "w") as file:
            file.write(self.tree.preorder_visit())

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
        res = []
        for word in self.optimized_dictionary[len(pattern)]:
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
            if not cross_pattern in self.cache:
                self.cache[cross_pattern] = self.find_possible_words(cross_pattern)
                self.CACHE_WORDS += len(self.cache[cross_pattern])
            else:
                self.CACHE_ACCESSES += 1
            res *= len(self.cache[cross_pattern])
            if res == 0:
                break
        self.crossword.set_word(move, pattern)
        return res

    def sort_by_score(self, move, words, reverse=True):
        scores = list()
        for word in words:
            scores.append((word, self.get_score(move, word)))
        #scores.sort(key=lambda x: x[1], reverse=reverse)
        return scores

    def visit_rec(self, tree, profile_stop=-1, observe=float('inf')):
        if self.VISITS == 1055:
            pass
        if self.VISITS == profile_stop:
            return True
        if self.VISITS % observe == 0:
            #self.save_tree()
            #clear_console()
            print(self.crossword)
            print()
            print("Preorder Visits:                 ", self.VISITS)
            print("Preorder Time per visit (ms):    ", ((1000000 * (time() - self.START_TIME)) // max(1, self.VISITS)) / 1000)
            print("Leaves:                          ", self.LEAVES)
            print("Cache Uses:                      ", self.CACHE_ACCESSES)
            print("Cache Keys:                      ", len(self.cache))
            print("Cache Words:                     ", self.CACHE_WORDS)
            print("Depth:                           ", self.crossword.n_moves - len(self.moves))
        self.VISITS += 1
        if not self.moves:
            print(str(self.crossword))
            self.crossword.show(self.dictionary)
            self.LEAVES += 1
            return True
        #shuffle(self.moves)
        move = self.moves.pop()
        pattern = self.crossword.get_word(move)
        if SLOW:
            print("Move: %s - %s" % (str(move), pattern))
            input("Invio per continuare_ ")
        if pattern in self.cache:
            self.CACHE_ACCESSES += 1
            words = self.cache[pattern]
        else:
            words = self.find_possible_words(pattern)
            self.cache[pattern] = words
            self.CACHE_WORDS += len(words)
        if len(words) == 0:
            self.moves.append(move)
            self.crossword.set_word(move, pattern)
            if SLOW:
                input("Back Jump begin: continue?")
            self.LEAVES += 1
            return False
        found_solution = False
        scores = self.sort_by_score(move, words, reverse=True)
        is_leave = True
        for (word, score) in scores:
            if score != 0:
                is_leave = False
                self.crossword.set_word(move, word)
                node = Tree(content=(move, word))
                tree.add_son(node)
                found_solution = self.visit_rec(node, profile_stop, observe=observe)
                if found_solution:
                    break
        self.LEAVES += 1 * is_leave
        self.moves.append(move)
        if found_solution:
            return True
        else:
            self.crossword.set_word(move, pattern)
            return False

    def visit(self, profile_stop=-1, observe=float('inf')):
        self.START_TIME = time()
        res = self.visit_rec(self.tree, profile_stop=profile_stop, observe=observe)
        self.save_tree()
        print()
        print("Visite:      ", self.VISITS)
        print("Foglie:      ", self.LEAVES)
        print("Cache Uses:  ", self.CACHE_ACCESSES)
        print("Cache Keys:  ", len(generator.cache))
        print("Cache Words: ", self.CACHE_WORDS)
        print("DURATION: %d" % (time() - self.START_TIME))
        print(generator.crossword.move_word_map)
        return res

if __name__ == "__main__":
    crossword = Crosswords(12, 8,
                           [(0, 5), (0, 7), (0, 9), (1, 2), (1, 4), (1, 2), (1, 4), (2, 3), (3, 1), (4, 0), (4, 11),
                            (5, 7), (5, 11), (6, 0), (6, 8), (6, 9), (7, 0), (7, 1), (7, 2), (7, 5)])
    print(crossword.__str__(numbers=True))
    dictionary = get_dictionary(test=True, n_words=4230, random=False)
    generator = Generator(crossword, dictionary=dictionary)
    print(generator.visit(profile_stop=-1, observe=500))



