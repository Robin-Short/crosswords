from random import randint
import re

HORIZONTAL = 0
VERTICAL = 1
chars = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'

class Move:
    def __init__(self, i, j, DIR):
        self.i = i
        self.j = j
        self.DIR = DIR

    def __str__(self):
        return str(self.get_params())

    def __repr__(self):
        return(str(self))

    def get_params(self):
        return self.i, self.j, self.DIR

    def __eq__(self, pos):
        return self.i == pos.i and self.j == pos.j and self.DIR == pos.DIR

class Cell:
    def __init__(self, value: str, is_black: bool, number, horizontal_length: int, vertical_length: int):
        self.value = value                          # ['A', 'B', ..., 'Z', '.']
        self.is_black = is_black                    # [True, False]
        self.number = number                        # [0, 1, 2, 3, ...]
        self.horizontal_length = horizontal_length  # [0, 1, 2, 3, ...]
        self.vertical_length = vertical_length      # [0, 1, 2, 3, ...]
        self.params = dict()
       
    def __str__(self, number=False):
        txt = (" " + (self.value if not number else (str(self.number)) if self.number else "_")) \
            if not self.is_black else '  '
        txt += " " * (3 - len(txt))
        return txt
        
class Crosswords:
    def __init__(self, width, height, black_indexes):
        self.width = width
        self.height = height
        self.black_indexes = black_indexes
        self.grid = list()
        self.numbers_list = list()
        self.moves_list = list()
        for i in range(self.height):
            row = list()
            for j in range(self.width):
                value = '.'
                is_black = (i, j) in self.black_indexes
                is_horizontal_number = (j == 0 or row[j-1].is_black) and not is_black
                is_horizontal_number = is_horizontal_number and not (j + 1 == self.width or (i, j + 1) in self.black_indexes)
                is_vertical_number = (i == 0 or self.grid[i-1][j].is_black) and not is_black
                is_vertical_number = is_vertical_number and not (i + 1 == self.height or (i + 1, j) in self.black_indexes)
                horizontal_length = 0
                if is_horizontal_number:
                    self.moves_list.append(Move(i, j, HORIZONTAL))
                    for jj in range(j, self.width):
                        if not (i, jj) in self.black_indexes:
                            horizontal_length += 1
                        else:
                            break
                vertical_length = 0
                if is_vertical_number:
                    self.moves_list.append(Move(i, j, VERTICAL))
                    for ii in range(i, self.height):
                        if not (ii, j) in self.black_indexes:
                            vertical_length += 1
                        else:
                            break
                if is_horizontal_number or is_vertical_number:
                    self.numbers_list.append((i, j))
                    number = len(self.numbers_list)
                else:
                    number = 0
                cell = Cell(value, is_black, number, horizontal_length, vertical_length)
                row.append(cell)
            self.grid.append(row)
        self.crosses = dict()
        self.move_word_map = dict()
        for move in self.moves_list:
            self.crosses[move.get_params()] = self.get_cross_moves(move)
            self.move_word_map[move.get_params()] = '.' * len(self.get_word_slow(move))
        self.n_moves = len(self.moves_list)
        
    def sync(self):
        for move, word in self.move_word_map.items():
            self.set_word_slow(Move(*move), word)

    def __getitem__(self, item):
        i, j = item
        return self.grid[i][j]
    
    def __str__(self, numbers=False):
        self.sync()
        txt = ''
        for i in range(self.height):
            txt += '\n' + '*---' * self.width + '*\n|'
            for j in range(self.width):
                txt += self.grid[i][j].__str__(number=numbers) + '|'
        return txt + '\n' + '*---' * self.width + '*\n'

    def show(self, dictionary):
        '''
        use only when crossword is completed!
        '''
        txt = "\nHORIZONTALS:\n"
        n = 0
        for move in self.moves_list:
            if move.DIR == HORIZONTAL:
                n += 1
                word = self.get_word(move)
                txt += "\n  %d - %s" % (n, dictionary[word] if word in dictionary else 'ERROR!')
        txt += "\n\nVERTICALS:\n"
        n = 0
        for move in self.moves_list:
            if move.DIR == VERTICAL:
                n += 1
                word = self.get_word(move)
                txt += "\n  %d - %s" % (n, dictionary[word] if word in dictionary else 'ERROR!')
        print(txt)
        return txt



    def get_cell(self, i, j):
        return self.grid[i][j]
    
    def get_nth_horizontal_indexes(self, n):
        '''
        return the i, j tuple representing the start of nth horizontal word (start counting from 1)
        '''
        curr_n = 0
        for i, j in self.numbers_list:
            if self.grid[i][j].horizontal_length > 0:
                curr_n += 1
            if n == curr_n:
                return i, j
       
    def get_nth_vertical_indexes(self, n):
        '''
        return the i, j tuple representing the start of nth vertical word (start counting from 1)
        '''
        curr_n = 0
        for i, j in self.numbers_list:
            if self.grid[i][j].vertical_length > 0:
                curr_n += 1
            if n == curr_n:
                return i, j

    def get_horizontal_word_slow(self, i, j):
        '''
        return the stringe composed by adjacency cells horizontally of word started at i, j if self.grid[i][j].horizontal_number else None
        '''
        word = ''
        for jj in range(j, j + self.grid[i][j].horizontal_length):
            word += self.grid[i][jj].value
        return word
       
    def get_vertical_word_slow(self, i, j):
        '''
        return the stringe composed by adjacency cells vertically of word started at i, j if self.grid[i][j].horizontal_number else None
        '''
        word = ''
        for ii in range(i, i + self.grid[i][j].vertical_length):
            word += self.grid[ii][j].value
        return word

    def get_word_slow(self, move):
        i, j, DIR = move.get_params()
        return self.get_horizontal_word_slow(i, j) if DIR == HORIZONTAL else self.get_vertical_word_slow(i, j)
    
    def get_word(self, move):
        return self.move_word_map[move.get_params()]
    
    def set_horizontal_word_slow(self, i, j, word):
        '''
        set horizontal word who started at i, j
        '''
        for jj in range(j, j + self.grid[i][j].horizontal_length):
            self.grid[i][jj].value = word[jj - j]
    
    def set_vertical_word_slow(self, i, j, word):
        '''
        set horizontal word who started at i, j
        '''
        for ii in range(i, i + self.grid[i][j].vertical_length):
            self.grid[ii][j].value = word[ii - i]
        return word
    
    def set_word_slow(self, move, word):
        i, j, DIR = move.get_params()
        if DIR == HORIZONTAL:
            self.set_horizontal_word_slow(i, j, word)
        elif DIR == VERTICAL:
            self.set_vertical_word_slow(i, j, word)

    def set_word(self, move, word):
        i, j, dir = move.get_params()
        self.move_word_map[(i, j, dir)] = word
        for cross_move in self.crosses[(i, j, dir)]:
            I, J, DIR = cross_move.get_params()
            k, l = abs(I-i), abs(J-j)
            if dir == HORIZONTAL:
                pass
            elif dir == VERTICAL:
                x = l
                l = k
                k = x
            ch = word[l]
            new_word = self.move_word_map[(I, J, DIR)]
            self.move_word_map[(I, J, DIR)] = new_word[:k] + ch + new_word[k+1:]
    
    def del_horizontal_word_slow(self, i, j):
        word = ' ' * self.grid[i][j].horizontal_length
        self.set_horizontal_word_slow(i, j, word)
       
    def del_vertical_word_slow(self, i, j):
        word = ' ' * self.grid[i][j].vertical_length
        self.set_vertical_word_slow(i, j, word)
        
    def find_possible_horizontal_words_slow(self, dictionary, i, j, optimize=False):
        pattern = self.get_horizontal_word_slow(i, j).replace(' ', '.')
        res = []
        
        # Precompilare il pattern per evitare di compilarlo ad ogni iterazione
        pattern_re = re.compile(pattern)
        
        # Usare una struttura dati più efficiente per la ricerca (es. set)
        if optimize:
            iterable = dictionary.get(len(pattern), [])
        else:
            iterable = dictionary.keys()
        
        for word in iterable:
            if pattern_re.fullmatch(word):
                res.append(word)
        return res
    
    def find_possible_vertical_words_slow(self, dictionary, i, j, optimize=False):
        pattern = self.get_vertical_word_slow(i, j).replace(' ', '.')
        res = []
        
        # Precompilare il pattern per evitare di compilarlo ad ogni iterazione
        pattern_re = re.compile(pattern)
        
        # Usare una struttura dati più efficiente per la ricerca (es. set)
        iterable = dictionary.keys() if not optimize else dictionary[len(pattern)]
        for word in iterable:
            if pattern_re.fullmatch(word):
                res.append(word)
        return res
    
    def find_possible_words_slow(self, dictionary, move, optimize=False):
        i, j, DIR = move.get_params()
        if DIR == HORIZONTAL:
            return self.find_possible_horizontal_words_slow(dictionary, i, j, optimize)
        elif DIR == VERTICAL:
            return self.find_possible_vertical_words_slow(dictionary, i, j, optimize)

    def find_possible_words(self, dictionary, move, optimize=False):
        pattern = self.get_word(move).replace(' ', '.')
        res = []
        # Precompilare il pattern per evitare di compilarlo ad ogni iterazione
        pattern_re = re.compile(pattern)
        # Usare una struttura dati più efficiente per la ricerca (es. set)
        iterable = dictionary.keys() if not optimize else dictionary[len(pattern)]
        for word in iterable:
            if pattern_re.fullmatch(word):
                res.append(word)
        return res

    def get_horizontal_cross_moves(self, i, j):
        positions = [(i, j + jj) for jj in range(self.grid[i][j].horizontal_length)]
        cross_moves = []
        for move in self.moves_list:
            I, J, DIR = move.get_params()
            ok = False
            if DIR == VERTICAL:
                for ii in range(self.grid[I][J].vertical_length):
                    if (I + ii, J) in positions:
                        ok = True
                        break
                if ok:
                    cross_moves.append(move)
        return cross_moves

    def get_vertical_cross_moves(self, i, j):
        positions = [(i + ii, j) for ii in range(self.grid[i][j].vertical_length)]
        cross_moves = []
        for move in self.moves_list:
            I, J, DIR = move.get_params()
            ok = False
            if DIR == HORIZONTAL:
                for jj in range(self.grid[I][J].horizontal_length):
                    if (I, J + jj) in positions:
                        ok = True
                        break
                if ok:
                    cross_moves.append(move)
        return cross_moves

    def get_cross_moves(self, move):
        i, j, DIR = move.get_params()
        if DIR == HORIZONTAL:
            return self.get_horizontal_cross_moves(i, j)
        elif DIR == VERTICAL:
            return self.get_vertical_cross_moves(i, j)

       
    def is_completed_horizontal_word(self, i, j):
        '''
        return if horizontal word started at i, j is completed or not
        '''
        for jj in range(j, j + self.grid[i][j].horizontal_length):
            if self.grid[i][jj].value == ' ' and not self.grid[i][j].is_black:
                return False
        return True
        
    def is_completed_vertical_word(self, i, j):
        '''
        return if vertical word started at i, j is completed or not
        '''
        for ii in range(i, i + self.grid[i][j].vertical_length):
            if self.grid[ii][j].value == ' ' and not self.grid[i][j].is_black:
                return False
        return True

    def is_completed_word(self, move):
        return not '.' in self.move_word_map[move.get_params()]
    
    def fill_random(self):
       for i in range(self.height):
           for j in range(self.width):
               if self.grid[i][j].value == ' ' and not self.grid[i][j].is_black:
                   self.grid[i][j].value = chars[randint(0, len(chars) - 1)]
           
    def is_filled(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].value == ' ' and not self.grid[i][j].is_black:
                    return False
        return True
        
    def loss_horizontal(self, dictionary):
        loss = 0
        for (i, j) in self.numbers_list:
            word = self.get_horizontal_word(i, j)
            if self.grid[i][j].horizontal_length > 0 and not word in dictionary:
                loss += 1
        return loss
    
    def loss_vertical(self, dictionary):
        loss = 0
        for (i, j) in self.numbers_list:
            word = self.get_vertical_word(i, j)
            if self.grid[i][j].vertical_length > 0 and not word in dictionary:
                loss += 1
        return loss
    
    def loss(self, dictionary):
        return self.loss_horizontal(dictionary) + self.loss_vertical(dictionary)
    
if __name__ == "__main__":
    crossword = Crosswords(5, 5, [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)])
    print(crossword)
    print(crossword.__str__(numbers=True))
    crossword.fill_random()
    print(crossword)
    print(crossword.__str__(numbers=True))
    
