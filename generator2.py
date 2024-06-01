from random import shuffle
from crosswords import Move, Crosswords, HORIZONTAL, VERTICAL
from matplotlib import pyplot as plt
from dictionary import dictionary
from time import time

VISITS = 0
LEAVES = 0
CACHE_ACCESSES = 0
CACHE_WORDS = 0
BACK_JUMP = 0

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

    def visit(self):
        global VISITS, LEAVES, CACHE_ACCESSES, CACHE_WORDS, BACK_JUMP
        VISITS += 1
        print("\nVisite:      ", VISITS)
        print("Foglie:      ", LEAVES)
        print("Cache Uses:  ", CACHE_ACCESSES)
        print("Cache Keys:  ", len(self.cache))
        print("Cache Words: ", CACHE_WORDS)
        print("Back Jumps:  ", BACK_JUMP)
        print(self.crossword)
        if not self.moves:
            print(self.crossword.__str__(numbers=True))
            self.crossword.show(self.dictionary)
            LEAVES += 1
            return True, None
        #shuffle(self.moves)
        move = self.moves.pop()
        pattern = self.crossword.get_word(move)
        if pattern in self.cache:
            CACHE_ACCESSES += 1
            words = self.cache[pattern]
        else:
            words = self.crossword.find_possible_words(self.optimized_dictionary, move, optimize=True)
            self.cache[pattern] = words
            CACHE_WORDS += len(words)
        if not words:
            self.moves.append(move)
            self.crossword.set_word(move, pattern)
            LEAVES += 1
            # BACK JUMP ORIGIN
            return False, move
        else:
            found_solution = False
            for word in words:
                self.crossword.set_word(move, word)
                found_solution, children_move = self.visit()
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
                return False, None


if __name__ == "__main__":
    crossword = Crosswords(12, 8,
                           [(0, 5), (0, 7), (0, 9), (1, 2), (1, 4), (1, 2), (1, 4), (2, 3), (3, 1), (4, 0), (4, 11),
                            (5, 7), (5, 11), (6, 0), (6, 8), (6, 9), (7, 0), (7, 1), (7, 2), (7, 5)])
    print(crossword.__str__(numbers=True))
    generator = Generator(crossword, dictionary, back_jump=True)
    start = time()
    print(generator.visit())
    print("\nVisite:      ", VISITS)
    print("Foglie:      ", LEAVES)
    print("Cache Uses:  ", CACHE_ACCESSES)
    print("Cache Keys:  ", len(generator.cache))
    print("Cache Words: ", CACHE_WORDS)
    print("Back Jumps: ", BACK_JUMP)
    print("DURATION: %d" % (time() - start))





