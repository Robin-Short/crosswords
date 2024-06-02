import java.util.*;
import java.util.regex.Pattern;

public class Crosswords {
    public static final int HORIZONTAL = 0;
    public static final int VERTICAL = 1;
    private final int width;
    private final int height;
    public List<Pos> blackPositions;
    public final Cell[][] grid;
    public List<int[]> numbersList;

    public Crosswords(int width, int height, List<Pos> blackPositions) {
        this.width = width;
        this.height = height;
        this.blackPositions = blackPositions;
        this.grid = new Cell[width][height];
        this.numbersList = new ArrayList<>();

        for (int i = 0; i < height; i++) {
            Cell[] row = new Cell[width];
            for (int j = 0; j < width; j++) {
                boolean isBlack = blackPositions.contains(new Pos(i, j));
                boolean isHorizontalNumber = (j == 0 || row[j-1].isBlack) && !isBlack && !((j + 1 == width) || blackPositions.contains(new Pos(i, j+1)));
                boolean isVerticalNumber = (i == 0 || getCell(i - 1, j).isBlack) && !isBlack && !((i + 1 == height) || blackPositions.contains(new Pos(i+1, j)));
                int horizontalLength = 0;
                if (isHorizontalNumber) {
                    for (int jj = j; jj < width; jj++) {
                        if (!blackPositions.contains(new Pos(i, jj))) {
                            horizontalLength++;
                        } else {
                            break;
                        }
                    }
                }
                int verticalLength = 0;
                if (isVerticalNumber) {
                    for (int ii = i; ii < height; ii++) {
                        if (!blackPositions.contains(new Pos(ii, j))) {
                            verticalLength++;
                        } else {
                            break;
                        }
                    }
                }
                int number = 0;
                if (isHorizontalNumber || isVerticalNumber) {
                    numbersList.add(new int[]{i, j});
                    number = numbersList.size();
                }
                row[j] = new Cell(' ', isBlack, number, horizontalLength, verticalLength);
            }
            grid[i] = row;
        }
    }

    public Cell getCell(int i, int j) {
        return grid[i][j];
    }

    @Override
    public String toString() {
        return toString(false);
    }

    public String toString(boolean numbers) {
        StringBuilder txt = new StringBuilder();
        for (int i = 0; i < height; i++) {
            txt.append("\n").append("*---".repeat(width)).append("*\n|");
            for (int j = 0; j < width; j++) {
                txt.append(getCell(i, j).toString(numbers)).append("|");
            }
        }
        return txt.append("\n").append("*---".repeat(width)).append("*\n").toString();
    }

    public String getHorizontalWord(int i, int j) {
        assert(grid[i][j].horizontalLength > 0 && grid[i][j].number != 0);
        StringBuilder word = new StringBuilder();
        for (int jj = j; jj < j + getCell(i, j).horizontalLength; jj++) {
            word.append(getCell(i, jj).value);
        }
        return word.toString();
    }

    public String getVerticalWord(int i, int j) {
        assert(grid[i][j].verticalLength > 0 && grid[i][j].number != 0);
        StringBuilder word = new StringBuilder();
        for (int ii = i; ii < i + getCell(i, j).verticalLength; ii++) {
            word.append(getCell(ii, j).value);
        }
        return word.toString();
    }

    public String getWord(int i, int j, int DIR) {
        return DIR == HORIZONTAL ? getHorizontalWord(i, j) : getVerticalWord(i, j);
    }

    public void setHorizontalWord(int i, int j, String word) {
        assert(grid[i][j].horizontalLength > 0 && grid[i][j].number != 0);
        for (int jj = j; jj < j + getCell(i, j).horizontalLength; jj++) {
            getCell(i, jj).value = word.charAt(jj - j);
        }
    }

    public void setVerticalWord(int i, int j, String word) {
        assert(grid[i][j].verticalLength > 0 && grid[i][j].number != 0);
        for (int ii = i; ii < i + getCell(i, j).verticalLength; ii++) {
            getCell(ii, j).value = word.charAt(ii - i);
        }
    }

    public void setWord(int i, int j, int DIR, String word) {
        if (DIR == HORIZONTAL) {
            setHorizontalWord(i, j, word);
        } else if (DIR == VERTICAL) {
            setVerticalWord(i, j, word);
        }
    }

    public void delHorizontalWord(int i, int j) {
        String word = " ".repeat(getCell(i, j).horizontalLength);
        setHorizontalWord(i, j, word);
    }

    public void delVerticalWord(int i, int j) {
        String word = " ".repeat(getCell(i, j).verticalLength);
        setVerticalWord(i, j, word);
    }

    public List<String> findPossibleHorizontalWords(Map<Integer, List<String>> dictionary, int i, int j) {
        //TODO: eliminare il replace
        String pattern = getHorizontalWord(i, j).replace(" ", ".");
        List<String> res = new ArrayList<>();
        for (String word : dictionary.get(grid[i][j].horizontalLength)) {
            if (Pattern.matches(pattern, word)) {
                res.add(word);
            }
        }
        return res;
    }

    public List<String> findPossibleVerticalWords(Map<Integer, List<String>> dictionary, int i, int j) {
        //TODO: eliminare il replace
        String pattern = getVerticalWord(i, j).replace(" ", ".");
        List<String> res = new ArrayList<>();
        for (String word : dictionary.get(grid[i][j].verticalLength)) {
            if (Pattern.matches(pattern, word)) {
                res.add(word);
            }
        }
        return res;
    }

    public List<String> findPossibleWords(Map<Integer, List<String>> dictionary, int i, int j, int DIR) {
        return DIR == HORIZONTAL ? findPossibleHorizontalWords(dictionary, i, j) : findPossibleVerticalWords(dictionary, i, j);
    }


    public static void main(String[] args) {
        List<Pos> blackPositions = Arrays.asList(
                new Pos(0, 5), new Pos(0, 7), new Pos(0, 9),
                new Pos(1, 2), new Pos(1, 4), new Pos(1, 2),
                new Pos(1, 4), new Pos(2, 3), new Pos(3, 1),
                new Pos(4, 0), new Pos(4, 11), new Pos(5, 7),
                new Pos(5, 11), new Pos(6, 0), new Pos(6, 8),
                new Pos(6, 9), new Pos(7, 0), new Pos(7, 1),
                new Pos(7, 2), new Pos(7, 5)
        );

        Crosswords crossword = new Crosswords(12, 8, blackPositions);
        System.out.println(crossword);
    }

}