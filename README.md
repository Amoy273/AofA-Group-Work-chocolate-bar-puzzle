# Chocolate Bar Puzzle

A simulator and verification suite for the chocolate bar problem (CIT3003 Analysis of Algorithms, Option 3).

The puzzle explores breaking an m × n chocolate bar along grid lines into individual 1×1 squares, demonstrating that any complete sequence of valid cuts always requires exactly m·n − 1 breaks.

## Requirements

- Python 3.9+
- External packages:
  - `pygame` (powers the GUI simulation)
  - `pytest` (used to run the automated test suite)

## Installation & Setup

1. **Clone the repository** (or download the project folder):
   ```bash
   git clone https://github.com/<your-username>/AofA-Group-Work-chocolate-bar-puzzle.git
   cd AofA-Group-Work-chocolate-bar-puzzle
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   Install the required packages using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, install them directly: `pip install pygame pytest`)*

## Running the Project

### 1. GUI Simulation
Launch the graphical Pygame interface to visually configure bar sizes, select pieces, and perform cuts:
```bash
python simulation.py
```

### 2. Command-Line Demo
Run the quick built-in terminal smoke test to see the 2×3 worked example in action:
```bash
python bar.py
```

### 3. Automated Test Suite
Run all tests:
```bash
pytest
```
Or run with verbose output:
```bash
pytest -v
```
You can also run a specific test by name or keyword:
```bash
pytest -v -k "float_piece"
```
All 69 tests should collect and pass.

## Project Structure

- `bar.py` - Core puzzle implementation (`Piece` and `Bar` classes, cut logic, invariant assertions, and manual demo).
- `simulation.py` - Pygame visual simulation interface.
- `tests/test_bar.py` - Pytest test suite covering normal breaks, strategies, geometry, input validation, and atomicity.
- `requirements.txt` - Project dependencies (`pygame`, `pytest`).
- `pytest.ini` - Pytest configuration file.
- `RESULTS.md` - Expected vs actual test results, break order counts, and mutation test records.

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

## Developers
- [Amoy Payne (2408392)](https://github.com/Amoy273)
- [Ajani Adlam (2402087)](https://github.com/2402087UTECHPortfolio)
- [Malik Bennett (2404813)](https://github.com/malikbennett) 
- [Justin Powell (2501887)](https://github.com/Justin-Powelljm)
