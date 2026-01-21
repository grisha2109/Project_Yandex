import arcade
import random
import math
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Spaceship Adventures — by Григорий Ф. и Артем М."

PLAYER_SPEED = 5
PLAYER_Y = 50
OBJECT_FALL_SPEED_BASE = 2
LIVES_START = 3
HIGHSCORE_FILE = "highscore.txt"
ASTEROID_SPAWN_INTERVAL = 1.5

TYPE_TRASH_COMMON = 1
TYPE_TRASH_VALUABLE = 2
TYPE_ASTEROID_SMALL = 3
TYPE_ASTEROID_LARGE = 4
TYPE_SHIELD = 5
TYPE_MAGNET = 6
TYPE_SLOW = 7


class FallingObject(arcade.Sprite):
    def __init__(self, object_type):
        super().__init__()
        self.object_type = object_type

        # Используем изображения если они существуют, иначе создаем квадраты
        if object_type == TYPE_TRASH_COMMON:
            try:
                self.texture = arcade.load_texture("assets/trash_common.png")
                self.scale = 0.5
            except:
                self.texture = arcade.make_soft_square_texture(20, arcade.color.LIME_GREEN)
            self.points = 10
        elif object_type == TYPE_TRASH_VALUABLE:
            try:
                self.texture = arcade.load_texture("assets/trash_valuable.png")
                self.scale = 0.1
            except:
                self.texture = arcade.make_soft_square_texture(25, arcade.color.GOLD)
            self.points = 50
        elif object_type == TYPE_ASTEROID_SMALL:
            try:
                self.texture = arcade.load_texture("assets/asteroid_small.png")
                self.scale = 0.2
            except:
                self.texture = arcade.make_soft_square_texture(30, arcade.color.DARK_GRAY)
            self.damage = 1
        elif object_type == TYPE_ASTEROID_LARGE:
            try:
                self.texture = arcade.load_texture("assets/asteroid_large.png")
                self.scale = 0.6
            except:
                self.texture = arcade.make_soft_square_texture(45, arcade.color.BLACK)
            self.damage = 2
        elif object_type == TYPE_SHIELD:
            self.texture = arcade.load_texture("assets/shield_bonus.png")
            self.scale = 0.1
        elif object_type == TYPE_MAGNET:
            self.texture = arcade.load_texture("assets/magnet_bonus.png")
            self.scale = 0.1
        elif object_type == TYPE_SLOW:
            self.texture = arcade.load_texture("assets/slow_bonus.png")
            self.scale = 0.1
        else:
            self.texture = arcade.make_soft_square_texture(20, arcade.color.WHITE)

        self.center_x = random.randint(20, SCREEN_WIDTH - 20)
        self.center_y = SCREEN_HEIGHT + 20
        self.change_y = -OBJECT_FALL_SPEED_BASE
        self.fall_speed = OBJECT_FALL_SPEED_BASE

    def update(self, delta_time=1 / 60):
        self.center_y += self.change_y * delta_time * 60
        if self.top < 0:
            self.remove_from_sprite_lists()


