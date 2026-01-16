import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Космическое приключение"
PLAYER_SPEED = 5
ASTEROID_SPAWN_INTERVAL = 2.5


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player_ship.png", scale=0.8)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 50

    def update(self):
        self.center_x += self.change_x
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH


class Asteroid(arcade.Sprite):
    def __init__(self, size):
        if size == "large":
            image = "assets/asteroid_large.png"
            scale = 0.6
        else:
            image = "assets/asteroid_small.png"
            scale = 0.4
        super().__init__(image, scale=scale)

        margin = int(self.width // 2)
        self.center_x = random.randint(margin, SCREEN_WIDTH - margin)
        self.center_y = SCREEN_HEIGHT + int(self.height // 2)
        self.change_y = -random.uniform(2, 5)

    def update(self, delta_time=1/60):
        self.center_y += self.change_y
        if self.top < 0:
            self.remove_from_sprite_lists()


class Trash(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/trash_common.png", scale=0.5)
        margin = int(self.width // 2)
        self.center_x = random.randint(margin, SCREEN_WIDTH - margin)
        self.center_y = SCREEN_HEIGHT + int(self.height // 2)
        self.change_y = -random.uniform(1.5, 3.5)

    def update(self, delta_time=1/60):
        self.center_y += self.change_y
        if self.top < 0:
            self.remove_from_sprite_lists()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.player_list = None
        self.asteroid_list = None
        self.trash_list = None
        self.background_list = None
        self.lives = 3
        self.game_over = False
        self.spawn_timer = 0.0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        self.asteroid_list = arcade.SpriteList()
        self.trash_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        bg = arcade.Sprite("assets/space_background.png")
        bg.center_x = SCREEN_WIDTH // 2
        bg.center_y = SCREEN_HEIGHT // 2
        bg.width = SCREEN_WIDTH
        bg.height = SCREEN_HEIGHT
        self.background_list.append(bg)

        self.lives = 3
        self.game_over = False
        self.spawn_timer = 0.0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.player_sprite.update()

        self.spawn_timer += delta_time
        if self.spawn_timer >= ASTEROID_SPAWN_INTERVAL:
            self.spawn_timer = 0
            choice = random.choices(
                ["large", "small", "trash"],
                weights=[1, 2, 2]
            )[0]

            if choice == "trash":
                self.trash_list.append(Trash())
            else:
                self.asteroid_list.append(Asteroid(choice))

        self.asteroid_list.update(delta_time)
        self.trash_list.update(delta_time)

        for obj in arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list):
            obj.remove_from_sprite_lists()
            self.lives -= 1

        for obj in arcade.check_for_collision_with_list(self.player_sprite, self.trash_list):
            obj.remove_from_sprite_lists()
            self.lives -= 1

        if self.lives <= 0:
            self.game_over = True

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.player_list.draw()
        self.asteroid_list.draw()
        self.trash_list.draw()

        arcade.draw_text(f"Жизни: {self.lives}", 10, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text("ИГРА ОКОНЧЕНА", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Нажмите R для перезапуска", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                             arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.R and self.game_over:
            self.setup()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player_sprite.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()