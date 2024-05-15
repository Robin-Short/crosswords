import numpy as np

class CrossWords:
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
    print(txt)
