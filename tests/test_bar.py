"""
tests/test_bar.py
Member 3: Testing and Verification for bar.py.

Run from the project root (the folder that contains bar.py):
    python -m pytest -v

Design rule: every expected value comes from the MATHEMATICS (a complete
legal break order always needs m*n - 1 breaks) or from the SPECIFICATION
(the rubric's list of invalid inputs). No expected value is copied from
bar.py's own output.
"""

import copy
import random

import pytest

from bar import Bar


# Helpers

def check_invariant(bar):
    """Facts that must hold after every legal break."""
    # 1. one more piece than breaks
    assert len(bar.pieces) - 1 == bar.breaks
    # 2. piece areas add up to the whole bar
    assert sum(p.area() for p in bar.pieces.values()) == bar.m * bar.n
    # 3. every piece lies inside the bar
    for p in bar.pieces.values():
        assert p.row >= 0 and p.col >= 0
        assert p.row + p.height <= bar.m
        assert p.col + p.width <= bar.n
    # 4. every cell belongs to exactly one piece: no empty cells (-1),
    #    and each piece owns exactly area() cells
    cells_per_id = {}
    for row in bar.grid():
        for cell in row:
            assert cell != -1, "an empty cell was found"
            cells_per_id[cell] = cells_per_id.get(cell, 0) + 1
    for pid, p in bar.pieces.items():
        assert cells_per_id.get(pid, 0) == p.area(), f"piece {pid} overlaps another piece"


def breakable_ids(bar):
    """Ids of pieces that are larger than 1x1, in ascending order."""
    return [pid for pid in sorted(bar.pieces) if not bar.pieces[pid].is_single()]


def peel_one_square(bar):
    """Strategy: always cut one unit off the first breakable piece."""
    pid = breakable_ids(bar)[0]
    if bar.pieces[pid].width > 1:
        return pid, "V", 1
    return pid, "H", 1


def random_strategy(rng):
    """Strategy: pick any breakable piece, any orientation, any legal offset."""
    def choose(bar):
        pid = rng.choice(breakable_ids(bar))
        p = bar.pieces[pid]
        if p.height > 1 and (p.width == 1 or rng.random() < 0.5):
            return pid, "H", rng.randint(1, p.height - 1)
        return pid, "V", rng.randint(1, p.width - 1)
    return choose


def run_strategy(bar, strategy):
    """Keep breaking until every piece is 1x1. Checks the invariant after each break."""
    while breakable_ids(bar):
        pid, orientation, offset = strategy(bar)
        bar.break_piece(pid, orientation, offset)
        check_invariant(bar)
    return bar.breaks


def legal_moves(bar):
    """Every legal (piece id, orientation, offset) on the current bar."""
    for pid in breakable_ids(bar):
        p = bar.pieces[pid]
        for offset in range(1, p.height):
            yield pid, "H", offset
        for offset in range(1, p.width):
            yield pid, "V", offset


def all_break_orders(m, n):
    """Explore EVERY legal break order on an m x n bar.
    Returns (number of complete orders, set of break totals reached).
    Only practical for small bars."""
    totals = set()
    count = 0

    def explore(bar):
        nonlocal count
        moves = list(legal_moves(bar))
        if not moves:                       # no legal move left: order is complete
            assert bar.is_solved()
            count += 1
            totals.add(bar.breaks)
            return
        for pid, orientation, offset in moves:
            child = copy.deepcopy(bar)      # branch from a copy so siblings don't interfere
            child.break_piece(pid, orientation, offset)
            explore(child)

    explore(Bar(m, n))
    return count, totals


    def snapshot(bar):
        """Everything a rejected cut must leave untouched."""
        return (
            bar.breaks,
            bar.next_id,
            {k: (p.row, p.col, p.height, p.width) for k, p in bar.pieces.items()},
        )


# ===========================================================================
# 1. Normal cases: 1x1, 1xn, mx1, squares, larger rectangles
# ===========================================================================

SHAPES = [(1, 1), (1, 7), (7, 1), (4, 4), (4, 5), (10, 10)]


@pytest.mark.parametrize("m, n", SHAPES)
def test_new_bar_is_one_piece_covering_everything(m, n):
    bar = Bar(m, n)
    assert len(bar.pieces) == 1
    p = bar.pieces[0]
    assert (p.row, p.col, p.height, p.width) == (0, 0, m, n)
    assert bar.breaks == 0
    check_invariant(bar)


