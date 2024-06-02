
public class Cell {

        public char value;
        public boolean isBlack;
        public int number;
        public int horizontalLength;
        public int verticalLength;

        public Cell(char value, boolean isBlack, int number, int horizontalLength, int verticalLength) {
            this.value = value;
            this.isBlack = isBlack;
            this.number = number;
            this.horizontalLength = horizontalLength;
            this.verticalLength = verticalLength;
        }

        @Override
        public String toString() {
            return toString(false);
        }

        public String toString(boolean number) {
            String txt = " " + (this.isBlack ? "##" : (number && this.number != 0) ? String.valueOf(this.number) : this.value);
            txt += " ".repeat(3 - txt.length());
            return txt;
        }
}