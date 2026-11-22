# Chocolate Bar Puzzle — Test Suite

Test suite and verification for `bar.py` (CIT3003 Analysis of Algorithms, Option 3).

## Setup & Running the Tests

Make sure `pytest` is installed:

```bash
pip install pytest
```

Run all tests from the repository root:

```bash
pytest -v
```

To run a specific test by name or keyword:

```bash
pytest -v -k "float_piece"
```

All 69 tests should pass.

## Project layout

```
chocolate_bar/
├── bar.py            
├── pytest.ini       
├── tests/
│   └── test_bar.py   
├── README.md         
├── RESULTS.md        
└── BUG_REPORTS.md    
```

## Test Suite Breakdown

| Category | Tests | Description |
|---|---|---|
| Normal shapes | 18 | Tests bars of various dimensions (1×1, strips, squares, rectangles up to 10×10) under peeling and randomized cut strategies. Confirms each run finishes in m·n − 1 breaks. |
| Worked example | 1 | Executes the 5-cut worked example from the report on a 2×3 bar, verifying the resulting grid and piece IDs. |
| Cut geometry | 1 | Verifies coordinate calculations (row/col offsets) when cutting a piece that is not at the origin (0, 0). |
| Dimension validation | 11 | Confirms that non-integer, negative, or zero dimensions for m and n raise ValueError. |
| Piece ID validation | 9 | Checks that non-existent IDs, wrong types (strings, None), booleans (True/False), floats (0.0), and unhashable types ([0]) raise ValueError. |
| Cut parameters | 20 | Validates orientation ('H' or 'V' only), cut offsets (must be an integer within 1 <= offset < size), and rejects attempts to cut a 1×1 piece. |
| Atomicity | 5 | Ensures rejected cuts raise ValueError without mutating the bar state (breaks counter, next ID, and pieces dictionary remain unchanged). |
| Exhaustive break orders | 4 | Explores every possible sequence of legal cuts for small bars (1×3, 1×4, 2×2, 2×3), verifying that all complete paths terminate in exactly m·n − 1 breaks. |
| **Total** | **69** | |

## Invariant Verification

During solver and strategy runs, `check_invariant()` runs after every cut to verify:
1. Number of pieces is always `breaks + 1`.
2. Total area of all pieces equals m × n.
3. All pieces lie within the bar boundaries (0 <= row + height <= m, 0 <= col + width <= n).
4. Every cell on the m × n grid is occupied by exactly one piece (no overlaps, no empty cells).
