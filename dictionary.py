with open("dict_test.txt", "r") as file:
    words = file.readlines()

dictionary = {word[:-1].upper(): "definizione a caso" for word in words}
length = [len(word[-1]) for word in words]