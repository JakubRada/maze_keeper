# coding: utf8
import os
import time

MAZE_OBJECTS = {'EMPTY', 'OBSTACLE', 'GOLD', 'START'}
# Here, you can change how the objects in the maze are visualized
VISUALIZATION_OBJECT_MAPPING = {'EMPTY': ' ',  # '.',
                                'OBSTACLE': '█',  # 'X',
                                'GOLD': 'G',
                                'AGENT': 'O',
                                'START': 'X'}  # '_'}


class Visualization:
    """Handles visualization of the maze and traces through the maze. Visualization is to the console window."""

    def __init__(self, layout, speed=0.2):
        self.layout = layout
        self.M = len(layout[0])
        self.N = len(layout[1])
        self.draw_mapping = VISUALIZATION_OBJECT_MAPPING
        self.speed = speed

    def line(self, top=True):
        corners = ('╔', '╗') if top else ('╚', '╝')
        return corners[0] + '═' * self.N + corners[1]

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    def show(self, agent_cord=()):
        output = [self.line(top=True), '\n']
        for r, row in enumerate(self.layout):
            output.append('║')
            for c, cell in enumerate(row):
                if (r, c) in agent_cord:
                    output.append(self.draw_mapping['AGENT'])
                else:
                    output.append(self.draw_mapping[cell])
            output.append('║\n')
        output.append(self.line(top=False))
        output.append('\n')

        print(''.join(output))

    def show_trace(self, trace):
        for step, position in enumerate(trace):
            self.cls()
            print('\t Step: {}'.format(step))
            self.show(agent_cord=[position])
            time.sleep(self.speed)


if __name__ == '__main__':
    agent_trace = [(0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (4, 1),
                   (4, 2)]

    E, O, G, S = 'EMPTY', 'OBSTACLE', 'GOLD', 'START'
    SAMPLE_LAYOUT = [[E, O, E, E, E],
                     [E, O, E, O, E],
                     [S, O, E, O, G],
                     [E, O, E, O, E],
                     [E, E, E, E, E]]

    v = Visualization(SAMPLE_LAYOUT)
    v.show()
    v.show_trace(agent_trace)
