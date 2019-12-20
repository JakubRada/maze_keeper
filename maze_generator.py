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


def generate_maze(maze_size):
    """
    Maze is built from cells that can be one of the elements of the MazeObjects enum,
    i.e. empty, obstacle, start or gold. Generated maze must be feasible.

    :return: 2-D list, the layout of the maze

    ===YOUR MAZE GENERATION CODE GOES HERE===
    """
    while True:
        layout = generate_random(maze_size)
        if is_feasible(layout):
            break
    return layout


if __name__ == '__main__':
    print(generate_maze((5, 5)))
