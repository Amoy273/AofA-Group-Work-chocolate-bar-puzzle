# Bug Reports for bar.py

**To:** Member 1 (author of `bar.py`)
**From:** Member 3 (Testing and Verification)
**Status:** all three open. The fix below has been verified on a copy of `bar.py` but not yet applied to the project.

## Summary

| ID | Severity | Summary | Covered by test | Status |
|---|---|---|---|---|
| BUG-01 | Medium | Boolean `True` is accepted as piece ID 1 | `test_bool_piece_id_is_rejected_when_piece_1_exists` | Open |
| BUG-02 | Medium | Float `0.0` is accepted as piece ID 0 | `test_float_piece_id_is_rejected` | Open |
| BUG-03 | Low | A list as piece ID raises `TypeError` instead of `ValueError` | `test_unhashable_piece_id_raises_value_error` | Open |

**Why these severities:** BUG-01 and BUG-02 cut a real piece when the caller asked for something invalid, so the wrong piece changes silently. The rubric asks for graceful handling of invalid input, so these are medium. BUG-03 still raises an error, so no wrong result is produced, but the error is unclear and doesn't match the rest of the class. That makes it low.

---

## BUG-01: `True` is accepted as piece ID 1

**Location:** `bar.py`, `Bar.break_piece`, the check `if piece_id not in self.pieces`.

**Cause:** Python treats `True` as equal to `1`. The membership test passes whenever piece 1 exists, and the cut is applied to that piece. The offset and orientation checks don't catch the wrong ID, and nothing else does either.

**Steps to reproduce:**

```python
from bar import Bar
b = Bar(2, 2)
b.break_piece(0, "V", 1)     # creates piece 1
b.break_piece(True, "H", 1)  # should raise ValueError, but cuts piece 1
```

**Expected:** `ValueError` raised. The bar is unchanged.

**Actual:** the call succeeds and returns two new pieces. The break counter goes up.

---

## BUG-02: float `0.0` is accepted as piece ID 0

**Location:** same check as BUG-01.

**Cause:** `0.0 == 0` and `hash(0.0) == hash(0)`, so the dictionary lookup finds piece 0.

**Steps to reproduce:**

```python
from bar import Bar
Bar(2, 2).break_piece(0.0, "V", 1)  # should raise ValueError
```

**Expected:** `ValueError` raised.

**Actual:** the call succeeds and returns two pieces.

---

## BUG-03: list as piece ID raises `TypeError`

**Location:** same check as BUG-01.

**Cause:** dictionary lookups need a hashable key, and a list isn't hashable. Python raises `TypeError` before the code reaches its own error message.

**Steps to reproduce:**

```python
from bar import Bar
Bar(2, 2).break_piece([0], "V", 1)
```

**Expected:** `ValueError` with a message such as "piece_id must be an integer".

**Actual:** `TypeError: unhashable type: 'list'`

---

## Suggested fix (covers all three bugs)

Add a type check on `piece_id` before the membership test in `break_piece`:

```python
if isinstance(piece_id, bool) or not isinstance(piece_id, int):
    raise ValueError(f"piece_id must be an integer, got {piece_id!r}")
if piece_id not in self.pieces:
    raise ValueError(...)   # existing check, unchanged
```

This follows the same pattern `Bar.__init__` already uses for m and n. It rejects `True` (BUG-01), `0.0` (BUG-02) and `[0]` (BUG-03) before any lookup happens.

**Verification:** applied to a copy of `bar.py` in Member 3's environment. The three known-bug tests then pass, which pytest reports as XPASS(strict). The other 72 tests still pass.

**After the fix is merged:** Member 3 removes the three `@pytest.mark.xfail` lines in `tests/test_bar.py`, and the suite should show 75 passed.

---

## Member 2 (interface)

No bugs to report. There's no interface code in the project folder yet. When it's added, its tests should go in `tests/`, and the README's "What is tested" table should be updated.

## Notes for the group report (not code bugs)

These are inconsistencies in the written drafts, not in the code. They should be settled before the report is submitted.

- **Complexity disagreement.** One draft gives a full solve as O(mn). Another gives O((mn)²). The code as written gives O((mn)²), because the area-sum assertion visits every piece on each break. Timings confirm this: a 100×100 solve took about 8 seconds and a 200×200 solve about 135 seconds. Without that check, the total would be O(mn). The report should state which version it describes and why.
- **"No printing" claim.** A draft says `bar.py` contains no printing. The `__main__` demo at the bottom of the file does print, so the claim should be corrected or the demo moved out of the module.
