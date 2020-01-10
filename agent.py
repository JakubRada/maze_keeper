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
    "UNKNOWN": "UNKNOWN",
    "BARRIER": "BARRIER"
}


class Node:
    """
    A single node of a search tree used to search possible routes in the maze.
    Each node represents one step finishing at the position stored in self.position
    and has its children (following steps of possible routes) stored in self.children.
    """
    def __init__(self, origin, position):
        # contains the first move of the route taken to get to this node
        # or a list of all moves taken to get to this node (depends on what is needed)
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
        self.route_back = None
        self.steps_back_taken = 0
        self.visited_tiles = []
        for i in range(self.maze_size[0]):
            self.visited_tiles.append([False] * self.maze_size[1])

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
        # update visited_tiles
        self.visited_tiles[observation.position[0]][observation.position[1]] = True

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
                if self.maze[observed_pos[0]][observed_pos[1]] != TILES["BARRIER"]:
                    self.maze[observed_pos[0]][observed_pos[1]] = TILES["FREE"]
            # save visible wall tile
            observed_pos[0] += DIRECTIONS[direction][0]
            observed_pos[1] += DIRECTIONS[direction][1]
            if not self.is_out_of_bounds(observed_pos):
                self.maze[observed_pos[0]][observed_pos[1]] = TILES["WALL"]

        # rewrite start and gold
        if self.maze[self.start_position[0]][self.start_position[1]] != TILES["BARRIER"]:
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
        # save agent's position
        self.agent_position = observation.position
        # save observed tiles
        self.save_observation(observation)

        # during the way to gold, perform BFS every turn
        if not self.gold_found:
            ret = self.perform_BFS(TILES["GOLD"])
            # check for dead ends
            self.check_for_dead_ends(ret)
        # during the way back to start, perform BFS only once and save the whole route
        else:
            if not self.route_back:
                self.remove_barriers()
                self.add_barriers_for_unknown_tiles()
                self.route_back = self.perform_BFS(TILES["START"])
            ret = self.route_back[self.steps_back_taken]
            self.steps_back_taken += 1

        return ret

    def check_for_dead_ends(self, next_move):
        """Adds barriers to cut off dead ends in order to reduce computation time."""
        next_move = DIRECTIONS[next_move]
        next_position = (self.agent_position[0] + next_move[0], self.agent_position[1] + next_move[1])
        if self.visited_tiles[next_position[0]][next_position[1]]:
            self.maze[self.agent_position[0]][self.agent_position[1]] = TILES["BARRIER"]

    def remove_barriers(self):
        """Removes all barriers to be able to find way back to the Start."""
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                if self.maze[row][col] == TILES["BARRIER"]:
                    self.maze[row][col] = TILES["FREE"]
        self.maze[self.start_position[0]][self.start_position[1]] = TILES["START"]

    def add_barriers_for_unknown_tiles(self):
        """Add barriers to unknown tiles to ignore unknown parts of the maze on the way back to start."""
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                if self.maze[row][col] == TILES["UNKNOWN"]:
                    self.maze[row][col] = TILES["BARRIER"]

    def is_obstacle(self, coordinates):
        """Checks whether the tile of the given coordinates is an obstacle."""
        if self.maze[coordinates[0]][coordinates[1]] == TILES["WALL"]:
            return True
        if self.maze[coordinates[0]][coordinates[1]] == TILES["BARRIER"]:
            return True
        return False

    def perform_BFS(self, target):
        """
        Performs BFS to find the shortest path to the given target (Gold or Start).
        Treats all unknown tiles as empty tiles.
        :return: if target is GOLD: The direction which to take in the next move to get to Gold by the shortest path.
                 if target is START: A list of all directions to take to get to Start by the shortest path.
        """
        # just to make finding errors easier
        if target != TILES["GOLD"] and target != TILES["START"]:
            return None

        # root represents 0th step (current position)
        if target == TILES["GOLD"]:
            root = Node(None, self.agent_position)
        else:
            root = Node([], self.agent_position)
        # a list of all visited coordinates
        visited = []
        for i in range(self.maze_size[0]):
            visited.append([False] * self.maze_size[1])
        # keeps the last generation of nodes so we can access them
        youngest_nodes = []
        youngest_nodes_buffer = []

        # perform the first iteration of BFS (it is slightly different)
        for dir in DIRECTIONS:
            new_position = (root.position[0] + DIRECTIONS[dir][0], root.position[1] + DIRECTIONS[dir][1])
            if self.is_out_of_bounds(new_position):
                continue
            if self.maze[new_position[0]][new_position[1]] == target:
                if target == TILES["GOLD"]:
                    return dir
                else:
                    return [dir]
            if not self.is_obstacle((new_position[0], new_position[1])):
                if target == TILES["GOLD"]:
                    new_node = Node(dir, new_position)
                else:
                    new_node = Node([dir], new_position)
                root.children.append(new_node)
                youngest_nodes.append(new_node)
                visited[new_position[0]][new_position[1]] = True

        # perform the rest of BFS to find target
        while True:
            # safety check if generated barriers "locked agent in" somewhere (probably not necessary)
            if target == TILES["GOLD"] and len(youngest_nodes) == 0:
                self.remove_barriers()
                return self.perform_BFS(target)

            for node in youngest_nodes:
                for dir in DIRECTIONS:
                    new_position = (node.position[0] + DIRECTIONS[dir][0], node.position[1] + DIRECTIONS[dir][1])
                    if self.is_out_of_bounds(new_position):
                        continue
                    if visited[new_position[0]][new_position[1]]:
                        continue
                    if self.maze[new_position[0]][new_position[1]] == target:
                        if target == TILES["GOLD"]:
                            return node.origin
                        else:
                            new_origin = node.origin
                            new_origin.append(dir)
                            return new_origin
                    if not self.is_obstacle((new_position[0], new_position[1])):
                        if target == TILES["GOLD"]:
                            new_node = Node(node.origin, new_position)
                        else:
                            new_origin = []
                            for item in node.origin:
                                new_origin.append(item)
                            new_origin.append(dir)
                            new_node = Node(new_origin, new_position)
                        node.children.append(new_node)
                        youngest_nodes_buffer.append(new_node)
                        visited[new_position[0]][new_position[1]] = True
            youngest_nodes = youngest_nodes_buffer
            youngest_nodes_buffer = []
