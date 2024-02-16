#!/usr/bin/env python3.11

from tkinter import *
import random, sys, os
from pathlib import Path

GAME_WIDTH = 630
GAME_HEIGHT = 630
SPEED = 250
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "wheat"
FOOD_COLOR = "brown"
BACKGROUND_COLOR = "tan"

# global but !constant
canvas = None
label = None
window = None
score = 0
direction = 'down'
times = 0
mode = "first"


# main function begins here
def main():
    
    global canvas
    global label
    global window
    global score
    global direction
    global times

    window = Tk()
    window.title("Snake Game - Galakpai Gates")
    window.resizable(False, False)

    label = Label(window, text=f"Score = {score}", font=('consolas', 25))
    label.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
    canvas.pack()
    
    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    snake = Snake()
    food = Food()

    next_turn(snake, food)

    window.mainloop()

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE 
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        
def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # check if the snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:

        # update score
        global score
        score += 1
        label.config(text="Score = {}".format(score))

        # update food
        canvas.delete('food')
        food = Food()

        # increase the speed by 5 after the everytime the user reaches a multiple of ten
        if score != 0 and score % 5 == 0:
            global SPEED

            if SPEED <= 69:
                SPEED -= 8
            elif SPEED >= 70 and SPEED <= 100:
                SPEED -= 12
            else:
                SPEED -= 30
        
        # do not delete the last body part to create the illusion of the snake growing longer

    else:
        # delete the snake's last body part
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # check if the snake hit the edges or itself
    if check_collisions(snake):
        game_over()
    else:
        # otherwise, continue the game
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2.25, font=('consolas', 30), text="THERE WAS A COLLISION!", fill="red", tag="gameover")
    replay_btn = Button(canvas, height=1, width=10, text="Replay", font=('consolas', 25), bg=SNAKE_COLOR, activebackground=SNAKE_COLOR, command=replay)
    
    replay_btn.place(x=GAME_WIDTH/3, y=canvas.winfo_height()/2)
    
def replay():

    # rerun the entire program
    py_interpreter = sys.executable
    os.execl(py_interpreter, py_interpreter, *sys.argv)


if __name__ == "__main__":
    main()
