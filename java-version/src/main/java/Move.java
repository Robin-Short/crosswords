import java.util.Objects;

public class Move {
    public int i;
    public int j;
    public int direction;
    public boolean removed;

    public Move(int i, int j, int direction) {
        this.i = i;
        this.j = j;
        this.direction = direction;
        this.removed = false;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Move move = (Move) o;
        return i == move.i && j == move.j && direction == move.direction;
    }

    @Override
    public int hashCode() {
        return Objects.hash(i, j, direction);
    }

    @Override
    public String toString() {
        return "Move{" +
                "i=" + i +
                ", j=" + j +
                ", direction=" + direction +
                '}';
    }
}
