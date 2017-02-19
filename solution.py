assignments = []

def cross(A, B):
    return [s+t for s in A for t in B]

# create some helper structures to help easily find
# peers and units

rows = "ABCDEFGHI"
cols = "123456789"

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(f, s) for f in ("ABC","DEF","GHI") for s in ("123", "456", "789")]

# unit needed to make sure we can enforce diagonal constraints
diagonal_units = [[a[0]+a[1] for a in zip(rows,cols)], [a[0]+a[1] for a in zip(rows[::-1],cols)]]

# make sure to add to diagonal units
unitlist = row_units + col_units + square_units + diagonal_units

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
    possibleTwins = [box for box in values.keys() if len(values[box]) == 2]

    for pt in possibleTwins:
        for u in units[pt]:
            twinsInUnit = [t for t in u if values[t] == values[pt]]
            if len(twinsInUnit) == 2:
                for v in values[pt]:
                    for ui in [ui for ui in u if values[ui] != values[pt]]:
                        assign_value(values, ui, values[ui].replace(v, ""))
    return values

def grid_values(grid):
    """
    Turn a string encoded sudoku puzzle into a dictionary
    where key is the address of the box and value is either a solved value
    or all the digits 1 through 9 
    """
    return dict(zip(boxes, [s.replace('.', '123456789') for s in grid]))

def display(values):
    """
    Output sudoku puzzle in console so that it can be visualized
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Find boxes that are solved and then for each of those get its peer
    and eliminate the value of that box for the peer as that value
    can't be used more than once for peers
    """
    for k in [k for k in values.keys() if len(values[k]) == 1]:
        for p in peers[k]:
            assign_value(values, p, values[p].replace(values[k], ""))
    return values

def only_choice(values):
    """
    Check each unsolved box and see if any of the potential solutions
    can be determined base on the criteria if none of its pairs have that value
    as either a solution or a possible solution
    """
    for k in [k for k in values.keys() if len(values[k]) != 1]:
        for pv in values[k]:
            for u in units[k]:
                unitHasIt = False
                for p in u:
                    if pv in values[p] and p != k:
                        unitHasIt = True
                        break
                if unitHasIt == False:
                    assign_value(values, k, pv)
                    break
    return values

def reduce_puzzle(values):
    """
        Apply constraint propagation to try and solve the puzzle, or at least
        reduce the solution space.

        Use elimination, only choice, and naked twins constraints to solve the board

        Make sure to check for stalled progress (no more eliminations, choices, twins can be applied)
    """
    stalled = False
    while not stalled:
        solved_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_before == solved_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    """
    Search for the solution for a given puzzle. General approach:
        - reduce the puzzle
        - see if it was solved by the reduction, return if so
        - find the smallest unsolved box, and search for solution again with a
            puzzle updated with the chosen value
    """
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
