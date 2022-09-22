# A expérimenter
#
# - Possibilité de traverser des murs
# - Plusieurs solutions au labyrinthe

from random import *

import arcade
import os
import pickle
import matplotlib.pyplot as plt

MAZE = """
#.#############
#     #       #
####  #   #   #
#     #  ### ##
#        #    #
#     #  #    #
#  #######    #
#     #  ##   #
#        #    #
#             #
#############*#
"""

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVES = {ACTION_UP: (-1, 0),
                ACTION_DOWN: (1, 0),
                ACTION_LEFT: (0, -1),
                ACTION_RIGHT: (0, 1)}

REWARD_DEFAULT = -1

MAZE_START = '.'
MAZE_WALL = '#'
MAZE_GOAL = '*'

SPRITE_SIZE = 64

FILE_QTABLE = 'qtable.dat'


class Environment:
    def __init__(self, str_maze):
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
               or self.is_wall(state) or self.is_start(state)

    def is_wall(self, state):
        return self.__states[state] == MAZE_WALL

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


class Agent:
    def __init__(self, env, alpha=1, gamma=1, exploration=0, cooling_rate=0.99):
        self.__env = env
        self.__score = 0
        self.__history = []
        self.reset()
        self.__init_qtable()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

    def reset(self, append_score = True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = env.start
        self.__score = 0


    def heat(self):
        self.__exploration = 1

    def __init_qtable(self):
        self.__qtable = {}
        for state in self.__env.states:
            self.__qtable[state] = {}
            for action in ACTIONS:
                self.__qtable[state][action] = 0

    def step(self):
        action = self.best_action()
        reward, state = self.__env.do(self.state, action)

        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.state][action] += \
            self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.state][action])
        self.__state = state
        self.__score += reward
        return action, reward

    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(ACTIONS)
        else:
            actions = self.__qtable[self.__state]
            return max(actions, key=actions.get)

    def learn(self, iterations):
        for i in range(iterations):
            self.reset()
            while self.state != self.__env.goal:
                self.step()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)

    @property
    def score(self):
        return self.__score

    @property
    def state(self):
        return self.__state

    @property
    def environment(self):
        return self.__env

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    def __repr__(self):
        return str(self.__qtable)


class MazeWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         'AL-2 Maze')

        self.__agent = agent
        self.__iteration = 1

    def setup(self):
        self.__walls = arcade.SpriteList()

        for state in self.__agent.environment.states:
            if self.__agent.environment.is_wall(state):
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_single.png", 0.5)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)

        self.__goal = arcade.Sprite(":resources:images/tiles/mushroomRed.png", 0.5)
        self.__goal.center_x, self.__goal.center_y = self.state_to_xy(self.__agent.environment.goal)

        self.__alien = arcade.Sprite(":resources:images/alien/alienBlue_walk1.png", 0.3)
        self.__alien.center_x, self.__alien.center_y = self.state_to_xy(self.__agent.state)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__goal.draw()
        self.__alien.draw()

        arcade.draw_text(f"#{self.__iteration} Score : {self.__agent.score} T°C : {self.__agent.exploration}",
                         10, 10, arcade.csscolor.WHITE, 20)

    def new_game(self):
        self.__agent.reset()
        self.__alien.center_x, self.__alien.center_y = self.state_to_xy(self.__agent.state)
        self.__iteration += 1

    def on_update(self, delta_time):
        if self.__agent.state != self.__agent.environment.goal:
            action, reward = self.__agent.step()
            self.__alien.center_x, self.__alien.center_y = self.state_to_xy(self.__agent.state)
        else:
            self.new_game()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()


if __name__ == '__main__':
    env = Environment(MAZE)

    agent = Agent(env)
    if os.path.exists(FILE_QTABLE):
        agent.load(FILE_QTABLE)

    print(len(env.states))

    # agent.learn(20)

    windows = MazeWindow(agent)
    windows.setup()
    arcade.run()

    agent.save(FILE_QTABLE)

    print(agent.score)

    plt.plot(agent.history)
    plt.show()

