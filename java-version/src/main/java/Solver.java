import java.util.*;

public class Solver {
    private final Crosswords crossword;
    private final List<Move> moves;
    private final Map<String, List<String>> cache;
    private final Map<Integer, List<String>> dictionary;

    public Solver(Crosswords crossword, List<String> dictionary) {
        this.crossword = crossword;
        this.cache = new HashMap<>();
        this.dictionary = getOptimizedDictionary(dictionary);
        this.moves = new ArrayList<>();

        for (int[] pos : this.crossword.numbersList) {
            int i = pos[0];
            int j = pos[1];
            if (crossword.getCell(i, j).horizontalLength > 0) {
                this.moves.add(new Move(i, j, Crosswords.HORIZONTAL));
            }
            if (crossword.getCell(i, j).verticalLength > 0) {
                this.moves.add(new Move(i, j, Crosswords.VERTICAL));
            }
        }
    }

    private Map<Integer, List<String>> getOptimizedDictionary(List<String> dictionary) {
        Map<Integer, List<String>> optimizedDict = new HashMap<>();
        for (String word : dictionary) {
            int length = word.length();
            if (!optimizedDict.containsKey(length)) {
                optimizedDict.put(length, new ArrayList<>());
            }
            optimizedDict.get(length).add(word);
        }
        return optimizedDict;
    }


    public boolean visit() {
        Optional<Move> moveOpt = moves.stream().filter(m -> !m.removed).findAny();
        if (moveOpt.isEmpty()) {
            System.out.println("Solution found!");
            System.out.println(this.crossword);
            return true;
        }
        Move move = moveOpt.get();
        String partialWord = crossword.getWord(move.i, move.j, move.direction);
        List<String> possibleWords;
        if (cache.containsKey(partialWord)) {
            possibleWords = cache.get(partialWord);
        } else {
            possibleWords = crossword.findPossibleWords(dictionary, move.i, move.j, move.direction);
            cache.put(partialWord, possibleWords);
        }
        if (possibleWords.isEmpty()) {
            return false;
        }
        move.removed = true;
        for (String word : possibleWords) {
            crossword.setWord(move.i, move.j, move.direction, word);
            boolean solution = visit();
            if (solution) {
                return true;
            }
        }
        move.removed = false;
        crossword.setWord(move.i, move.j, move.direction, partialWord);
        return false;
    }


}
