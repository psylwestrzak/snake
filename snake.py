'''
snake.py Python 3.x
Simple snake game based on curses library
'''
from curses import wrapper
import curses
import copy
import time
import random

class Coordinates:

    x, y = 0, 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:

    elements_position = []

    def __init__(self):
        self.head_cords = Coordinates(0,0)
        self.elements_position.append(self.head_cords)
        self.snake_length = 1

    # Increase snake size in case of eating food
    def grow_snake(self):
        self.elements_position.append(copy.copy(self.elements_position[self.snake_length - 1]))
        self.snake_length += 1

    def move_snake(self, x, y):
        if x != 0 or y != 0: #dorobic ograniczenie wartosci
            for elementNumber in range(self.snake_length - 1):
                self.elements_position[elementNumber] = copy.copy(self.elements_position[elementNumber + 1])
            self.elements_position[self.snake_length - 1].x += x
            self.elements_position[self.snake_length - 1].y += y


class SnakeGame():
    food_pattern = '*'
    snake_pattern = '#'

    def __init__(self, stdscr):

        self.stdscr = stdscr
        self.stdscr.nodelay(1)
        self.snake = Snake()

        # default first food location
        self.food = Coordinates(3,3)

        # default movement direction is right (x-axis)
        self.movement_direction_x = 0
        self.movement_direction_y = 0

    def draw_gameplay(self):
        self.stdscr.clear()
        self.stdscr.addstr(self.food.y, self.food.x, self.food_pattern)

        for element in self.snake.elements_position:
            self.stdscr.addstr(element.y, element.x, self.snake_pattern)

        self.stdscr.addstr(5, 0, 'Score: ' + str(self.snake.snake_length - 1))

    def generate_food(self):
        self.food.x = random.randint(0, 4)
        self.food.y = random.randint(0, 4)

    def control_game(self):

        pressed_key_str = self.stdscr.getch()

        if pressed_key_str == curses.KEY_LEFT:
            self.movement_direction_x = -1
            self.movement_direction_y = 0

        elif pressed_key_str == curses.KEY_RIGHT:
            self.movement_direction_x = 1
            self.movement_direction_y = 0

        elif pressed_key_str == curses.KEY_UP:
            self.movement_direction_x = 0
            self.movement_direction_y = -1

        elif pressed_key_str == curses.KEY_DOWN:
            self.movement_direction_x = 0
            self.movement_direction_y = 1
        time.sleep(0.3)
        self.snake.move_snake(self.movement_direction_x, self.movement_direction_y)

        # generate food in case a previous one was eaten
        if self.snake.elements_position[0].x == self.food.x and self.snake.elements_position[0].y == self.food.y:
            self.snake.grow_snake()
            self.generate_food()


def main(stdscr):

    snake_game = SnakeGame(stdscr)

    while True:

        snake_game.control_game()
        snake_game.draw_gameplay()

wrapper(main)