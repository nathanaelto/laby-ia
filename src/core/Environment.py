from src.core.Agent import ACTION_MOVES

MAZE = """
#.#############
#     !       #
#!!!  !   !   #
#     !  !!! !#
#        !    #
#     !  !    #
#  !!!!!!!    #
#     !  !!   #
#        !    #
#             #
#############*#
"""

REWARD_DEFAULT = -1

MAZE_START = '.'
MAZE_WALL = '#'
MAZE_GOAL = '*'
MAZE_BRICKWALL = '!'


class Environment:
    def __init__(self, str_maze, brick_walls):
        self.__brick_walls = brick_walls
        self.__parse(str_maze)
        self.__nb_states = len(self.__states)

    def __parse(self, str_maze):
        self.__states = {}
        for row, line in enumerate(str_maze.strip().splitlines()):
            for col, char in enumerate(line):
                if char == MAZE_START:
                    self.__start = (row, col)
                elif char == MAZE_GOAL:
                    self.__goal = (row, col)
                self.__states[(row, col)] = char

        self.__rows = row + 1
        self.__cols = col + 1

    def is_forbidden_state(self, state):
        return state not in self.__states \
               or (self.is_brick_wall(state) and self.__brick_walls) or self.is_wall(state) or self.is_start(state)

    def is_wall(self, state):
        return self.__states[state] == MAZE_WALL

    def is_brick_wall(self, state):
        return self.__states[state] == MAZE_BRICKWALL

    def is_start(self, state):
        return self.__states[state] == MAZE_START

    def is_goal(self, state):
        return self.__states[state] == MAZE_GOAL

    def do(self, state, action):
        move = ACTION_MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        reward = REWARD_DEFAULT

        if self.is_forbidden_state(new_state):
            reward = -2 * self.__nb_states
        elif self.is_brick_wall(new_state):
            reward = -2 * self.__nb_states
        else:
            state = new_state
            if self.__states[state] == MAZE_GOAL:
                reward = self.__nb_states

        return reward, state

    def print(self, agent):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                if state == agent.state:
                    res += 'A'
                else:
                    res += self.__states[state]
            res += '\n'
        print(res)

    @property
    def brick_walls(self):
        return self.__brick_walls

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols
