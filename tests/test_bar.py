"""
tests/test_bar.py
Unit tests for Bar class and chocolate bar puzzle mechanics.
CIT3003 Analysis of Algorithms - Option 3
"""

import copy
import random
import pytest

from bar import Bar


# Test helpers

def check_invariant(bar):
    """Verify invariants that must hold after every legal cut."""
    # Pieces count must equal breaks + 1
    assert len(bar.pieces) - 1 == bar.breaks

    # Total area of all pieces must equal original bar dimensions
    assert sum(p.area() for p in bar.pieces.values()) == bar.m * bar.n

    # All pieces must be within grid boundaries
    for p in bar.pieces.values():
        assert 0 <= p.row and p.row + p.height <= bar.m
        assert 0 <= p.col and p.col + p.width <= bar.n

    # Each grid cell must be occupied by exactly one piece
    cell_counts = {}
    for row in bar.grid():
        for cell in row:
            assert cell != -1, "Found unassigned grid cell"
            cell_counts[cell] = cell_counts.get(cell, 0) + 1

    for pid, p in bar.pieces.items():
        assert cell_counts.get(pid, 0) == p.area(), f"Piece {pid} has incorrect cell count"


def breakable_ids(bar):
    """Return IDs of pieces that can still be cut (> 1x1)."""
    return [pid for pid in sorted(bar.pieces) if not bar.pieces[pid].is_single()]


def peel_one_square(bar):
    """Cut a 1-unit strip from the first breakable piece."""
    pid = breakable_ids(bar)[0]
    p = bar.pieces[pid]
    if p.width > 1:
        return pid, "V", 1
    return pid, "H", 1


def pick_random_cut(bar, rng):
    """Pick a random breakable piece, orientation, and valid offset."""
    pid = rng.choice(breakable_ids(bar))
    p = bar.pieces[pid]
    if p.height > 1 and (p.width == 1 or rng.random() < 0.5):
        return pid, "H", rng.randint(1, p.height - 1)
    return pid, "V", rng.randint(1, p.width - 1)


def run_strategy(bar, strategy_fn):
    """Repeatedly apply a strategy until all pieces are 1x1."""
    while not bar.is_solved():
        pid, orientation, offset = strategy_fn(bar)
        bar.break_piece(pid, orientation, offset)
        check_invariant(bar)
    return bar.breaks


def legal_moves(bar):
    """Generate all possible legal cuts for the current bar state."""
    for pid in breakable_ids(bar):
        p = bar.pieces[pid]
        for offset in range(1, p.height):
            yield pid, "H", offset
        for offset in range(1, p.width):
            yield pid, "V", offset


def all_break_orders(m, n):
    """Explore all possible sequences of legal cuts on an m x n bar."""
    totals = set()
    count = 0

    def explore(b):
        nonlocal count
        moves = list(legal_moves(b))
        if not moves:
            assert b.is_solved()
            count += 1
            totals.add(b.breaks)
            return

        for pid, orientation, offset in moves:
            child = copy.deepcopy(b)
            child.break_piece(pid, orientation, offset)
            explore(child)

    explore(Bar(m, n))
    return count, totals


def snapshot(bar):
    """Capture pieces and counters to verify atomicity of rejected operations."""
    return (
        bar.breaks,
        bar.next_id,
        {k: (p.row, p.col, p.height, p.width) for k, p in bar.pieces.items()},
    )


# Normal shapes & breaking strategies

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
        rng = random.Random(seed)
        breaks = run_strategy(bar, lambda b: pick_random_cut(b, rng))
        assert breaks == m * n - 1, f"Seed {seed} gave {breaks} breaks"
        assert bar.is_solved()


def test_2x3_trace_matches_worked_example():
    bar = Bar(2, 3)
    bar.break_piece(0, "V", 1)
    bar.break_piece(1, "V", 1)
    bar.break_piece(0, "H", 1)
    bar.break_piece(1, "H", 1)
    bar.break_piece(2, "H", 1)
    assert bar.breaks == 5
    assert bar.grid() == [[0, 1, 2], [3, 4, 5]]
    assert bar.is_solved()


# Cut geometry & placement

def test_vertical_cut_geometry_on_a_piece_not_at_origin():
    bar = Bar(2, 4)
    bar.break_piece(0, "V", 2)
    left, right = bar.break_piece(1, "V", 1)
    assert (left.row, left.col, left.height, left.width) == (0, 2, 2, 1)
    assert (right.row, right.col, right.height, right.width) == (0, 3, 2, 1)


# Dimension validation

@pytest.mark.parametrize("m, n", [(0, 5), (5, 0), (-1, 5), (3, -2), (0, 0)])
def test_zero_or_negative_dimensions_rejected(m, n):
    with pytest.raises(ValueError, match="positive integer"):
        Bar(m, n)


@pytest.mark.parametrize("m, n", [(2.5, 5), (5, 2.0), ("3", 3), (3, None), (True, 3), (3, False)])
def test_non_integer_dimensions_rejected(m, n):
    with pytest.raises(ValueError, match="positive integer"):
        Bar(m, n)


# Piece ID validation

@pytest.mark.parametrize("bad_id", [99, -1, 1])
def test_unknown_piece_id_rejected(bad_id):
    bar = Bar(2, 3)
    with pytest.raises(ValueError, match="No piece with id"):
        bar.break_piece(bad_id, "V", 1)
    assert bar.breaks == 0


@pytest.mark.parametrize("bad_id", ["0", None, "one"])
def test_wrong_type_piece_id_rejected(bad_id):
    bar = Bar(2, 3)
    with pytest.raises(ValueError):
        bar.break_piece(bad_id, "V", 1)
    assert bar.breaks == 0


def test_bool_piece_id_is_rejected_when_piece_1_exists():
    bar = Bar(2, 2)
    bar.break_piece(0, "V", 1)
    with pytest.raises(ValueError):
        bar.break_piece(True, "H", 1)


def test_float_piece_id_is_rejected():
    bar = Bar(2, 2)
    with pytest.raises(ValueError):
        bar.break_piece(0.0, "V", 1)
    assert bar.breaks == 0


def test_unhashable_piece_id_raises_value_error():
    bar = Bar(2, 2)
    with pytest.raises(ValueError):
        bar.break_piece([0], "V", 1)


# Cut parameters & legality

@pytest.mark.parametrize("orientation, offset", [
    ("V", 0), ("V", -1), ("V", 3), ("V", 4),
    ("H", 0), ("H", -1), ("H", 2), ("H", 5),
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


# Atomicity: rejected cuts must leave bar unchanged

@pytest.mark.parametrize("bad_call", [
    (0, "V", 3), (0, "H", 0), (0, "X", 1), (99, "V", 1), (0, "V", 1.5),
])
def test_rejected_cut_leaves_bar_unchanged(bad_call):
    bar = Bar(2, 3)
    bar.break_piece(0, "V", 1)
    before = snapshot(bar)
    with pytest.raises(ValueError):
        bar.break_piece(*bad_call)
    assert snapshot(bar) == before
    check_invariant(bar)


# Exhaustive break order verification

@pytest.mark.parametrize("m, n, expected_orders", [(1, 3, 2), (1, 4, 6), (2, 2, 4)])
def test_every_break_order_on_small_bars(m, n, expected_orders):
    orders, totals = all_break_orders(m, n)
    assert orders == expected_orders
    assert totals == {m * n - 1}


def test_every_break_order_on_2x3_gives_5_breaks():
    orders, totals = all_break_orders(2, 3)
    assert orders > 0
    assert totals == {5}
