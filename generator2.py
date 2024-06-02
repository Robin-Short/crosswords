from random import shuffle
from crosswords import Move, Crosswords, HORIZONTAL, VERTICAL
from dictionary import dictionary
from tree import Tree
from time import time
import os

SLOW = False

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

VISITS = 0
LEAVES = 0
CACHE_ACCESSES = 0
CACHE_WORDS = 0
BACK_JUMP = 0


TREE = Tree()

def word_distance(word1, word2):
    if len(word1) != len(word2):
        return float('inf')
    word1 = word1.encode('utf-8')
    word2 = word2.encode('utf-8')
    # Trova gli indici in cui i caratteri sono diversi utilizzando XOR
    differing_indices = [i for i in range(len(word1)) if word1[i] ^ word2[i]]
    return len(differing_indices)

def most_similar_word(word1, dictionary):
    most_similar = None
    dist = word_distance(word1, '')
    for word, _ in dictionary.items():
        curr_dist = word_distance(word1, word)
        if curr_dist < dist:
            most_similar = word
            dist = curr_dist
    if most_similar is None:
        pass
    return most_similar


class Generator:
    def __init__(self, crossword, dictionary, back_jump=False):
        self.crossword = crossword
        self.dictionary = dictionary
        self.moves = []
        for i, j in self.crossword.numbers_list:
            if self.crossword[i, j].horizontal_length > 0:
                self.moves.append(Move(i, j, HORIZONTAL))
            if self.crossword[i, j].vertical_length > 0:
                self.moves.append(Move(i, j, VERTICAL))
        self.moves.sort(key=lambda x: len(self.crossword.get_word(x)))
        self.cache = dict()
        self.back_jump = back_jump
        self.optimized_dictionary = self.get_optimized_dictionary()
        self.tree = Tree(content=(None, None))

    def save_tree(self, filename="tree.txt"):
        with open(filename, "w") as file:
            file.write(self.tree.preorder_visit())

    def get_optimized_dictionary(self):
        res = dict()
        for word in self.dictionary.keys():
            n = len(word)
            if n in res:
                res[n].append(word)
            else:
                res[n] = [word]
        for n in range(2, 16):
            if not n in res:
                raise ValueError("Non ci sono parole lunghe %d" % n)
        return res
    
    def check_pruning(self, move):
        global CACHE_ACCESSES, CACHE_WORDS
        for m in self.crossword.crosses[move.get_params()]:
            pattern = self.crossword.get_word(m)
            if not pattern in self.cache:
                self.cache[pattern] = self.crossword.find_possible_words(self.optimized_dictionary, m, optimize=True)
                CACHE_WORDS += len(self.cache[pattern])
            else:
                CACHE_ACCESSES += 1
            if len(self.cache[pattern]) == 0:
                return True
        return False

    def get_score(self, move, word):
        global CACHE_ACCESSES, CACHE_WORDS
        res = 1
        pattern = self.crossword.get_word(move)
        self.crossword.set_word(move, word)
        for m in self.crossword.crosses[move.get_params()]:
            cross_pattern = self.crossword.get_word(m)
            if not cross_pattern in self.cache:
                self.cache[cross_pattern] = self.crossword.find_possible_words(self.optimized_dictionary, m, optimize=True)
                CACHE_WORDS += len(self.cache[cross_pattern])
            else:
                CACHE_ACCESSES += 1
            res *= len(self.cache[cross_pattern])
            if res == 0:
                break
        self.crossword.set_word(move, pattern)
        return res

    def sort_by_score(self, move, words, reverse=True):
        scores = dict()
        for word in words:
            scores[word] = self.get_score(move, word)
        words.sort(key=lambda x: scores[x], reverse=reverse)
        return scores


    def visit(self, tree):
        global VISITS, LEAVES, CACHE_ACCESSES, CACHE_WORDS, BACK_JUMP, SLOW
        if VISITS % 10000 == 0:
            #self.save_tree()
            #clear_console()
            print(self.crossword)
            print()
            print("Visits:              ", VISITS)
            print("Leaves:              ", LEAVES)
            print("Cache Uses:          ", CACHE_ACCESSES)
            print("Cache Keys:          ", len(self.cache))
            print("Cache Words:         ", CACHE_WORDS)
            print("Back Jumps:          ", BACK_JUMP)
            print("Depth:               ", self.crossword.n_moves - len(self.moves))
            #return True, None
        VISITS += 1
        if not self.moves:
            print(str(self.crossword))
            self.crossword.show(self.dictionary)
            LEAVES += 1
            return True, None
        #shuffle(self.moves)
        move = self.moves.pop()
        pattern = self.crossword.get_word(move)
        if SLOW:
            print("Move: %s - %s" % (str(move), pattern))
            input("Invio per continuare_ ")
        if pattern in self.cache:
            CACHE_ACCESSES += 1
            words = self.cache[pattern]
        else:
            words = self.crossword.find_possible_words(self.optimized_dictionary, move, optimize=True)
            self.cache[pattern] = words
            CACHE_WORDS += len(words)
        if len(words) == 0:
            self.moves.append(move)
            self.crossword.set_word(move, pattern)
            #print(move)
            if SLOW:
                input("Back Jump begin: continue?")
            return False, move
        found_solution = False
        scores = self.sort_by_score(move, words)
        for word in words:
            if scores[word] != 0:
                self.crossword.set_word(move, word)
                node = Tree(content=(move, word))
                tree.add_son(node)
                found_solution, children_move = self.visit(node)
                # BACK JUMP CONDITION
                if self.back_jump:
                    if not children_move is None:
                        if not children_move in self.crossword.crosses[move.get_params()]:
                            BACK_JUMP += 1
                            self.moves.append(move)
                            self.crossword.set_word(move, pattern)
                            return found_solution, children_move
                if found_solution:
                    break
        self.moves.append(move)
        if found_solution:
            return True, None
        else:
            self.crossword.set_word(move, pattern)
            LEAVES += 1
            return False, None


if __name__ == "__main__":
    crossword = Crosswords(12, 8,
                           [(0, 5), (0, 7), (0, 9), (1, 2), (1, 4), (1, 2), (1, 4), (2, 3), (3, 1), (4, 0), (4, 11),
                            (5, 7), (5, 11), (6, 0), (6, 8), (6, 9), (7, 0), (7, 1), (7, 2), (7, 5)])
    print(crossword.__str__(numbers=True))
    generator = Generator(crossword, dictionary, back_jump=False)
    start = time()
    print(generator.visit(generator.tree))
    generator.save_tree()
    print("\nVisite:      ", VISITS)
    print("Foglie:      ", LEAVES)
    print("Cache Uses:  ", CACHE_ACCESSES)
    print("Cache Keys:  ", len(generator.cache))
    print("Cache Words: ", CACHE_WORDS)
    print("Back Jumps: ", BACK_JUMP)
    print("DURATION: %d" % (time() - start))
    print(generator.crossword.move_word_map)

