from maze_keeper import ACTIONS, get_cell_positions, get_unique_cell, add_tuples
import random

"""
When supplied with the size of the maze as NxM tuple (M - number of rows,
M - number of columns), function generate mazemust generate a maze layout of
given size.
Coordinates in the maze are such that c is the index of the column, r is the
index of the row, indexing from top-left corner at (0,0).
Maze is a 2-D list that consists of cells that are one of the elements of the
MazeObjects enum, i.e. empty, obstacle, start or gold.
Generated maze has to be feasible, i.e. there must exist valid path between
the start and the gold.
"""

EMPTY = 'EMPTY'
WALL = 'OBSTACLE'
GOLD = 'GOLD'
START = 'START'
UNKNOWN = 'UNKNOWN'
RIGHT_LINE_THRESHOLD = 10
GOLD_THRESHOLD = 5

def generate_empty(maze_size):
    """Creates an empty maze with start at top-left corner and gold at the opposite corner"""
    layout = []
    for r in range(maze_size[0]):
        row = []
        for c in range(maze_size[1]):
            row.append('EMPTY')
        layout.append(row)
    layout[0][0] = 'START'
    layout[-1][-1] = 'GOLD'
    return layout


def generate_random(maze_size):
    """Creates random maze with origin and destination in opposing corners. May not be feasible."""
    layout = []
    for r in range(maze_size[0]):
        row = []
        for c in range(maze_size[1]):
            # 25% chance of cell being  a wall
            row.append(random.choice(['EMPTY', 'EMPTY', 'EMPTY', 'OBSTACLE']))
        layout.append(row)
    layout[0][0] = 'START'
    layout[-1][-1] = 'GOLD'
    return layout


def is_feasible(layout):
    """
    Use BFS to find whether the layout is feasible, i.e. whether there exists
    a path beween start and gold.
    """
    gold = get_unique_cell(layout, "GOLD")
    start = get_unique_cell(layout, "START")
    movable_positions = set(get_cell_positions(layout, ["EMPTY", "GOLD"]))

    wave = {start}
    while wave:
        if gold in wave:
            return True
        expanding_cell = wave.pop()
        for action in ACTIONS.values():
            new_cell = add_tuples(expanding_cell, action)
            if new_cell in movable_positions:
                movable_positions.remove(new_cell)
                wave.add(new_cell)
    return False

def init_maze(rows, cols):
    layout = []
    for i in range(rows):
        temp = []
        for n in range(cols):
            temp.append(EMPTY)
        layout.append(temp)
    return layout

def place_start_gold(layout):
    layout[0][0] = START
    gold_position = (len(layout) - 3, 0)
    if len(layout) == GOLD_THRESHOLD:
        gold_position = (len(layout) - 2, 0)
    layout[gold_position[0]][gold_position[1]] = GOLD
    layout[gold_position[0] - 1][gold_position[1]] = WALL
    layout[gold_position[0]][gold_position[1] + 1] = WALL


def place_right_line(layout):
    for i in range(1, len(layout) - 1):
        layout[i][len(layout[0]) - 2] = WALL
    layout[len(layout) - 1][len(layout[0]) - 3] = WALL

def place_start_path(layout):
    for i in range(1, len(layout) - 3):
        layout[i][1] = WALL

def place_gold_path(layout):
    start = len(layout[0]) - 2
    if len(layout[0]) > RIGHT_LINE_THRESHOLD:
        place_right_line(layout)
        start -= 2
    for i in range(1, start):
        layout[len(layout) - 2][i] = WALL
    for i in range(len(layout) - 3, 0, -1):
        layout[i][start] = WALL

def place_dead_ends_thin(layout):
    count = len(layout[0]) - 6
    position = len(layout[0]) - 4
    if len(layout[0]) > RIGHT_LINE_THRESHOLD:
        count -= 2
        position -= 2
    count = int(count / 2)
    for i in range(count, 0, -1):
        y = 1
        x = position
        c = 2
        if i == count:
            c = i + 1
        while layout[y + c][x] != WALL:
            layout[y][x] = WALL
            y += 1
        y -= 1
        for n in range(i + 1):
            layout[y][x] = WALL
            y += 1
            x -= 1
        y -= 1
        while layout[y][x] != WALL:
            layout[y][x] = WALL
            x -= 1
        position -= 2

def diagonalize_up(layout, x, y):
    while layout[y - 1][x + 1] != WALL:
        layout[y][x] = WALL
        y -= 1
        x += 1

