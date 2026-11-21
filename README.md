# Chocolate Bar Puzzle: Test Suite

Testing and verification for `bar.py` (CIT3003 Option 3, Chocolate Bar Puzzle).
Prepared by Member 3.

## Requirements

- Python 3.9 or newer (tested with Python 3.12.3)
- pytest 7 or newer (tested with pytest 9.2.0)

## Setup

Install pytest once.

Windows:

```
py -m pip install pytest
```

macOS or Linux:

```
python3 -m pip install pytest
```

## Project layout

```
chocolate_bar/
├── bar.py            the simulator (Member 1)
├── pytest.ini        pytest settings (tells pytest where to find bar.py)
├── tests/
│   └── test_bar.py   the test suite (Member 3)
├── README.md         this file
├── RESULTS.md        expected vs actual results
└── BUG_REPORTS.md    bugs found, for Members 1 and 2
```

## Running the tests

Open a terminal in the `chocolate_bar` folder, the one that contains `bar.py`, then run:

Windows:

```
py -m pytest -v
```

macOS or Linux:

```
python3 -m pytest -v
```

The last line should read:

```
72 passed, 3 xfailed
```

The run takes well under a second.

## Reading the results

- **PASSED**: the behavior matches the specification.
- **XFAIL**: a known bug. The test is marked as expected to fail, so it doesn't break the run. Each one is described in `BUG_REPORTS.md`.
- **FAILED**: a regression or a new bug. Read the message under the failing test to see what was expected and what happened.
- **XPASS(strict)**: a bug was fixed, so its XFAIL test now passes. The run is marked as failed on purpose. Remove the `@pytest.mark.xfail` line above that test and the run will pass again.

To run one test, or all tests matching a name:

```
python -m pytest -v -k "float_piece"
```

## What is tested

| Group              | Tests | What it checks                                                                                                                           |
| ------------------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Normal shapes      | 23    | 1×1, 1×7, 7×1, 4×4, 4×5 and 10×10 bars. Each starts as one piece, reaches m·n − 1 breaks under every strategy, and ends fully separated. |
| Worked example     | 1     | The 2×3 trace from the report produces the expected grid.                                                                                |
| Summary            | 1     | `summary()` agrees with the bar's state after every break.                                                                               |
| Cut geometry       | 2     | New pieces land at the correct row and column, including a piece that doesn't start at the top-left corner.                              |
| Invalid dimensions | 12    | Zero, negative, decimal, string, `None` and boolean values for m or n are rejected, and the error names the bad dimension.               |
| Invalid piece IDs  | 9     | Unknown IDs are rejected. Wrong-type IDs are rejected. Three known bugs are marked XFAIL.                                                |
| Illegal cuts       | 20    | Offsets outside 1 to size−1, invalid orientations, non-integer offsets and any cut on a 1×1 piece are rejected.                          |
| Atomicity          | 5     | After a rejected cut, the break count, the piece list and the next ID are unchanged.                                                     |
| Break orders       | 4     | Every legal break order on 1×3, 1×4, 2×2 and 2×3 bars is explored. Each complete order uses exactly m·n − 1 breaks.                      |

Every expected value comes from the mathematics or the specification, not from copying the code's output. The break-order tests use exhaustive enumeration on small bars and seeded random orders on larger ones.

## How the tests check the invariant

`check_invariant()` in `tests/test_bar.py` runs after each break in the larger tests. It checks four things independently of `bar.py`'s own `assert` statements:

1. pieces − 1 = breaks
2. the piece areas sum to m × n
3. every piece lies inside the bar
4. every cell is covered by exactly one piece

## Known limitations

- The tests exercise the simulator through its code only. The command-line interface (Member 2) isn't covered until it exists in this folder.
- Exhaustive break-order checks are limited to small bars. The largest is 2×3, which has 56 complete orders. Larger bars are covered by random orders.
- `bar.py` uses `assert` for its invariant checks, and Python removes those under `python -O`. The tests check the invariant themselves, so they still catch problems when run that way.
- Lowercase `'h'` and `'v'` are rejected by design. If the group decides to accept them, update `test_invalid_orientation_rejected`.
