# Expected vs Actual Results

**Environment:** Linux, Python 3.12.3, pytest 9.2.0.
**Suite result:** 72 passed, 3 xfailed (the 3 xfailed tests are the known bugs in `BUG_REPORTS.md`). Runtime 0.16 s.

The "Actual" column was recorded by running `bar.py` in the environment above. Rerun the suite on your own machine and update this table if any value differs.

## Expected vs actual

| # | Group | Input | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | Normal | 1×1 bar | 0 breaks, solved | 0 breaks, solved | PASS |
| 2 | Normal | 1×7 bar (peel strategy) | 6 breaks | 6 breaks | PASS |
| 3 | Normal | 7×1 bar (peel strategy) | 6 breaks | 6 breaks | PASS |
| 4 | Normal | 4×4 bar | 15 breaks | 15 breaks | PASS |
| 5 | Normal | 4×5 bar | 19 breaks | 19 (peel); 19, 19, 19, 19, 19 (5 random seeds) | PASS |
| 6 | Normal | 10×10 bar | 99 breaks | 99 (peel); 99, 99, 99, 99, 99 (5 random seeds) | PASS |
| 7 | Worked example | 2×3, the five cuts in the report | 5 breaks, grid [[0,1,2],[3,4,5]] | 5 breaks, grid [[0,1,2],[3,4,5]] | PASS |
| 8 | Invalid dimension | m = 0 | ValueError | `m must be a positive integer, got 0` | PASS |
| 9 | Invalid dimension | m = −1 | ValueError | `m must be a positive integer, got -1` | PASS |
| 10 | Invalid dimension | m = 2.5 | ValueError | `m must be a positive integer, got 2.5` | PASS |
| 11 | Invalid dimension | m = True | ValueError | `m must be a positive integer, got True` | PASS |
| 12 | Invalid dimension | m = '3' | ValueError | `m must be a positive integer, got '3'` | PASS |
| 13 | Invalid piece ID | ID 99 on 2×3 bar | ValueError | `No piece with id 99. Valid ids: [0]` | PASS |
| 14 | Invalid piece ID | ID None | ValueError | `No piece with id None. Valid ids: [0]` | PASS |
| 15 | Illegal cut | Vertical offset 3 on 2×3 bar (width 3) | ValueError | `Vertical cut offset must be in 1..2, got 3 (piece width = 3).` | PASS |
| 16 | Illegal cut | Horizontal offset 0 on 2×3 bar | ValueError | `Horizontal cut offset must be in 1..1, got 0 (piece height = 2).` | PASS |
| 17 | Illegal cut | Orientation 'h' (lowercase) | ValueError | `orientation must be 'H' or 'V', got 'h'` | PASS |
| 18 | Illegal cut | Offset True | ValueError | `offset must be an integer, got True` | PASS |
| 19 | Illegal cut | Break a 1×1 piece | ValueError | `Piece 0 is a 1x1 square and cannot be broken.` | PASS |
| 20 | Atomicity | Orientation 'X' after one legal cut | Bar unchanged | Breaks, next ID and pieces unchanged | PASS |
| 21 | Break orders | 1×3, every order | 2 orders, all with 2 breaks | 2 orders, totals {2} | PASS |
| 22 | Break orders | 1×4, every order | 6 orders, all with 3 breaks | 6 orders, totals {3} | PASS |
| 23 | Break orders | 2×2, every order | 4 orders, all with 3 breaks | 4 orders, totals {3} | PASS |
| 24 | Break orders | 2×3, every order | every order gives 5 breaks | 56 orders, totals {5} | PASS |
| 25 | BUG-01 | True as ID after piece 1 exists | ValueError | Cuts piece 1 and returns two pieces | XFAIL (bug confirmed) |
| 26 | BUG-02 | 0.0 as ID | ValueError | Cuts piece 0 and returns two pieces | XFAIL (bug confirmed) |
| 27 | BUG-03 | [0] as ID | ValueError | `TypeError: unhashable type: 'list'` | XFAIL (bug confirmed) |

**Why rows 21–24 are exact:** a 1×n bar has (n−1)! complete break orders, so 1×3 gives 2 and 1×4 gives 6. A 2×2 bar has 4 orders, worked out by hand before running the code. The 2×3 count of 56 comes from the exhaustive search.

## Mutation check

To confirm the suite can actually catch mistakes, five deliberate bugs were planted in a copy of `bar.py`, one at a time.

| Planted bug | Failing tests | Caught |
|---|---|---|
| Horizontal offset range allows offset = height (off-by-one) | 1 | Yes |
| Second piece in a vertical cut ignores the piece's column | 11 | Yes |
| Boolean check removed from offset validation | 1 | Yes |
| Break counter never increases | 25 | Yes |
| Dimension check accepts 0 | 4 | Yes |

## Proposed fix for the three known bugs

The fix is one type check placed before the piece lookup (see `BUG_REPORTS.md`). Tested on a copy of `bar.py`:

- The three XFAIL tests now pass, and pytest reports them as XPASS(strict).
- The other 72 tests still pass, so the fix causes no regressions.
- Once Member 1 applies the fix, Member 3 removes the three `@pytest.mark.xfail` lines.
