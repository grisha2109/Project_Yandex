import tkinter as tk
import subprocess
import sys
from PIL import Image, ImageTk
import os


def run_game():
    """Запускает игру и закрывает меню"""
    # Создаем файл с выбором пользователя
    with open("game_choice.txt", "w") as f:
        f.write("play")

    # Закрываем меню
    root.destroy()


def leave_app():
    """Выход из приложения"""
    # Создаем файл с выбором пользователя
    with open("game_choice.txt", "w") as f:
        f.write("exit")

    # Закрываем меню
    root.destroy()


def show_game_over_menu(final_score=0):
    """Показывает меню после завершения игры"""
    game_over_window = tk.Tk()
    game_over_window.title("Game Over")
    game_over_window.geometry("600x400")
    game_over_window.resizable(False, False)

    # Загружаем фон (если есть)
    bg_img = None
    try:
        bg_path = "assets/hon.png"
        if os.path.exists(bg_path):
            img = Image.open(bg_path)
            img = img.resize((600, 400), Image.LANCZOS)
            bg_img = ImageTk.PhotoImage(img)
    except:
        pass

    canvas = tk.Canvas(game_over_window, width=600, height=400, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    if bg_img:
        canvas.create_image(0, 0, image=bg_img, anchor="nw")

    # Заголовок
    canvas.create_text(
        300, 80,
        text="ИГРА ОКОНЧЕНА",
        font=("Arial", 24, "bold"),
        fill="red",
        justify="center"
    )

    # Счет
    canvas.create_text(
        300, 140,
        text=f"Ваш счет: {final_score}",
        font=("Arial", 18),
        fill="white",
        justify="center"
    )

    # Кнопки
    restart_btn = canvas.create_text(
        300, 220,
        text="Новая игра",
        font=("Arial", 18),
        fill="#4CAF50",
        activefill="lightgreen",
        justify="center"
    )
    canvas.tag_bind(restart_btn, "<Button-1>", lambda _: restart_game(game_over_window))

    main_menu_btn = canvas.create_text(
        300, 280,
        text="Главное меню",
        font=("Arial", 18),
        fill="#2196F3",
        activefill="lightblue",
        justify="center"
    )
    canvas.tag_bind(main_menu_btn, "<Button-1>", lambda _: return_to_menu(game_over_window))

    exit_btn = canvas.create_text(
        300, 340,
        text="Выход",
        font=("Arial", 18),
        fill="#f44336",
        activefill="salmon",
        justify="center"
    )
    canvas.tag_bind(exit_btn, "<Button-1>", lambda _: exit_from_game_over(game_over_window))

    game_over_window.mainloop()


def restart_game(window):
    """Запускает новую игру"""
    window.destroy()
    with open("game_choice.txt", "w") as f:
        f.write("play")


def return_to_menu(window):
    """Возвращает в главное меню"""
    window.destroy()
    with open("game_choice.txt", "w") as f:
        f.write("menu")


def exit_from_game_over(window):
    """Выход из игры из меню Game Over"""
    window.destroy()
    with open("game_choice.txt", "w") as f:
        f.write("exit")


# Главное меню
def create_main_menu():
    global root
    root = tk.Tk()
    root.title("Space Adventures")
    root.geometry("800x600")
    root.resizable(False, False)

    bg_img = None
    try:
        bg_path = "assets/hon.png"
        if os.path.exists(bg_path):
            img = Image.open(bg_path)
            img = img.resize((800, 600), Image.LANCZOS)
            bg_img = ImageTk.PhotoImage(img)
    except:
        pass

    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    if bg_img:
        canvas.create_image(0, 0, image=bg_img, anchor="nw")

    canvas.create_text(
        400, 80,
        text="Space Adventures",
        font=("Arial", 24, "bold"),
        fill="white",
        justify="center"
    )

    start_btn = canvas.create_text(
        400, 250,
        text="Старт",
        font=("Arial", 18),
        fill="#4CAF50",
        activefill="lightgreen",
        justify="center"
    )
    canvas.tag_bind(start_btn, "<Button-1>", lambda _: run_game())

    exit_btn = canvas.create_text(
        400, 350,
        text="Выход",
        font=("Arial", 18),
        fill="#f44336",
        activefill="salmon",
        justify="center"
    )
    canvas.tag_bind(exit_btn, "<Button-1>", lambda _: leave_app())

    root.mainloop()


if __name__ == "__main__":
    # Проверяем, нужно ли показать меню Game Over или главное меню
    if os.path.exists("final_score.txt"):
        with open("final_score.txt", "r") as f:
            final_score = int(f.read().strip())
        os.remove("final_score.txt")
        show_game_over_menu(final_score)
    else:
        create_main_menu()