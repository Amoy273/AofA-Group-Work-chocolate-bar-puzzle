from bar import Bar

b = Bar(2, 3)

def show(label):
    print(f"\n{label}  |  pieces={len(b.pieces)}  breaks={b.breaks}")
    g = b.grid()
    for row in g:
        print(" ".join(f"{x:2d}" for x in row))
    assert len(b.pieces) - 1 == b.breaks, "INVARIANT VIOLATED"

show("Start")
b.break_piece(0, 'V', 1); show("Step 1: break 0 V@1")
b.break_piece(1, 'V', 1); show("Step 2: break 1 V@1")
b.break_piece(2, 'H', 1); show("Step 3: break 2 H@1")
b.break_piece(1, 'H', 1); show("Step 4: break 1 H@1")
b.break_piece(0, 'H', 1); show("Step 5: break 0 H@1")

assert b.is_solved(), "Should be fully separated"
assert b.breaks == 2*3 - 1, "Should be exactly mn-1 breaks"
print("\nALL CHECKS PASSED")