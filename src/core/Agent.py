from random import *
import pickle

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVES = {ACTION_UP: (-1, 0),
                ACTION_DOWN: (1, 0),
                ACTION_LEFT: (0, -1),
                ACTION_RIGHT: (0, 1)}

class Agent:
    def __init__(self, env, alpha=1, gamma=1, exploration=1, cooling_rate=0.99):
        self.__env = env
        self.reset()
        self.__init_qtable()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

    def reset(self):
        self.__state = self.__env.start
        self.__score = 0

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

    def __repr__(self):
        return str(self.__qtable)

