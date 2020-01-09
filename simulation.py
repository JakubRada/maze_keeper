import random

from maze_keeper import MazeKeeper
from visualization import Visualization


# Use seed to repeat the same behavior in randomized algorithms
random.seed(42)


class Simulation:
    """
    Simulation class that controls the main simulation loop and visualization of the agents movement in the maze.
    WARNING: Run this file from console for visualization to work properly.
    """

    def __init__(self, maze_size=(30, 50), step_limit=5000, visualize=True, agent=None, maze_generator=None):
        self.visualize = visualize
        self.step_limit = step_limit
        self.maze_size = maze_size

        self.layout = maze_generator(maze_size)

        self.maze_keeper = MazeKeeper(self.layout)

        self.agent = agent(maze_size, step_limit, self.maze_keeper.start_position, self.maze_keeper.gold_position)

    def run(self):
        observation = self.maze_keeper.observation()
        step = 0
        trace = []
        while not self.maze_keeper.finished and step < self.step_limit:
            step += 1
            action = self.agent.select_action(observation)
            observation = self.maze_keeper.agent_move(action)
            trace.append(observation.position)

        return trace, self.maze_keeper.layout

    def run_and_display_results(self, speed=0.1):
        trace, layout = self.run()

        print('Simulation finished.')
        if self.maze_keeper.finished:
            print('Agent SUCCESSFULY brought gold to the start', end='')
        else:
            print('Agent FAILED to bring the gold to the start', end='')
        print(' in {} steps.'.format(len(trace)))
        #input('Press any key to visualize the agents progress.')
        if self.visualize:
            vis = Visualization(layout, speed=speed)
            vis.show_trace(trace)


if __name__ == '__main__':
    from agent import Agent
    from maze_generator import generate_maze
    import time

    sizes = [5, 10, 20, 40, 70]
    # sizes = [5]

    for size in sizes:
        start = time.time()
        sim = Simulation(maze_size=(size, size), step_limit=1000, visualize=False, agent=Agent, maze_generator=generate_maze)
        sim.run_and_display_results(speed=0.1)
        finish = time.time()
        print("Time for ", size, "x", size, ": ", finish - start, sep="")
        print()
