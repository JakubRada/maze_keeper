from maze_keeper import ACTIONS
import random


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
        self.start_position = start_position
        self.gold_position = gold_position

    def random_action(self):
        """Moves randomly"""
        return random.choice(list(ACTIONS.keys()))

    def select_action(self, observation):
        """
        Returns action the agent takes in given state
        :param state: State of the agent
        :return: One of the actions from ACTIONS.keys()

        ===YOUR AGENT DECISION MAKING CODE GOES HERE===
        """
        return self.random_action()
