assignments = []

def cross(A, B):
    return [s+t for s in A for t in B]

rows = "ABCDEFGHI"
cols = "123456789"

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(f, s) for f in ("ABC","DEF","GHI") for s in ("123", "456", "789")]

unitlist = row_units + col_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    return dict(zip(boxes, [s.replace('.', '123456789') for s in grid]))

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for k in [k for k in values.keys() if len(values[k]) == 1]:
        for p in peers[k]:
            values[p] = values[p].replace(values[k], "")
    return values

def only_choice(values):
    for k in [k for k in values.keys() if len(values[k]) != 1]:
        for pv in values[k]:
            for u in units[k]:
                unitHasIt = False
                for p in u:
                    if pv in values[p] and p != k:
                        unitHasIt = True
                        break
                if unitHasIt == False:
                    values[k] = pv
                    break
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        values = eliminate(values)
        values = only_choice(values)
    
        solved_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_before == solved_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False

    unsolved = len([box for box in values.keys() if len(values[box]) > 1])
    if unsolved == 0:
        return values

    unsolved_boxes = [box for box in values.keys() if len(values[box]) > 1 ]
    sorted_by_unsolved = sorted(unsolved_boxes, key=lambda k: len(values[k]))

    for v in values[sorted_by_unsolved[0]]:
        cp = values.copy()
        cp[sorted_by_unsolved[0]] = v            
        attempt = search(cp)
        
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    d = grid_values(grid)
    
    return search(d)

if __name__ == '__main__':
    
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
