import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Космическое приключение"

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = 50
        self.score = 0
        arcade.set_background_color(arcade.color.BLUEBERRY)

    def on_draw(self):
        self.clear()

        arcade.draw_triangle_filled(
        self.player_x, self.player_y + 25,
        self.player_x - 25, self.player_y - 25,
        self.player_x + 25, self.player_y - 25,
        arcade.color.GREEN)

        arcade.draw_text(f"Ваш счёт: {self.score}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, arcade.color.WHITE_SMOKE, 20)
        arcade.draw_text(f"Управление: <- ->", 10, SCREEN_HEIGHT - 40, arcade.color.WHITE_SMOKE, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_x -= 10
        elif key == arcade.key.RIGHT:
            self.player_x += 10
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        if self.player_x < 25:
            self.player_x = 25
        if self.player_x > SCREEN_WIDTH - 25:
            self.player_x = SCREEN_WIDTH - 25


def main():
    window = GameWindow()
    arcade.run()

if __name__ == '__main__':
    main()