@pytest.mark.parametrize("m, n", SHAPES)
def test_peeling_strategy_needs_mn_minus_1_breaks(m, n):
    bar = Bar(m, n)
    breaks = run_strategy(bar, peel_one_square)
    assert breaks == m * n - 1
    assert bar.is_solved()
    assert len(bar.pieces) == m * n


@pytest.mark.parametrize("m, n", SHAPES)
def test_random_orders_all_need_mn_minus_1_breaks(m, n):
    for seed in range(5):
        bar = Bar(m, n)
        breaks = run_strategy(bar, random_strategy(random.Random(seed)))
        assert breaks == m * n - 1, f"seed {seed} gave {breaks} breaks"
        assert bar.is_solved()


def test_1x1_bar_is_solved_with_zero_breaks():
    bar = Bar(1, 1)
    assert bar.is_solved()
    assert bar.breaks == 0
    assert bar.summary()["expected_total_breaks"] == 0


def test_single_row_bar_1x7_takes_6_breaks():
    bar = Bar(1, 7)
    for _ in range(6):
        pid = breakable_ids(bar)[0]
        bar.break_piece(pid, "V", 1)
        check_invariant(bar)
    assert bar.breaks == 6 and bar.is_solved()


def test_single_column_bar_7x1_takes_6_breaks():
    bar = Bar(7, 1)
    for _ in range(6):
        pid = breakable_ids(bar)[0]
        bar.break_piece(pid, "H", 1)
        check_invariant(bar)
    assert bar.breaks == 6 and bar.is_solved()


def test_2x3_trace_matches_worked_example():
    """The five cuts from the report's worked example."""
    bar = Bar(2, 3)
    bar.break_piece(0, "V", 1)   # id0 2x1, id1 2x2
    bar.break_piece(1, "V", 1)   # id1 2x1, id2 2x1
    bar.break_piece(0, "H", 1)   # id0 1x1, id3 1x1
    bar.break_piece(1, "H", 1)   # id1 1x1, id4 1x1
    bar.break_piece(2, "H", 1)   # id2 1x1, id5 1x1
    assert bar.breaks == 5
    assert bar.grid() == [[0, 1, 2], [3, 4, 5]]
    assert bar.is_solved()


def test_summary_is_consistent_after_each_break():
    bar = Bar(2, 3)
    while breakable_ids(bar):
        pid, orientation, offset = peel_one_square(bar)
        bar.break_piece(pid, orientation, offset)
        s = bar.summary()
        assert s["pieces"] == len(bar.pieces)
        assert s["breaks"] == bar.breaks
        assert s["solved"] == (not breakable_ids(bar))
    assert bar.summary()["solved"] is True
    assert bar.summary()["breaks"] == 5


# ===========================================================================
# 2. Cut geometry: is each new piece placed where the offset says?
# ===========================================================================

def test_horizontal_cut_geometry():
    bar = Bar(4, 3)
    top, bottom = bar.break_piece(0, "H", 1)
    assert (top.row, top.col, top.height, top.width) == (0, 0, 1, 3)
    assert (bottom.row, bottom.col, bottom.height, bottom.width) == (1, 0, 3, 3)
    assert top.id == 0 and bottom.id == 1


def test_vertical_cut_geometry_on_a_piece_not_at_origin():
    """The second cut must add the piece's own column (2) to the offset (1)."""
    bar = Bar(2, 4)
    bar.break_piece(0, "V", 2)                 # id0 at col 0 w2, id1 at col 2 w2
    left, right = bar.break_piece(1, "V", 1)
    assert (left.row, left.col, left.height, left.width) == (0, 2, 2, 1)
    assert (right.row, right.col, right.height, right.width) == (0, 3, 2, 1)


# ===========================================================================
# 3. Invalid dimensions
# ===========================================================================

@pytest.mark.parametrize("m, n", [(0, 5), (5, 0), (-1, 5), (3, -2), (0, 0)])
def test_zero_or_negative_dimensions_rejected(m, n):
    with pytest.raises(ValueError, match="positive integer"):
        Bar(m, n)


@pytest.mark.parametrize("m, n", [(2.5, 5), (5, 2.0), ("3", 3), (3, None), (True, 3), (3, False)])
def test_non_integer_dimensions_rejected(m, n):
    with pytest.raises(ValueError, match="positive integer"):
        Bar(m, n)


def test_error_message_names_the_bad_dimension():
    with pytest.raises(ValueError, match="^m must"):
        Bar(0, 5)
    with pytest.raises(ValueError, match="^n must"):
        Bar(5, 0)


# ===========================================================================
# 4. Invalid piece IDs
# ===========================================================================

