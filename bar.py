"""
bar.py — Chocolate Bar Puzzle: core algorithm and state.

Represents an m x n chocolate bar as a set of rectangular pieces and
supports legal grid-line breaks. Each break splits one rectangle into two
non-empty rectangles and increments the break counter.

Invariant (asserted after every break):
    len(pieces) - 1 == breaks          and    sum(piece.area()) == m * n

Coordinate system: 0-indexed, (row, col) = top-left corner of each piece.
Break offsets are PIECE-RELATIVE (distance from the piece's top/left edge).

Author: Member 1
Course: CIT3003 Analysis of Algorithms — Option 3 (Chocolate Bar Puzzle)
"""

from __future__ import annotations
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Piece: an axis-aligned rectangle on the bar grid
# ---------------------------------------------------------------------------
@dataclass
class Piece:
    id: int       # unique, stable identifier (used by the UI for display)
    row: int      # top-left row (0-indexed)
    col: int      # top-left column (0-indexed)
    height: int   # number of rows spanned
    width: int    # number of columns spanned

    def area(self) -> int:
        return self.height * self.width

    def is_single(self) -> bool:
        return self.area() == 1

    def __str__(self) -> str:
        return (f"Piece(id={self.id}, row={self.row}, col={self.col}, "
                f"h={self.height}, w={self.width})")


# ---------------------------------------------------------------------------
# Bar: holds all pieces and the break counter
# ---------------------------------------------------------------------------
class Bar:
    def __init__(self, m: int, n: int):
        # --- input validation (reject bool explicitly: isinstance(True, int) is True) ---
        for name, val in (("m", m), ("n", n)):
            if isinstance(val, bool) or not isinstance(val, int):
                raise ValueError(f"{name} must be a positive integer, got {val!r}")
            if val < 1:
                raise ValueError(f"{name} must be a positive integer, got {val}")

        self.m = m
        self.n = n
        self.next_id = 1                       # id 0 is the original bar
        self.pieces: dict[int, Piece] = {0: Piece(0, 0, 0, m, n)}
        self.breaks = 0

    # ------------------------------------------------------------------
    # Core operation: break one piece into two along a grid line
    # ------------------------------------------------------------------
    def break_piece(self, piece_id: int, orientation: str, offset: int) -> tuple[Piece, Piece]:
        """
        Break the piece with the given id into two non-empty rectangles.

        Parameters
        ----------
        piece_id    : id of an existing piece in this bar
        orientation : 'H' for a horizontal cut (splits height)
                      'V' for a vertical cut   (splits width)
        offset      : piece-relative cut position
                      'H': 1 <= offset <= height - 1
                      'V': 1 <= offset <= width  - 1

        Returns
        -------
        (top_or_left_piece, bottom_or_right_piece)
        The original id stays on the first returned piece; the second gets a new id.

        Raises
        ------
        ValueError with a clear message on any illegal request.
        """
        # --- legality checks (fail fast: no mutation before all checks pass) ---
        if piece_id not in self.pieces:
            raise ValueError(f"No piece with id {piece_id}. "
                             f"Valid ids: {sorted(self.pieces)}")

        piece = self.pieces[piece_id]

        if piece.is_single():
            raise ValueError(f"Piece {piece_id} is a 1x1 square and cannot be broken.")

        if orientation not in ("H", "V"):
            raise ValueError(f"orientation must be 'H' or 'V', got {orientation!r}")

        if isinstance(offset, bool) or not isinstance(offset, int):
            raise ValueError(f"offset must be an integer, got {offset!r}")

        if orientation == "H":
            if not (1 <= offset <= piece.height - 1):
                raise ValueError(f"Horizontal cut offset must be in 1..{piece.height - 1}, "
                                 f"got {offset} (piece height = {piece.height}).")
            # top piece keeps the original id, bottom piece gets a new id
            p1 = Piece(piece.id, piece.row, piece.col, offset, piece.width)
            p2 = Piece(self.next_id, piece.row + offset, piece.col,
                       piece.height - offset, piece.width)
        else:  # orientation == "V"
            if not (1 <= offset <= piece.width - 1):
                raise ValueError(f"Vertical cut offset must be in 1..{piece.width - 1}, "
                                 f"got {offset} (piece width = {piece.width}).")
            p1 = Piece(piece.id, piece.row, piece.col, piece.height, offset)
            p2 = Piece(self.next_id, piece.row, piece.col + offset,
                       piece.height, piece.width - offset)

        # --- commit the change ---
        del self.pieces[piece_id]
        self.pieces[p1.id] = p1
        self.pieces[p2.id] = p2
        self.next_id += 1
        self.breaks += 1

        # --- live invariant checks (cheap, catch offset bugs instantly) ---
        assert len(self.pieces) - 1 == self.breaks, \
            "Invariant violated: pieces - 1 != breaks"
        assert sum(p.area() for p in self.pieces.values()) == self.m * self.n, \
            "Invariant violated: total area != m * n"

        return p1, p2

    # ------------------------------------------------------------------
    # Helpers used by the UI and by tests
    # ------------------------------------------------------------------
    def is_solved(self) -> bool:
        """True when every remaining piece is a 1x1 square."""
        return all(p.is_single() for p in self.pieces.values())

    def grid(self) -> list[list[int]]:
        """Return an m x n 2D array of piece IDs (for ASCII rendering)."""
        g = [[-1] * self.n for _ in range(self.m)]
        for p in self.pieces.values():
            for r in range(p.row, p.row + p.height):
                for c in range(p.col, p.col + p.width):
                    g[r][c] = p.id
        return g

    def summary(self) -> dict:
        return {
            "m": self.m,
            "n": self.n,
            "pieces": len(self.pieces),
            "breaks": self.breaks,
            "solved": self.is_solved(),
            "expected_total_breaks": self.m * self.n - 1,
        }

    def __str__(self) -> str:
        ids = sorted(self.pieces)
        return f"Bar({self.m}x{self.n}, pieces={len(ids)}, breaks={self.breaks})"


