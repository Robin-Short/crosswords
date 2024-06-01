import json
from random import sample

print(">> Loading Dictionary")
# Specifica il percorso del file JSON
percorso_file_json = 'words.json'

# Apri il file JSON e carica il contenuto in una variabile dizionario
with open(percorso_file_json, 'r', encoding="utf8") as file:
    full_dictionary = json.load(file)

dictionary = {item['word']: sample(item['definitions'], 1)[0] for item in full_dictionary if item['definitions']}
print("Founded dictionary with %d words. \nHead:" % len(dictionary))
for i, (word, definition) in enumerate(dictionary.items()):
    if i < 20:
        print("    %s: %s" % (word, definition))