@pytest.mark.parametrize("bad_id", [99, -1, 1])
def test_unknown_piece_id_rejected(bad_id):
    bar = Bar(2, 3)                            # only piece 0 exists
    with pytest.raises(ValueError, match="No piece with id"):
        bar.break_piece(bad_id, "V", 1)
    assert bar.breaks == 0


@pytest.mark.parametrize("bad_id", ["0", None, "one"])
def test_wrong_type_piece_id_rejected(bad_id):
    """Checks only that a ValueError is raised, not the wording, so the
    error message can be improved without breaking this test."""
    bar = Bar(2, 3)
    with pytest.raises(ValueError):
        bar.break_piece(bad_id, "V", 1)
    assert bar.breaks == 0


@pytest.mark.xfail(strict=True, reason="BUG-01: True is treated as piece id 1")
def test_bool_piece_id_is_rejected_when_piece_1_exists():
    bar = Bar(2, 2)
    bar.break_piece(0, "V", 1)                 # creates piece 1
    with pytest.raises(ValueError):
        bar.break_piece(True, "H", 1)


@pytest.mark.xfail(strict=True, reason="BUG-02: 0.0 is treated as piece id 0")
def test_float_piece_id_is_rejected():
    bar = Bar(2, 2)
    with pytest.raises(ValueError):
        bar.break_piece(0.0, "V", 1)
    assert bar.breaks == 0


@pytest.mark.xfail(strict=True, raises=TypeError,
                reason="BUG-03: a list id raises TypeError, not ValueError")
def test_unhashable_piece_id_raises_value_error():
    bar = Bar(2, 2)
    with pytest.raises(ValueError):
        bar.break_piece([0], "V", 1)


# ===========================================================================
# 5. Illegal cuts
# ===========================================================================

@pytest.mark.parametrize("orientation, offset", [
    ("V", 0), ("V", -1), ("V", 3), ("V", 4),   # bar is 2x3, so width is 3
    ("H", 0), ("H", -1), ("H", 2), ("H", 5),   # height is 2
])
def test_offset_outside_1_to_size_minus_1_rejected(orientation, offset):
    bar = Bar(2, 3)
    with pytest.raises(ValueError):
        bar.break_piece(0, orientation, offset)
    assert bar.breaks == 0


@pytest.mark.parametrize("orientation", ["X", "h", "v", "", None, "HV"])
def test_invalid_orientation_rejected(orientation):
    bar = Bar(2, 3)
    with pytest.raises(ValueError, match="orientation"):
        bar.break_piece(0, orientation, 1)
    assert bar.breaks == 0


@pytest.mark.parametrize("offset", [1.0, 1.5, "1", None, True])
def test_non_integer_offset_rejected(offset):
    bar = Bar(2, 3)
    with pytest.raises(ValueError, match="offset must be an integer"):
        bar.break_piece(0, "V", offset)
    assert bar.breaks == 0


def test_cannot_break_a_1x1_piece():
    bar = Bar(1, 1)
    for orientation in ("H", "V"):
        with pytest.raises(ValueError, match="1x1"):
            bar.break_piece(0, orientation, 1)
    assert bar.breaks == 0


# ===========================================================================
# 6. Atomicity: a rejected cut must change nothing
# ===========================================================================

@pytest.mark.parametrize("bad_call", [
    (0, "V", 3), (0, "H", 0), (0, "X", 1), (99, "V", 1), (0, "V", 1.5),
])
def test_rejected_cut_leaves_bar_unchanged(bad_call):
    bar = Bar(2, 3)
    bar.break_piece(0, "V", 1)                 # reach a non-trivial state first
    before = snapshot(bar)
    with pytest.raises(ValueError):
        bar.break_piece(*bad_call)
    assert snapshot(bar) == before             # same pieces, same counter, same next id
    check_invariant(bar)


# ===========================================================================
# 7. Different break orders
# ===========================================================================

@pytest.mark.parametrize("m, n, expected_orders", [(1, 3, 2), (1, 4, 6), (2, 2, 4)])
def test_every_break_order_on_small_bars(m, n, expected_orders):
    """Exhaustive: every legal order is explored. Expected counts were worked
    out by hand: a 1xn bar has (n-1)! orders, and 2x2 has 4."""
    orders, totals = all_break_orders(m, n)
    assert orders == expected_orders
    assert totals == {m * n - 1}


def test_every_break_order_on_2x3_gives_5_breaks():
    orders, totals = all_break_orders(2, 3)
    assert orders > 0
    assert totals == {5}
