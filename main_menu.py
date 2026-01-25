import tkinter as tk
import subprocess
import sys
from PIL import Image, ImageTk
import os

def run_game():
    game_file = "main1.py"
    if not os.path.exists(game_file):
        return
    try:
        subprocess.Popen([sys.executable, game_file])
        root.quit()
    except:
        pass

def leave_app():
    root.destroy()

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
