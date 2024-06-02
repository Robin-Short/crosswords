class Tree:
    def __init__(self, content=None):
        self.content = content
        self.sons = list()
        self.daddy = None

    def __str__(self):
        return str(self.content)

    def get_daddy(self):
        return self.daddy

    def set_daddy(self, daddy):
        self.daddy = daddy

    def set_content(self, content):
        self.content = content

    def add_son(self, son):
        self.sons.append(son)
        son.daddy = self

    def preorder_visit(self, depth=0):
        txt = "    " * depth + str(self)
        if self.sons == []:
            return txt
        for son in self.sons:
            txt += "\n" + son.preorder_visit(depth=depth + 1)
        return txt


if __name__ == "__main__":
    root = Tree("bella")
    root.add_son(Tree("Robin"))
    root.add_son(Tree("Gabriele"))
    root.sons[0].add_son(Tree("Ginevra"))
    root.sons[1].add_son(Tree("Spartaco"))
    root.sons[1].add_son(Tree("Grazia"))
    root.sons[1].sons[1].add_son(Tree("Graziella"))
    root.sons[1].sons[1].add_son(Tree("Gentile"))
    root.sons[0].sons[0].add_son(Tree("Vincenzo"))
    print(root.preorder_visit())







