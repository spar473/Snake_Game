import pygame
import random
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 10
    width = 300

    def __init__(self, start, x_direction=1, y_direction=0, colour=(0, 255, 0)):
        self.pos = start
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.colour = colour

    def move(self, x_direction, y_direction):
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.pos = (self.pos[0] + self.x_direction, self.pos[1] + self.y_direction)

    def draw(self, surface, eyes=False):
        size = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.colour, (i * size + 1, j * size + 1, size - 2, size - 2))
        if eyes:
            centre = size // 2
            radius = 3
            circleMiddle = (i * size + centre - radius, j * size + 8)
            circleMiddle2 = (i * size + size - radius * 2, j * size + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake(object):
    def __init__(self, colour, pos):
        self.colour = colour
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.x_direction = 0
        self.y_direction = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        for key in keys:
            if keys[pygame.K_LEFT]:
                self.x_direction = -1
                self.y_direction = 0
                self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

            elif keys[pygame.K_RIGHT]:
                self.x_direction = 1
                self.y_direction = 0
                self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

            elif keys[pygame.K_UP]:
                self.x_direction = 0
                self.y_direction = -1
                self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

            elif keys[pygame.K_DOWN]:
                self.x_direction = 0
                self.y_direction = 1
                self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.x_direction == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.x_direction == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.y_direction == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.y_direction == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.x_direction, c.y_direction)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.x_direction = 0
        self.y_direction = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.x_direction, tail.y_direction

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].x_direction = dx
        self.body[-1].y_direction = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(w, rows, surface):
    size_between = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redraw_window(surface, snake, snack):
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(snake.head.width, snake.head.rows, surface)
    pygame.display.update()

def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()

def main():
    width = 300
    rows = 10
    win = pygame.display.set_mode((width, width))
    s = Snake((0, 255, 0), (5, 5))
    snack = Cube(random_snack(rows, s), colour=(255, 0, 0))
    flag = True

    pygame.display.set_caption('Snake game by Sooyoung')
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), colour=(255, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                pygame.quit()
                message_box('You Lost!', 'Play again...')
                s.reset((5, 5))
                pygame.init()
                win = pygame.display.set_mode((width, width))
                break

        redraw_window(win, s, snack)

    pass

main()