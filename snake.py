# SNAKE MAIN OBJECTS

import math, random, pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
        width_length = 600
        rows = 20

        def __init__(self, start, direction_x = 1, direction_y = 0, color=(255, 0, 0)):
                self.position = start
                self.direction_x = 1
                self.direction_y = 0
                self.color = color

        def move(self, direction_x, direction_y,):
                self.direction_x = direction_x
                self.direction_y = direction_y
                self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

        def draw(self, surface, head = False):
                dis = self.width_length // self.rows
                row_i = self.position[0]
                column_j = self.position[1]  

                pygame.draw.rect(surface, self.color, (row_i * dis + 1, column_j * dis + 1, dis - 2, dis - 2))

                if head:
                        centre = dis // 2
                        radius = 3
                        circleMiddle = (row_i * dis + centre - radius, column_j * dis + 8)
                        circleMiddle2 = (row_i * dis + dis - radius * 2, column_j * dis + 8)

                        pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
                        pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake_player(object):
        body_cubes = []
        turns_direction = {}

        def __init__(self, color, position):
                self.color = color
                self.head = cube(position)
                self.body_cubes.append(self.head) 
                self.direction_x = 0
                self.direction_y = 1

        def move(self):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()

                        keys = pygame.key.get_pressed()

                        for key in keys:
                                if keys[pygame.K_LEFT]:
                                        self.direction_x = -1 
                                        self.direction_y = 0
                                        self.turns_direction[self.head.position[:]] = [self.direction_x, self.direction_y]

                                elif keys[pygame.K_RIGHT]:
                                        self.direction_x = 1 
                                        self.direction_y = 0
                                        self.turns_direction[self.head.position[:]] = [self.direction_x, self.direction_y]

                                elif keys[pygame.K_UP]:
                                        self.direction_x = 0
                                        self.direction_y = -1
                                        self.turns_direction[self.head.position[:]] = [self.direction_x, self.direction_y]

                                elif keys[pygame.K_DOWN]:
                                        self.direction_x = 0
                                        self.direction_y = 1
                                        self.turns_direction[self.head.position[:]] = [self.direction_x, self.direction_y]

                for i, c in enumerate(self.body_cubes):
                        p = c.position[:]
                        if p in self.turns_direction:
                                turn = self.turns_direction[p]
                                c.move(turn[0], turn[1])

                                if i == len(self.body_cubes)-1:
                                        self.turns_direction.pop(p)
                        # snake moviment on the edges
                        else:
                                if c.direction_x == -1 and c.position[0] <= 0:
                                        c.position = (c.rows-1, c.position[1])
                                elif c.direction_y == 1 and c.position[1] >= c.rows-1:
                                        c.position = (c.position[0], 0)
                                elif c.direction_x == 1 and c.position[0] >= c.rows-1:
                                        c.position = (0, c.position[1])
                                elif c.direction_y == -1 and c.position[1] <= 0:
                                        c.position = (c.position[0], c.rows-1)
                                else:
                                        c.move(c.direction_x, c.direction_y)                             

        def reset(self, position):
                self.head = cube(position) 
                self.body_cubes = []
                self.body_cubes.append(self.head)
                self.turns_direction = {}
                self.direction_x = 0
                self.direction_y = 1

        def add_snack(self):
                tail = self.body_cubes[-1]
                dx, dy = tail.direction_x, tail.direction_y 

                if dx == 1 and dy == 0:
                        self.body_cubes.append(cube((tail.position[0]-1, tail.position[1])))
                elif dx == -1 and dy == 0:
                        self.body_cubes.append(cube((tail.position[0]+1, tail.position[1])))
                elif dx == 0 and dy == 1:
                        self.body_cubes.append(cube((tail.position[0], tail.position[1]-1)))
                elif dx == 0 and dy == -1:
                        self.body_cubes.append(cube((tail.position[0], tail.position[1]+1)))

                self.body_cubes[-1].direction_x = dx
                self.body_cubes[-1].direction_y = dy
        
        def draw(self, surface):
                for i, c in enumerate(self.body_cubes):
                        if i == 0:
                                c.draw(surface, True)
                        else:
                                c.draw(surface)

def draw_grid(width_length, rows, surface):
        size_between = width_length // rows 

        x, y = 0, 0

        for i in range(rows):
                x = x + size_between
                y = y + size_between

                pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width_length))
                pygame.draw.line(surface, (255, 255, 255), (0, y), (width_length, y))

def redraw_window(surface):
        global rows, width, snake, snack

        surface.fill((0, 0, 0))
        snake.draw(surface)
        snack.draw(surface)
        draw_grid(width, rows, surface)
        pygame.display.update()

def random_snack(rows, item):
        positions = item.body_cubes

        while True:
                x = random.randrange(rows) 
                y = random.randrange(rows) 

                if len(list(filter(lambda z: z.position == (x,y), positions))) > 0:
                        continue
                else:
                        break

        return (x,y)

def message_box(subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
                root.destroy()
        except:
                pass 

def main():
        global width, rows, snake, snack

        # better if width % 2 == 0 and has a square window
        width, height = 600, 600
        rows = 20

        main_window = pygame.display.set_mode((width, height))
        snake = snake_player((255, 0, 0), (10, 10))
        snack = cube(random_snack(rows, snake), color = (0, 255, 0))

        # flag = True
        clock = pygame.time.Clock()

        # snake moviment velocity
        while True:
                pygame.time.delay(50)   # low this number for faster moviments
                clock.tick(10)          # low this number for lower the moviment

                snake.move()
                if snake.body_cubes[0].position == snack.position:
                        snake.add_snack()
                        snack = cube(random_snack(rows, snake), color = (0, 255, 0))

                for i in range(len(snake.body_cubes)):
                        if snake.body_cubes[i].position in list(map(lambda z:z.position, snake.body_cubes[i+1:])):
                                print('score: ', len(snake.body_cubes))
                                message_box('you lost', 'play again...')

                                snake.reset((10, 10))
                                break

                redraw_window(main_window)

        pass 


main()