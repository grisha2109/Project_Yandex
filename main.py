import arcade
import random

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
        self.trash = []
        for i in range(5):
            self.trash.append({'x': random.randint(50, SCREEN_HEIGHT - 50), 'y': SCREEN_WIDTH - 50, 'speed': random.uniform(2, 4), 'size': random.randint(10, 20)})

    def on_draw(self):
        self.clear()

        arcade.draw_triangle_filled(
        self.player_x, self.player_y + 25,
        self.player_x - 25, self.player_y - 25,
        self.player_x + 25, self.player_y - 25,
        arcade.color.GREEN)

        arcade.draw_text(f"Ваш счёт: {self.score}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, arcade.color.WHITE_SMOKE, 20)
        arcade.draw_text(f"Управление: <- ->", 10, SCREEN_HEIGHT - 40, arcade.color.WHITE_SMOKE, 20)

        for j in self.trash:
            arcade.draw_circle_filled(j['x'], j['y'], j['size'], arcade.color.YELLOW_ROSE)


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

    def on_update(self, delta_time):
        for i in self.trash:
            i['y'] -= i['speed']
            if i['y'] <= - i['size']:
                i['y'] = SCREEN_HEIGHT + i['size']
                i['x'] = random.randint(50, SCREEN_WIDTH - 50)

            distance_x = abs(self.player_x - i['x'])
            distance_y = abs(self.player_y - i['y'])
            if distance_x < 35 and distance_y < 35:
                self.score += 10
                i['y'] = SCREEN_HEIGHT + i['size']
                i['x'] = random.randint(50, SCREEN_WIDTH - 50)

def main():
    window = GameWindow()
    arcade.run()

if __name__ == '__main__':
    main()