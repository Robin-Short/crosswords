import numpy as np

class Cell:
    def __init__(self, value: str, is_black: bool, horizontal_number: int, vertical_number: int,
                 horizontal_length: int, vertical_length: int):
        self.value = value                          # ['a', 'b', ..., 'z', '0']
        self.is_black = is_black                    # [True, False]
        self.horizontal_number = horizontal_number  # [0, 1, 2, 3, ...]
        self.vertical_number = vertical_number      # [0, 1, 2, 3, ...]
        self.horizontal_length = horizontal_length  # [0, 1, 2, 3, ...]
        self.vertical_length = vertical_length      # [0, 1, 2, 3, ...]
       
    def __str__(self):
        pass
        
class Crosswords:
    def __init__(self, width, height, black_indexes):
        self.width = width
        self.height = height
        self.black_indexes = black_indexes
        self.grid = list()
        self.numbers_list = list()
        for i in range(self.height):
            row = list()
            for j in range(self.width):
                value = '0'
                is_black = (i, j) in self.black_indexes
                horizontal_number = (j == 0 or row[j-1].is_black) and not is_black
                vertical_number = (i == 0 or self.grid[-1][j].is_black) and not is_black
                horizontal_length = 0
                if horizontal_number:
                    for jj in range(j, self.width):
                        if not (i, jj) in self.black_indexes:
                            horizontal_number += 1
                        else:
                            break
                vertical_length = 0
                if vertical_number:
                    for ii in range(i, self.height):
                        if not (ii, j) in self.black_indexes:
                            vertical_number += 1
                        else:
                            break
                if horizontal_number or vertical_number:
                    self.numbers_list.append(i, j)
                cell = Cell(value, is_black, horizontal_number, vertical_number, horizontal_length, vertical_length)
                row.append(cell)
            self.grid.append(row)
    
    def __getitem__(self, item):
        i, j = item
        return self.grid[i][j]
    
    def __str__(self):
        txt = ''
        for i in range(self.height):
            txt += '\n|'
            for i in range(self.width):
                if self[i, j] == -1:
                    txt += '# |'
                elif self[i, j] == 0:
                    if numbers:
                        content = str(self.get_number(i, j)) if self.is_number(i, j) else ' '
                        txt += content + (" " if len(content) == 1 else "") + '|'
                    else:
                        txt += '  |'
                else:
                    if numbers:
                        content = str(self.get_number(i, j)) if self.is_number(i, j) else ' '
                        txt += content + (" " if len(content) == 1 else "") + '|'
                    else:
                        txt += chr(int(self[i, j])) + ' |'
        return txt
    
    def get_cell(self, i, j):
        return self[i][j]
    
    def get_nth_horizontal_indexes(self, n):
        '''
        return the i, j tuple representing the start of nth horizontal word
        '''
       
    def get_nth_vertical_indexes(self, n):
        '''
        return the i, j tuple representing the start of nth vertical word
        '''
    
    def get_horizontal_word(self, i, j):
        '''
        return the stringe composed by adjacency cells horizontally of word started at i, j if self[i][j].horizontal_number else None
        '''
       
    def get_vertical_word(self, i, j):
        '''
        return the stringe composed by adjacency cells vertically of word started at i, j if self[i][j].horizontal_number else None
        '''
    
    def get_horizontal_cells(self, i, j):
        '''
        return the list of adjacency cells horizontally of word started at i, j if self[i][j].horizontal_number else None
        '''
    
    def get_vertical_cells(self, i, j):
        '''
        return the list of adjacency cells vertically of word started at i, j if self[i][j].horizontal_number else None
        '''
    
    def set_horizontal_word(self, i, j, word):
        '''
        set horizontal word who started at i, j
        '''
    
    def set_vertical_word(self, i, j, word):
        '''
        set horizontal word who started at i, j
        '''
       
    def is_completed_horizontal_word(self, i, j):
        '''
        return if horizontal word started at i, j is completed or not
        '''
       
    def is_completed_vertical_word(self, i, j):
        '''
        return if vertical word started at i, j is completed or not
        '''
       
    def is_filled(self):
        pass
        
    def loss_horizontal(self):
        pass
    
    def loss_vertical(self):
        pass
    
    def loss(self):
        pass
    
