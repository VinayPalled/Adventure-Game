import sys
import random
from tkinter import *
import tkinter.messagebox as tmsg
from PIL import Image, ImageTk


def get_story(level=1):
    with open(f'assets/level{level}_story.txt') as f:
        story = f.read()
    return story


def show_help():
    with open('assets/help.txt') as f:
        help_text = f.read()
    win = Toplevel(root)
    win.geometry(WIN_SIZE)
    win.resizable(False, False)
    win.config(bg=BG_COLOR)
    Label(win, text=help_text, font=("Arial", 14, "bold"), justify='center').pack(ipady=30, pady=100, ipadx=20)
    Button(win, text="Close", command=win.destroy, font=("Arial", 20, "bold"), bg='red', fg='yellow').pack()
    win.mainloop()


def show_treasure_window():
    GAME_WON_MSG = "Congratulations, You have won the game!"
    win = Toplevel(root)
    win.geometry(WIN_SIZE)
    win.config(bg=BG_COLOR)
    win.resizable(False, False)
    canvas = Canvas(win, bg='green', width=720, height=480)
    treasure_img = Image.open('assets/treasure.png')
    treasure_img = ImageTk.PhotoImage(treasure_img)
    canvas.image = treasure_img
    canvas.create_image(0, 0, image=treasure_img, anchor=NW)
    canvas.create_text(360, 395, text=GAME_WON_MSG, font=("Arial", 20, 'bold'), fill='yellow', justify='center')
    canvas.pack()
    win.mainloop()


def show_game_over_window():
    win = Toplevel(root)
    win.geometry(WIN_SIZE)
    win.config(bg=BG_COLOR)
    win.resizable(False, False)
    game_over_msg = "You were killed by the {} as you chose the wrong door"
    canvas = Canvas(win, bg='red', width=720, height=480)
    if current_level == 1:
        img_path = 'assets/ghost.png'
        game_over_msg = game_over_msg.format('ghost')
    elif current_level == 2:
        img_path = 'assets/animal.png'
        game_over_msg = game_over_msg.format('animal')
    game_over_img = Image.open(img_path)
    game_over_img = ImageTk.PhotoImage(game_over_img)
    canvas.image = game_over_img
    canvas.create_image(0, 0, image=game_over_img, anchor=NW)
    canvas.create_text(360, 395, text="GAME OVER!", font=("Arial", 20, 'bold'), fill='yellow', justify='center')
    canvas.create_text(360, 435, text=game_over_msg, font=("Arial", 15, 'bold'), fill='yellow', justify='center')
    canvas.pack()
    win.mainloop()


def pick_door(door_no):
    correct_door = random.randint(1, 2)
    global current_level
    win = root.winfo_children()[4]
    if door_no == correct_door:
        if current_level == 2:
            win.destroy()
            root.deiconify()
            show_treasure_window()
        else:
            tmsg.showinfo("Level Cleared", "Congrats you have made it to the next level")
            win.destroy()
            start_game(level=2)
    else:
        win.destroy()
        root.deiconify()
        show_game_over_window()


def show_door():
    canvas = root.winfo_children()[4].winfo_children()[0]
    canvas.delete('all')
    canvas.create_text(360, 30, text="Pick a Door", font=("Arial", 20, 'bold'), fill='red', activefill='yellow')
    canvas.create_text(360, 210, text=f"Level {current_level}", font=("Arial", 20, 'bold'), fill='blue')
    if current_level == 1:
        img_path = 'assets/door1.png'
    elif current_level == 2:
        img_path = 'assets/door2.png'
    door_img = Image.open(img_path)
    door_img = ImageTk.PhotoImage(door_img)
    canvas.image = door_img
    canvas.create_image(360, 220, image=door_img)
    win = root.winfo_children()[4]
    win.winfo_children()[1].destroy()
    doorone_btn = Button(win, text="Pick", command=lambda: pick_door(1), bg='red', fg='yellow', font=("Arial", 14, 'bold'), width=17)
    doortwo_btn = Button(win, text="Pick", command=lambda: pick_door(2), bg='red', fg='yellow', font=("Arial", 14, 'bold'), width=17)
    doorone_btn.place(x=20, y=452, anchor='w')
    doortwo_btn.place(x=702, y=452, anchor='e')


def start_game(level):
    global current_level
    current_level = level
    story = None
    img_path = None
    root.withdraw()
    win = Toplevel(root)
    win.geometry(WIN_SIZE)
    win.resizable(False, False)
    canvas = Canvas(win, bg=BG_COLOR, width=720, height=480)
    if level == 1:
        img_path = 'assets/bg3.jpg'
        story = get_story(level=1)
    elif level == 2:
        img_path = 'assets/bg4.jpg'
        story = get_story(level=2)
    bg_img = Image.open(img_path)
    bg_img = ImageTk.PhotoImage(bg_img)
    canvas.image = bg_img
    canvas.create_image(0, 0, image=bg_img, anchor=NW)
    canvas.create_text(350, 40, text=f"Level {current_level}", fill='yellow', font=("Arial", 18, 'bold'),
                       justify='center', activefill='white')
    canvas.create_text(350, 175, text=story, fill='red', font=("Arial", 13, 'bold'), justify='center',
                       tags='story', activefill='white')
    cont_btn = Button(win, text="Continue", bg='red', fg='yellow', font=("Arial", 14, 'bold'), command=show_door)
    cont_btn.pack(fill='x', side='bottom')
    canvas.pack()
    win.mainloop()


if __name__ == '__main__':
    current_level = 1
    root = Tk()
    WIN_SIZE = "720x480+360+200"
    GAME_TITLE = "Adventure Game"
    BG_COLOR = "skyblue"
    root.geometry(WIN_SIZE)
    root.title(GAME_TITLE)
    root.config(bg=BG_COLOR)
    root.resizable(False, False)
    title_label = Label(root, text=GAME_TITLE.upper(), bg=BG_COLOR, font=('Arial', 40))
    title_label.pack(pady=30)

    play_btn = Button(root, text="Play", bg='red', fg="yellow", font=('Arial', 20), width=15, command=lambda: start_game(level=1))
    play_btn.pack(pady=20)

    help_btn = Button(root, text="Help", bg='red', fg="yellow", font=('Arial', 20), width=15, command=show_help)
    help_btn.pack()

    exit_btn = Button(root, text="Exit", bg='red', fg="yellow", font=('Arial', 20), width=15, command=sys.exit)
    exit_btn.pack(pady=20)

    root.mainloop()