class PlayerShip(arcade.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.texture = arcade.load_texture("assets/player_ship.png")
            self.scale = 0.1
        except:
            self.texture = arcade.make_soft_square_texture(60, arcade.color.CYAN)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = PLAYER_Y
        self.change_x = 0

    def update(self):
        self.center_x += self.change_x
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE)

        self.player = None
        self.player_sprite_list = None
        self.objects_list = None
        self.background_list = None
        self.score = 0
        self.lives = LIVES_START
        self.game_over = False
        self.level = 1
        self.level_num = 1
        self.shield_active = False
        self.magnet_active = False
        self.slow_active = False
        self.slow_timer = 0

        self.spawn_timer = 0
        self.spawn_interval = 1.0

        self.highscore = self.load_highscore()

    def setup(self):
        # Создаем фон
        self.background_list = arcade.SpriteList()
        try:
            bg = arcade.Sprite("assets/space_background.png")
            bg.center_x = SCREEN_WIDTH // 2
            bg.center_y = SCREEN_HEIGHT // 2
            bg.width = SCREEN_WIDTH
            bg.height = SCREEN_HEIGHT
            self.background_list.append(bg)
        except:
            pass  # Если нет фонового изображения, используем просто цвет

        self.player = PlayerShip()
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player)

        self.objects_list = arcade.SpriteList()
        self.score = 0
        self.lives = LIVES_START
        self.game_over = False
        self.level = 1
        self.shield_active = False
        self.magnet_active = False
        self.slow_active = False
        self.slow_timer = 0
        self.spawn_interval = 1.0
        self.spawn_timer = 0

    def load_highscore(self):
        if not os.path.exists(HIGHSCORE_FILE):
            return 0
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except (ValueError, OSError):
            return 0

    def save_highscore(self):
        if self.score > self.highscore:
            try:
                with open(HIGHSCORE_FILE, "w") as f:
                    f.write(str(self.score))
            except OSError:
                pass

    def spawn_object(self):
        r = random.random()
        if r < 0.45:
            obj = FallingObject(TYPE_TRASH_COMMON)
        elif r < 0.55:
            obj = FallingObject(TYPE_TRASH_VALUABLE)
        elif r < 0.75:
            obj = FallingObject(TYPE_ASTEROID_SMALL)
        elif r < 0.90:
            obj = FallingObject(TYPE_ASTEROID_LARGE)
        elif r < 0.94 and not self.shield_active:
            obj = FallingObject(TYPE_SHIELD)
        elif r < 0.97 and not self.magnet_active:
            obj = FallingObject(TYPE_MAGNET)
        elif r < 0.99 and not self.slow_active:
            obj = FallingObject(TYPE_SLOW)
        else:
            obj = FallingObject(TYPE_TRASH_COMMON)
        self.objects_list.append(obj)

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.R:
            self.setup()
            return

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -PLAYER_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = 0

    def disable_magnet(self, _):
        self.magnet_active = False

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.player.update()
        self.objects_list.update(delta_time)

        if self.slow_active:
            self.slow_timer -= delta_time
            if self.slow_timer <= 0:
                self.slow_active = False
        if self.score > 100:
            self.level += 1
            self.level_num = 2
        if self.score > 400:
            self.level += 2
            self.level_num = 3
        if self.score > 1000:
            self.level += 3
            self.level_num = 4
        if self.score > 2000:
            self.level += 4
            self.level_num = 5
        if self.score > 3300:
            self.level += 3
            self.level_num = 7
        if self.score > 4000:
            self.level += 2
            self.level_num = 8
        if self.score > 5000:
            self.level += 1
            self.level_num = 9
        if self.score > 10000:
            self.level += 2
            self.level_num = "MAX LEVEL!"

        base_speed = OBJECT_FALL_SPEED_BASE + (self.level - 1) * 0.3
        speed_mult = 0.5 if self.slow_active else 1.0


        # Устанавливаем скорость падения объектов
        for obj in self.objects_list:
            obj.change_y = -base_speed * speed_mult

        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_object()
            self.spawn_interval = max(0.3, 1.0 - self.level * 0.05)

        # Проверка столкновений
        for obj in arcade.check_for_collision_with_list(self.player, self.objects_list):
            obj.remove_from_sprite_lists()

            if obj.object_type in (TYPE_TRASH_COMMON, TYPE_TRASH_VALUABLE):
                self.score += obj.points
            elif obj.object_type == TYPE_ASTEROID_SMALL:
                if self.shield_active:
                    self.shield_active = False
                else:
                    self.lives -= 1
            elif obj.object_type == TYPE_ASTEROID_LARGE:
                if self.shield_active:
                    self.shield_active = False
                else:
                    self.lives -= 2
            elif obj.object_type == TYPE_SHIELD:
                self.shield_active = True
            elif obj.object_type == TYPE_MAGNET:
                self.magnet_active = True
                arcade.schedule(self.disable_magnet, 5.0)
            elif obj.object_type == TYPE_SLOW:
                self.slow_active = True
                self.slow_timer = 5.0

            if self.lives <= 0:
                self.lives = 0
                self.game_over = True
                self.save_highscore()

        self.level = (self.score // 1000) + 1

        if self.magnet_active:
            for obj in self.objects_list:
                if obj.object_type not in (TYPE_TRASH_COMMON, TYPE_TRASH_VALUABLE):
                    continue
                dx = self.player.center_x - obj.center_x
                dy = self.player.center_y - obj.center_y
                dist = math.hypot(dx, dy)
                if dist == 0:
                    continue
                force = 2.0
                obj.center_x += (dx / dist) * force
                obj.center_y += (dy / dist) * force

    def on_draw(self):
        self.clear()

        # Рисуем фон или звезды
        if self.background_list:
            self.background_list.draw()
        else:
            # Рисуем звезды если нет фона
            for _ in range(80):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                arcade.draw_point(x, y, arcade.color.WHITE, random.uniform(1, 2))

        self.objects_list.draw()
        self.player_sprite_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
        arcade.draw_text(f"Lives: {self.lives}", 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 16)
        arcade.draw_text(f"Level: {self.level_num}", 10, SCREEN_HEIGHT - 90, arcade.color.WHITE, 16)
        arcade.draw_text(f"Highscore: {self.highscore}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30,
                         arcade.color.YELLOW, 14)

        if self.shield_active:
            arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 40,
                                      (0, 100, 255, 80))

        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30,
                             arcade.color.RED, 48, anchor_x="center")
            arcade.draw_text("Press R to restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
                             arcade.color.WHITE, 20, anchor_x="center")
            arcade.draw_text("ИГРА ОКОНЧЕНА", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80,
                             arcade.color.RED, 40, anchor_x="center")


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()