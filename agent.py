import random
# used only for debugging
from maze_generator import print_maze

DIRECTIONS = {
        "NORTH": (-1, 0),
        "SOUTH": (1, 0),
        "WEST": (0, -1),
        "EAST": (0, 1)
    }

TILES = {
    "START": "START",
    "GOLD": "GOLD",
    "WALL": "OBSTACLE",
    "FREE": "EMPTY",
    "UNKNOWN": "UNKNOWN"
}


class Node:
    """
    A single node of a search tree used to search possible routes in the maze.
    Each node represents one step finishing at the position stored in self.position
    and has its children (following steps of possible routes) stored in self.children.
    """
    def __init__(self, origin, position):
        self.origin = origin
        self.position = position
        self.children = []


class Agent:
    """
    Agent intelligence for searching the maze.
    Receives size of the maze and the maximum number of steps to find the gold in the maze.
    Agent is supplied with its position in the maze, his field of vision, gold position and number of steps passed in
    the maze when the action method is called. Based on this information, agent has to decide which action to take.
    """

    def __init__(self, maze_size, step_limit, start_position, gold_position):
        self.step_limit = step_limit
        self.maze_size = maze_size
        self.agent_position = start_position
        self.start_position = start_position
        self.gold_position = gold_position

        self.maze = None
        self.init_maze()

        self.gold_found = False

    def init_maze(self):
        """initialize maze map with the positions of start and gold"""
        self.maze = []
        for i in range(self.maze_size[0]):
            self.maze.append([TILES["UNKNOWN"]] * self.maze_size[1])
        self.maze[self.start_position[0]][self.start_position[1]] = TILES["START"]
        self.maze[self.gold_position[0]][self.gold_position[1]] = TILES["GOLD"]

    def is_out_of_bounds(self, tile):
        """returns true if the given coordinates are out of bounds of the maze"""
        if tile[0] < 0 or tile[1] < 0:
            return True
        if tile[0] >= self.maze_size[0]:
            return True
        if tile[1] >= self.maze_size[1]:
            return True

        return False

    def save_observation(self, observation):
        """saves the observed information"""
        # save agent's position
        self.agent_position = observation.position

        # check if gold has been retrieved
        if not self.gold_found and self.agent_position == self.gold_position:
            self.gold_found = True

        # save visible tiles in each direction
        for direction in observation.vision:
            observed_pos = [self.agent_position[0], self.agent_position[1]]
            # save visible free tiles
            for i in range(observation.vision[direction]):
                observed_pos[0] += DIRECTIONS[direction][0]
                observed_pos[1] += DIRECTIONS[direction][1]
                self.maze[observed_pos[0]][observed_pos[1]] = TILES["FREE"]
            # save visible wall tile
            observed_pos[0] += DIRECTIONS[direction][0]
            observed_pos[1] += DIRECTIONS[direction][1]
            if not self.is_out_of_bounds(observed_pos):
                self.maze[observed_pos[0]][observed_pos[1]] = TILES["WALL"]

        # rewrite start and gold
        self.maze[self.start_position[0]][self.start_position[1]] = TILES["START"]
        self.maze[self.gold_position[0]][self.gold_position[1]] = TILES["GOLD"]

    def random_action(self):
        """Moves randomly"""
        return random.choice(list(DIRECTIONS.keys()))

    def select_action(self, observation):
        """
        Returns action the agent takes in given state
        :param observation: includes tuple "position" and dictionary "vision"
        :return: One of the actions from ACTIONS.keys()
        """
        self.save_observation(observation)

        if self.gold_found:
            ret = self.perform_BFS(TILES["START"])
        else:
            ret = self.perform_BFS(TILES["GOLD"])
        return ret

    def perform_BFS(self, target):
        """
        Performs BFS to find the shortest path to the given target (Gold or Start).
        Treats all unknown tiles as empty tiles.
        :return: The directions which to take to get to Gold by the shortest path.
        """
        # just to make finding errors easier
        if target != TILES["GOLD"] and target != TILES["START"]:
            return None

        # root represents 0th step (current position)
        root = Node(None, self.agent_position)
        # a list of all visited coordinates
        visited = [root.position]
        # keeps the last generation of nodes so we can access them
        youngest_nodes = []
        youngest_nodes_buffer = []

        # perform the first iteration of BFS (it is slightly different)
        for dir in DIRECTIONS:
            new_position = (root.position[0] + DIRECTIONS[dir][0], root.position[1] + DIRECTIONS[dir][1])
            if self.is_out_of_bounds(new_position):
                continue
            if self.maze[new_position[0]][new_position[1]] == target:
                return dir
            if self.maze[new_position[0]][new_position[1]] != TILES["WALL"]:
                new_node = Node(dir, new_position)
                root.children.append(new_node)
                youngest_nodes.append(new_node)
                visited.append(new_node.position)

        # perform the rest of BFS to find Gold
        while True:
            for node in youngest_nodes:
                for direction in list(DIRECTIONS.values()):
                    new_position = (node.position[0] + direction[0], node.position[1] + direction[1])
                    if self.is_out_of_bounds(new_position):
                        continue
                    if new_position in visited:
                        continue
                    if self.maze[new_position[0]][new_position[1]] == target:
                        return node.origin
                    if self.maze[new_position[0]][new_position[1]] != TILES["WALL"]:
                        new_node = Node(node.origin, new_position)
                        node.children.append(new_node)
                        youngest_nodes_buffer.append(new_node)
                        visited.append(new_node.position)
            youngest_nodes = youngest_nodes_buffer
            youngest_nodes_buffer = []
