ACTIONS = {'NORTH': (-1, 0), 'SOUTH': (1, 0), 'WEST': (0, -1), 'EAST': (0, 1)}
MAZE_OBJECTS = {'EMPTY', 'OBSTACLE', 'GOLD', 'START'}


def get_cell_positions(layout, cell_types):
    """
    Returns list of positions of provided given cell types in the maze
    """
    positions = []
    for r, row in enumerate(layout):
        for c, cell in enumerate(row):
            if cell in cell_types:
                positions.append((r, c))
    return positions


def get_unique_cell(layout, cell_type):
    """
    Returns positions of single cell type cell if given cell type is present only once in the maze.
    Otherwise, raises an exception
    """
    cell = get_cell_positions(layout, [cell_type])
    if len(cell) == 1:
        return cell[0]
    else:
        raise Exception('Maze layout contains more than one {0} or does not contain {0} at all'.format(cell_type))


def add_tuples(c1, c2):
    """Elementwise add for two tuples of the same length"""
    return tuple(v1 + v2 for v1, v2 in zip(c1, c2))


class Observation:
    """Observation of an agent in a maze.
    Observation variables:
    position: 2-tuple, (r,c) coordinate of the current position of the agent
    vision: dictionary, number of cells to the closest obstacle or edge of the
    maze in each direction from ACTIONS.keys().
    """

    def __init__(self, vision, position):
        self.position = position
        self.vision = vision


class MazeKeeper:
    """
    Handles interaction between the agent and the maze.
    Takes agents actions and returns agents new Observation after executing the action
    """

    def __init__(self, layout):
        self.layout = layout
        self.start_position = get_unique_cell(layout, 'START')
        self.agent_position = self.start_position
        self.gold_position = get_unique_cell(self.layout, 'GOLD')
        self._movable_positions = get_cell_positions(self.layout, ['EMPTY', 'GOLD', 'START'])
        self.finished = False
        self.has_gold = False

    def _agent_vision(self):
        """
        Returns vision of the agent from current position
        :return dictionary:
        key is direction from ACTIONS.keys(),
        value is number of cells to the closest obstacle or edge in given diraction from the current position of the agent.
        """
        vision = {}
        for direction, move in ACTIONS.items():
            vision[direction] = -1
            tmp_position = self.agent_position
            while tmp_position in self._movable_positions:
                tmp_position = add_tuples(tmp_position, move)
                vision[direction] += 1
        return vision

    def observation(self):
        """Returns current Observation of the agent"""
        if self.agent_position == self.gold_position:
            self.has_gold = True
        if self.has_gold and self.agent_position == self.start_position:
            self.finished = True
        return Observation(vision=self._agent_vision(),
                           position=self.agent_position)

    def agent_move(self, action):
        """
        Executes action of the agent.
        If the agent tries to move into an obstacle or edge of the maze, he stays at the same position.
        :return Observation: new observation of the agent after executing the move.
        """
        new_position = add_tuples(self.agent_position, ACTIONS[action])
        if new_position in self._movable_positions:
            self.agent_position = new_position
        return self.observation()


if __name__ == '__main__':
    E, O, G, S = 'EMPTY', 'OBSTACLE', 'GOLD', 'START'

    SAMPLE_LAYOUT = [[E, O, E, E, E],
                     [E, O, E, O, E],
                     [S, O, E, O, G],
                     [E, O, E, O, E],
                     [E, E, E, E, E]]

    maze = MazeKeeper(SAMPLE_LAYOUT)
    print(get_cell_positions(SAMPLE_LAYOUT, S))
    print(maze._agent_vision())