# ---------------------------------------------------------------------------
# Smoke test / manual demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Smoke test: 2 x 3 bar, one legal break order ===\n")
    bar = Bar(2, 3)
    print(bar)
    print("Initial grid:", bar.grid())

    # A correct sequence: always break the largest remaining piece.
    attempts = [
        (0, "V", 1),   # 2x3 -> 2x1 (id 0) + 2x2 (id 1)
        (1, "V", 1),   # 2x2 -> 2x1 (id 1) + 2x1 (id 2)
        (0, "H", 1),   # 2x1 -> 1x1 (id 0) + 1x1 (id 3)
        (1, "H", 1),   # 2x1 -> 1x1 (id 1) + 1x1 (id 4)
        (2, "H", 1),   # 2x1 -> 1x1 (id 2) + 1x1 (id 5)
    ]

    for i, (pid, orient, off) in enumerate(attempts, 1):
        p1, p2 = bar.break_piece(pid, orient, off)
        print(f"Step {i}: break piece {pid} ({orient}{off}) -> "
              f"{p1.id} {p1.height}x{p1.width} + {p2.id} {p2.height}x{p2.width}")
        print("  summary:", bar.summary())

    assert bar.is_solved(), "Bar should be fully separated"
    assert bar.breaks == 2 * 3 - 1 == 5
    print("\nPASS: 2x3 bar solved in exactly 5 = 2*3 - 1 breaks.")

    # --- Demonstrate illegal-input handling ---
    print("\n=== Illegal-input checks ===")
    bad = Bar(3, 3)
    for call in [
        lambda: bad.break_piece(99, "V", 1),      # unknown id
        lambda: bad.break_piece(0, "X", 1),       # bad orientation
        lambda: bad.break_piece(0, "V", 0),       # offset 0
        lambda: bad.break_piece(0, "V", 3),       # offset too large
        lambda: Bar(0, 5),                        # zero dimension
        lambda: Bar(2.5, 5),                      # non-int dimension
    ]:
        try:
            call()
            print("  UNEXPECTED: no error raised")
        except ValueError as e:
            print(f"  OK ValueError: {e}")