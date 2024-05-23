from random import randint
from crosswords import Crosswords
from matplotlib import pyplot as plt
from dictionary import dictionary

HORIZONTAL = 0
VERTICAL = 1
EPOCHS = 10000

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

class Filler:
    def __init__(self, crossword, dictionary, direction=HORIZONTAL):
        self.crossword = crossword
        self.dictionary = dictionary
        self.direction = direction
        if direction == HORIZONTAL:
            self.numbers_list = [(i, j) for (i, j) in crossword.numbers_list if crossword[i, j].horizontal_length > 0]
        elif direction == VERTICAL:
            self.numbers_list = [(i, j) for (i, j) in crossword.numbers_list if crossword[i, j].vertical_length > 0]

    def get_loss(self):
        if self.direction == HORIZONTAL:
            return self.crossword.loss_horizontal(self.dictionary)
        elif self.direction == VERTICAL:
            return self.crossword.loss_vertical(self.dictionary)

    def get_word(self, i, j):
        if self.direction == HORIZONTAL:
            return self.crossword.get_horizontal_word(i, j)
        elif self.direction == VERTICAL:
            return self.crossword.get_vertical_word(i, j)

    def set_word(self, i, j, word):
        if self.direction == HORIZONTAL:
            self.crossword.set_horizontal_word(i, j, word)
        elif self.direction == VERTICAL:
            self.crossword.set_vertical_word(i, j, word)

    def move(self):
        choice = randint(0, len(self.numbers_list) - 1)
        i, j = self.numbers_list[choice]
        word1 = self.get_word(i, j)
        word2 = most_similar_word(word1, self.dictionary)
        self.set_word(i, j, word2)


class WFiller(Filler):
    def __init__(self, crossword, dictionary):
        super().__init__(crossword=crossword, dictionary=dictionary, direction=HORIZONTAL)


class HFiller(Filler):
    def __init__(self, crossword, dictionary):
        super().__init__(crossword=crossword, dictionary=dictionary, direction=VERTICAL)

class Generator:
    def __init__(self, crossword, dictionary):
        self.crossword = crossword
        self.w_filler = WFiller(crossword, dictionary)
        self.h_filler = HFiller(crossword, dictionary)
        self.losses = []

    def train(self):
        self.losses = []
        self.crossword.fill_random()
        epoch = 0
        w_loss = self.w_filler.get_loss()
        h_loss = self.h_filler.get_loss()
        while epoch < EPOCHS and w_loss + h_loss > 0:
            epoch += 1
            if w_loss > h_loss:
                self.w_filler.move()
            else:
                self.h_filler.move()
            w_loss = self.w_filler.get_loss()
            h_loss = self.h_filler.get_loss()
            ######
            self.losses.append(self.crossword.loss(dictionary))
            #print("Loss, WLoss, HLoss:", self.losses[-1], w_loss, h_loss)
        print("LOSS: ", self.losses[-1])
        print(self.crossword)
        return self.losses

if __name__ == "__main__":
    crossword = Crosswords(14, 10, [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)])
    generator = Generator(crossword, dictionary)
    losses = generator.train()
    plt.plot(losses)
    plt.plot([0, len(losses)], [0, 0], 'g-')
    plt.show()