'''class CrossWords:
    def __init__(self, width, height, black_indexes):
        self.width = width
        self.height = height
        self.black_indexes = black_indexes
        self.matrix = None
        self.start_w_list = []
        self.start_h_list = []

    def __getitem__(self, *args):
        return self.matrix.__getitem__(*args)

    def __setitem__(self, *args):
        return self.matrix.__setitem__(*args)

    def __str__(self, numbers=False):
        txt = ''
        for j in range(self.height):
            txt += '\n|'
            for i in range(self.width):
                if self[i, j] == -1:
                    txt += '# |'
                elif self[i, j] == 0:
                    if numbers:
                        content = str(self.get_number(i, j)) if self.is_number(i, j) else ' '
                        txt += content + (" " if len(content) == 1 else "") + '|'
                    else:
                        txt += '  |'
                else:
                    if numbers:
                        content = str(self.get_number(i, j)) if self.is_number(i, j) else ' '
                        txt += content + (" " if len(content) == 1 else "") + '|'
                    else:
                        txt += chr(int(self[i, j])) + ' |'
        return txt

    def get_index(self, i, j):
        return self.width * i + j

    def get_indexes(self, k):
        return k % self.width, k // self.width

    def start_w(self, i, j=None):
        if j is None:
            i, j = self.get_indexes(i)
        return (i, j) in self.start_w_list

    def start_h(self, i, j=None):
        if j is None:
            i, j = self.get_indexes(i)
        return (i, j) in self.start_h_list

    def len_w(self, i, j=None):
        if self.start_w(i, j):
            w = 1
            while i + w < self.width:
                if not self[i + w, j] == -1:
                    w += 1
                else:
                    break
            return w
        return None

    def len_h(self, i, j=None):
        if self.start_h(i, j):
            w = 1
            while j + w < self.height:
                if not self[i, j + w] == -1:
                    w += 1
                else:
                    break
            return w
        return None

    def is_number(self, i, j=None):
        if j is None:
            i, j = self.get_indexes(i)
        return not self[i][j] == -1 and (self.start_w(i, j) or self.start_h(i, j))

    def get_number(self, i, j=None):
        if j is None:
            i, j = self.get_indexes(i)
        count = 0
        for m in range(self.height):
            for l in range(self.width):
                if self.is_number(l, m):
                    count += 1
                    if l == i and m == j:
                        return count
        return None

    def build(self):
        self.matrix = np.zeros((self.width, self.height), dtype=int)
        # Insert black cells
        for index in self.black_indexes:
            if isinstance(index, tuple):
                i, j = index
            else:
                i, j = self.get_indexes(index)
            self.matrix[i][j] = -1
        for i in range(self.width):
            for j in range(self.height):
                if not i or self[i - 1, j] == -1:
                    self.start_w_list.append((i, j))
                if not j or self[i, j - 1] == -1:
                    self.start_h_list.append((i, j))
            
    


if __name__ == "__main__":
    crosswords = CrossWords(10, 5, [6, 15, 24, 33, 42])
    crosswords.build()
    print(crosswords.__str__(numbers=True))
    txt = ''
    for j in range(crosswords.height):
        txt += '\n|'
        for i in range(crosswords.width):
            len_w = crosswords.len_w(i, j)
            txt += ' ' + (str(len_w) if len_w else ' ') + '|'
    print(txt)
    txt = ''
    for j in range(crosswords.height):
        txt += '\n|'
        for i in range(crosswords.width):
            len_h = crosswords.len_h(i, j)
            txt += ' ' + (str(len_h) if len_h else ' ') + '|'
    print(txt)'''
