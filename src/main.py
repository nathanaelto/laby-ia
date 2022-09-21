import os
import arcade

from src.core.Agent import Agent
from src.core.Environment import Environment, MAZE
from src.core.MazeWindow import MazeWindow


FILE_QTABLE = '../qtable.dat'

if __name__ == '__main__':
    env = Environment(MAZE, False)

    agent = Agent(env)
    if os.path.exists(FILE_QTABLE):
        agent.load(FILE_QTABLE)

    print(len(env.states))

    agent.learn(0)

    windows = MazeWindow(agent)
    windows.setup()
    arcade.run()

    agent.save(FILE_QTABLE)

    print(agent.score)

