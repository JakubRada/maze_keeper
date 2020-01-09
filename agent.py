from maze_keeper import ACTIONS
import random
from maze_generator import print_maze


class Agent:
    """
    Agent intelligence for searching the maze.
    Receives size of the maze and the maximum number of steps to find the gold in the maze.
    Agent is supplied with its position in the maze, his field of vision, gold position and number of steps passed in
    the maze when the action method is called. Based on this information, agent has to decide which action to take.
    """

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

    def __init__(self, maze_size, step_limit, start_position, gold_position):
        self.step_limit = step_limit
        self.maze_size = maze_size
        self.agent_position = start_position
        self.start_position = start_position
        self.gold_position = gold_position

        self.maze = None
        self.init_maze()

    def init_maze(self):
        """initialize maze map with the positions of start and gold"""
        self.maze = []
        for i in range(self.maze_size[0]):
            self.maze.append([self.TILES["UNKNOWN"]] * self.maze_size[1])
        self.maze[self.start_position[0]][self.start_position[1]] = self.TILES["START"]
        self.maze[self.gold_position[0]][self.gold_position[1]] = self.TILES["GOLD"]

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
        # save visible tiles in each direction
        for direction in observation.vision:
            observed_pos = [self.agent_position[0], self.agent_position[1]]
            # save visible free tiles
            for i in range(observation.vision[direction]):
                observed_pos[0] += self.DIRECTIONS[direction][0]
                observed_pos[1] += self.DIRECTIONS[direction][1]
                self.maze[observed_pos[0]][observed_pos[1]] = self.TILES["FREE"]
            # save visible wall tile
            observed_pos[0] += self.DIRECTIONS[direction][0]
            observed_pos[1] += self.DIRECTIONS[direction][1]
            if not self.is_out_of_bounds(observed_pos):
                self.maze[observed_pos[0]][observed_pos[1]] = self.TILES["WALL"]

    def random_action(self):
        """Moves randomly"""
        return random.choice(list(ACTIONS.keys()))

    def select_action(self, observation):
        """
        Returns action the agent takes in given state
        :param observation: includes tuple "position" and dictionary "vision"
        :return: One of the actions from ACTIONS.keys()
        """
        self.save_observation(observation)

        return self.random_action()