def place_diagonals_thin(layout):
    y = len(layout) - 3
    if len(layout) <= GOLD_THRESHOLD:
        y += 1
    x = 2
    while layout[y - 1][x] == WALL:
        x += 1
    x += 1
    while layout[y][x] != WALL and layout[y][x + 1] != WALL and layout[y][x + 2]:
        diagonalize_up(layout, x, y)
        x += 3

def place_dead_ends_thick(layout):
    count = len(layout[0]) - 4
    if len(layout[0]) >= RIGHT_LINE_THRESHOLD:
        count -= 2
    count = int((count - 1) / 2)
    x = 3
    if len(layout[0]) % 2 == 0:
        x += 1
    for i in range(count):
        y = 1
        while layout[y][x] != WALL:
            layout[y][x] = WALL
            y += 1
        x += 2

def clear_vertical(layout):
    end = len(layout) - 2
    start = 1
    if end <= GOLD_THRESHOLD:
        end += 1
        start += 1
    for y in range(start, end):
        if layout[y][2] == WALL:
            layout[y][1] = EMPTY

def clear_horizontal(layout):
    end = len(layout[0]) - 3
    if len(layout[0]) >= RIGHT_LINE_THRESHOLD:
        end -= 2
    y = len(layout) - 2
    for x in range(1, end):
        if layout[y - 1][x] == WALL:
            layout[y][x] = EMPTY

def place_top_thin(layout):
    x = 3
    y = 2
    while layout[y][x] == EMPTY and layout[y + 1][x] == EMPTY:
        layout[y][x] = WALL
        layout[y][x + 1] = EMPTY
        y += 2

def place_top_thick(layout):
    if len(layout[0]) % 2 == 0:
        x = 3
        y = 2
        while layout[y][x] == EMPTY and layout[y + 1][x] == EMPTY:
            layout[y][x] = WALL
            layout[y][x + 1] = EMPTY
            y += 2

def generate_maze(maze_size):
    """
    Maze is built from cells that can be one of the elements of the MazeObjects enum,
    i.e. empty, obstacle, start or gold. Generated maze must be feasible.

    :return: 2-D list, the layout of the maze

    ===YOUR MAZE GENERATION CODE GOES HERE===
    """
    rows = maze_size[0]
    cols = maze_size[1]
    layout = init_maze(rows, cols)
    place_start_gold(layout)
    place_gold_path(layout)
    place_start_path(layout)
    if rows >= cols:
        place_dead_ends_thin(layout)
        if cols > 13:
            place_diagonals_thin(layout)
        place_top_thin(layout)
    else:
        place_dead_ends_thick(layout)
        place_top_thick(layout)
    clear_vertical(layout)
    clear_horizontal(layout)
    place_start_gold(layout)
    if is_feasible(layout):
        return layout

def print_maze(maze):
    values = {
        EMPTY: "·",
        WALL: "\u2588",
        START: "S",
        GOLD: "G",
        UNKNOWN: " "
    }
    print_maze_header(maze)
    print()
    for row in range(len(maze)):
        print_maze_row(maze, row, values)
        print()
    print_maze_footer(maze)
    print()
    

def print_maze_header(maze):
    print("\u250f", end="")
    print("\u2501" * len(maze[0]), end="")
    print("\u2513", end="")

def print_maze_footer(maze):
    print("\u2517", end="")
    print("\u2501" * len(maze[0]), end="")
    print("\u251b", end="")

def print_maze_row(maze, line, values):
        print("\u2503", end="")
        for col in maze[line]:
            print(values[col], end="")
        print("\u2503", end="")

def test(maze):
    if not is_feasible(maze):
        print(len(maze[0]), len(maze), "NotFeasible")

def test_mazes():
    for i in range(5, 71):
        for n in range(5, 71):
            try:
                test(generate_maze((i, n)))
            except:
                print(i, n, "Error")

def save_mazes():
    values = {
        EMPTY: "·",
        WALL: "\u2588",
        START: "S",
        GOLD: "G",
        UNKNOWN: " "
    }
    l = []
    y = 0
    for i in range(5, 71):
        l.append([])
        for n in range(5, 71):
            l[y].append(generate_maze((i, n)))
        y += 1
    for i in range(len(l)):
        for n in range(len(l[0])):
            print_maze_header(l[i][n])
            print(" ", end="")
        print()
        for n in range(len(l[i][n])):
            for o in range(len(l[0])):
                print_maze_row(l[i][o], n, values)
                print(" ", end="")
            print()
        for n in range(len(l[0])):
            print_maze_footer(l[i][n])
            print(" ", end="")
        print()


if __name__ == '__main__':
    test_mazes()
    # print_maze(generate_maze((18, 18)))
    # save_mazes()
