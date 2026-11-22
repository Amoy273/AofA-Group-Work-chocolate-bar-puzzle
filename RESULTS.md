# Test Results & Verification

**Test environment:** Python 3.13 / pytest 9.2  
**Result:** 69 passed (0.15s)

## Expected vs Actual Results

Summary of key test scenarios verified against `bar.py`:

| # | Group | Input / Action | Expected | Actual | Status |
|---|---|---|---|---|---|
| 1 | Normal solve | 1×1 bar | 0 breaks, solved | 0 breaks, solved | PASS |
| 2 | Normal solve | 1×7 bar (peel strategy) | 6 breaks | 6 breaks | PASS |
| 3 | Normal solve | 7×1 bar (peel strategy) | 6 breaks | 6 breaks | PASS |
| 4 | Normal solve | 4×4 bar | 15 breaks | 15 breaks | PASS |
| 5 | Normal solve | 4×5 bar (peeling & 5 random seeds) | 19 breaks | 19 breaks across all runs | PASS |
| 6 | Normal solve | 10×10 bar (peeling & 5 random seeds) | 99 breaks | 99 breaks across all runs | PASS |
| 7 | Worked example | 2×3 bar, five specific cuts | 5 breaks, grid `[[0,1,2],[3,4,5]]` | 5 breaks, grid `[[0,1,2],[3,4,5]]` | PASS |
| 8 | Invalid dimension | m = 0 | ValueError | ValueError raised | PASS |
| 9 | Invalid dimension | m = -1 | ValueError | ValueError raised | PASS |
| 10 | Invalid dimension | m = 2.5 | ValueError | ValueError raised | PASS |
| 11 | Invalid dimension | m = True | ValueError | ValueError raised | PASS |
| 12 | Invalid dimension | m = '3' | ValueError | ValueError raised | PASS |
| 13 | Invalid piece ID | Unknown ID 99 on 2×3 bar | ValueError | ValueError raised | PASS |
| 14 | Invalid piece ID | ID None | ValueError | ValueError raised | PASS |
| 15 | Illegal cut | Vertical offset 3 on piece of width 3 | ValueError | ValueError raised | PASS |
| 16 | Illegal cut | Horizontal offset 0 | ValueError | ValueError raised | PASS |
| 17 | Illegal cut | Orientation 'h' (lowercase) | ValueError | ValueError raised | PASS |
| 18 | Illegal cut | Offset True | ValueError | ValueError raised | PASS |
| 19 | Illegal cut | Cut a 1×1 piece | ValueError | ValueError raised | PASS |
| 20 | Atomicity | Bad orientation 'X' on cut | State unchanged | Pieces, break count, and next ID unchanged | PASS |
| 21 | Break orders | 1×3 bar (all orders) | 2 orders, all 2 breaks | 2 orders, all 2 breaks | PASS |
| 22 | Break orders | 1×4 bar (all orders) | 6 orders, all 3 breaks | 6 orders, all 3 breaks | PASS |
| 23 | Break orders | 2×2 bar (all orders) | 4 orders, all 3 breaks | 4 orders, all 3 breaks | PASS |
| 24 | Break orders | 2×3 bar (all orders) | 56 orders, all 5 breaks | 56 orders, all 5 breaks | PASS |
| 25 | Piece ID edge case | True as piece ID after piece 1 exists | ValueError | ValueError raised | PASS |
| 26 | Piece ID edge case | 0.0 as piece ID | ValueError | ValueError raised | PASS |
| 27 | Piece ID edge case | [0] as piece ID | ValueError | ValueError raised | PASS |

*Notes on break order counts:*  
For a 1×n bar, any cut sequence corresponds to picking cut locations one by one, giving (n−1)! distinct orders (2 for 1×3, 6 for 1×4). For a 2×2 bar, there are 4 orders. For a 2×3 bar, exhaustive tree exploration confirms there are 56 distinct paths to solve the bar, and every single one takes exactly 5 breaks.

## Mutation Testing

To ensure the test suite properly catches implementation errors, we tested five injected faults in `bar.py`:

| Injected Bug | Failing Tests Caught | Detected? |
|---|---|---|
| Allow offset == height in horizontal cut (off-by-one) | 1 | Yes |
| Ignore piece column offset in vertical cuts | 11 | Yes |
| Remove boolean check on cut offset | 1 | Yes |
| Break counter does not increment | 25 | Yes |
| Accept dimension <= 0 | 4 | Yes |

## Edge Cases & Bug Fixes

We addressed three piece ID validation edge cases in `bar.py`:
- In Python, `bool` is a subclass of `int` (`isinstance(True, int) == True` and `True == 1`). If piece 1 existed, `break_piece(True, ...)` previously succeeded because `True in pieces` returned true.
- Floats like `0.0` matched integer key `0` due to equality and identical hash values.
- Unhashable objects like lists (`[0]`) previously failed with an unhandled `TypeError` during the `in self.pieces` lookup instead of raising `ValueError`.

Adding `if isinstance(piece_id, bool) or not isinstance(piece_id, int): raise ValueError(...)` before the dictionary lookup ensures all non-integer and boolean IDs are cleanly rejected with `ValueError`.
