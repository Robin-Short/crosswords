import java.util.Objects;

public class Pos {

    public int i;
    public int j;

    public Pos(int i, int j) {
        this.i = i;
        this.j = j;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pos pos = (Pos) o;
        return i == pos.i && j == pos.j;
    }

    @Override
    public int hashCode() {
        return Objects.hash(i, j);
    }

    @Override
    public String toString() {
        return "Pos{" +
                "i=" + i +
                ", j=" + j +
                '}';
    }
}
