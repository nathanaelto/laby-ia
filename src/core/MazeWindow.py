import arcade

SPRITE_SIZE = 64


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
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)

            if self.__agent.environment.is_brick_wall(state):

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()

