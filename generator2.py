from random import shuffle
from crosswords import Move, Crosswords, HORIZONTAL, VERTICAL
from matplotlib import pyplot as plt
from dictionary import dictionary
from time import time

VISITS = 0
LEAVES = 0
CACHE_ACCESSES = 0
CACHE_WORDS = 0

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
    def __init__(self, crossword, dictionary):
        self.crossword = crossword
        self.dictionary = dictionary
        self.moves = []
        for i, j in self.crossword.numbers_list:
            if self.crossword[i, j].horizontal_length > 0:
                self.moves.append(Move(i, j, HORIZONTAL))
            if self.crossword[i, j].vertical_length > 0:
                self.moves.append(Move(i, j, VERTICAL))
        self.cache = dict()
        self.optimized_dictionary = self.get_optimized_dictionary()
       
    def get_optimized_dictionary(self):
        res = dict()
        for word in self.dictionary.keys():
            n = len(word)
            if n in res:
                res[n].append(word)
            else:
                res[n] = [word]
        return res

    def visit(self):
        global VISITS, LEAVES, CACHE_ACCESSES, CACHE_WORDS
        VISITS += 1
        print("\nVisite:      ", VISITS)
        print("Foglie:      ", LEAVES)
        print("Cache Uses:  ", CACHE_ACCESSES)
        print("Cache Keys:  ", len(self.cache))
        print("Cache Words: ", CACHE_WORDS)
        if not self.moves:
            print(self.crossword)
            return True
        shuffle(self.moves)
        move = self.moves.pop()
        print(move)
        pattern = self.crossword.get_word(move)
        if pattern in self.cache:
            words = self.cache[pattern]
        else:
            words = self.crossword.find_possible_words(self.optimized_dictionary, move, optimize=True)
            self.cache[pattern] = words
        if not words:
            self.moves.append(move)
            self.crossword.set_word(move, pattern)
            return False
        else:
            found_solution = False
            for word in words:
                self.crossword.set_word(move, word)
                if self.visit():
                    found_solution = True
                    break
            self.moves.append(move)
            if found_solution:
                return True
            else:
                self.crossword.set_word(move, pattern)
                return False
          
        
if __name__ == "__main__":
    crossword = Crosswords(15, 15,
                           [(0, 4), (0, 10),
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
                            ])
    print(crossword.__str__(numbers=True))
    generator = Generator(crossword, dictionary)
    start = time()
    print(generator.visit())
    print("DURATION: %d" % (time() - start))





