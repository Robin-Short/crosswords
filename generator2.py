from random import randint
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
             
    def sort_words(self, words, move, desc=False):
        i, j, DIR = move.get_params()
        pattern = self.crossword.get_word(move)
        scores = dict()
        for word in words:
            self.crossword.set_word(move, word)
            score = 1
            cross_moves = [cross_move for cross_move in self.crossword.crosses[(i, j, DIR)]
                           if cross_move in self.moves]
            for cross_move in cross_moves:
                little_pattern = self.crossword.get_word(cross_move)
                if little_pattern in self.cache:
                    little_possible_words = self.cache[little_pattern]
                else:
                    little_possible_words = self.crossword.find_possible_words(self.optimized_dictionary,
                                                                               cross_move,
                                                                               optimize=True)
                    self.cache[little_pattern] = little_possible_words
                score *= len(little_possible_words)
                if not score:
                    break
            scores[word] = score
            self.crossword.set_word(move, pattern)
        words.sort(key=lambda w: scores[w], reverse=True)
        if not desc:
            words.reverse()
        return scores

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
            LEAVES += 1
            return True
        scores = dict()
        min_score, min_move, possible_words = float('inf'), None, None
        for move in self.moves:
            pattern = self.crossword.get_word(move).replace(' ', '.')
            if pattern in self.cache.keys():
                attempt_possible_words = self.cache[pattern]
                CACHE_ACCESSES += 1
            else:
                attempt_possible_words = self.crossword.find_possible_words(self.optimized_dictionary, move,
                                                                            optimize=True)
                self.cache[pattern] = attempt_possible_words
                CACHE_WORDS += len(attempt_possible_words)
            scores[move.get_params()] = len(attempt_possible_words)
            if scores[move.get_params()] < min_score:
                min_score = scores[move.get_params()]
                min_move = move
                possible_words = attempt_possible_words
        if min_score == 0:
            LEAVES += 1
            return False
        else:
            partial_word = self.crossword.get_word(min_move)
            self.moves.remove(min_move)
            scores = self.sort_words(words=possible_words, move=min_move, desc=True)
            for word in possible_words:
                if scores[word]:    # Score Boosting
                    self.crossword.set_word(min_move, word)
                    solution = self.visit()
                    if solution:
                        return True
                else:
                    LEAVES += 1
            self.moves.append(min_move)
            self.crossword.set_word(min_move, partial_word)
          
        
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
    generator.visit()
    print("DURATION: %d" % (time() - start))





