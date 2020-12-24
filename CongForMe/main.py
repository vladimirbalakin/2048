import random
import json
from time import sleep

import pygame
from pygame import init, draw, event, display, QUIT, MOUSEBUTTONDOWN, MOUSEWHEEL, K_RIGHT, K_LEFT, K_UP, K_DOWN, KEYDOWN

init()

w, h = 640, 480
root = display.set_mode((w, h))
display.set_caption("2048 game")


class Polygon:
    cell_w, cell_h = 4, 4
    cell_width = 50
    built = 2
    new_choose = (-1, -1)
    score = 0
    best_score = 0

    def __init__(self, how_many_cells=4, width=50):
        self.cell_w = how_many_cells
        self.cell_h = how_many_cells
        self.cell_width = width
        self.numbers = [[-1 for i in range(self.cell_h)] for i in range(self.cell_w)]

    def redraw(self):
        root.fill((0, 0, 0))
        for ip, i in enumerate(self.numbers):
            for jp, j in enumerate(i):
                draw.rect(root, (255, 255, 255), ((ip * self.cell_width, jp * self.cell_width),
                                                  (self.cell_width, self.cell_width)), 1, 20)
                if j == -1:
                    continue
                font = pygame.font.SysFont(None, 24)
                img = font.render(str(j), True, 'RED')
                if (ip, jp) == self.new_choose:
                    img = font.render(str(j), True, 'BLUE')
                    self.new_choose = (-1, -1)
                root.blit(img, ((ip + 0.5) * self.cell_width, (jp + 0.5) * self.cell_width))
        font = pygame.font.SysFont(None, 50)
        img = font.render("Score: {}".format(self.score), True, 'RED')
        root.blit(img, ((len(self.numbers) + 1) * self.cell_width, 0))
        font = pygame.font.SysFont(None, 50)
        img = font.render("Best score: {}".format(self.best_score), True, 'RED')
        root.blit(img, ((len(self.numbers) + 1) * self.cell_width, 100))
        display.flip()

    def recalculate_best_score(self):
        with open("st.json", "r") as input_file:
            self.best_score = json.load(input_file)
        input_file.close()

        self.best_score = max(self.score, self.best_score)

        with open("st.json", "w") as output_file:
            json.dump(self.best_score, output_file)

    def shift(self, direction=0):
        ans = False
        if direction == 0:
            for i in range(self.cell_h):
                fl = False
                for j in range(self.cell_w):
                    if self.numbers[i][j] == -1:
                        continue
                    if fl:
                        fl = False
                        continue
                    for q in range(j + 1, self.cell_w):
                        if self.numbers[i][q] != -1:
                            if self.numbers[i][q] == self.numbers[i][j]:
                                self.numbers[i][q] += self.numbers[i][j]
                                self.numbers[i][j] = -1
                                self.score += self.numbers[i][q]
                                ans = True
                                fl = True
                            else:
                                c = self.numbers[i][j]
                                self.numbers[i][j] = -1
                                self.numbers[i][q - 1] = c
                            break
                    else:
                        c = self.numbers[i][j]
                        self.numbers[i][j] = -1
                        self.numbers[i][-1] = c
        elif direction == 2:
            for i in range(self.cell_h - 1, -1, -1):
                fl = False
                for j in range(self.cell_w - 1, -1, -1):
                    if self.numbers[i][j] == -1:
                        continue
                    if fl:
                        fl = False
                        continue
                    for q in range(j - 1, -1, -1):
                        if self.numbers[i][q] != -1:
                            if self.numbers[i][q] == self.numbers[i][j]:
                                self.numbers[i][q] += self.numbers[i][j]
                                self.numbers[i][j] = -1
                                self.score += self.numbers[i][q]
                                ans = True
                                fl = True
                            else:
                                c = self.numbers[i][j]
                                self.numbers[i][j] = -1
                                self.numbers[i][q + 1] = c
                            break
                    else:
                        c = self.numbers[i][j]
                        self.numbers[i][j] = -1
                        self.numbers[i][0] = c
        elif direction == 1:
            for i in range(self.cell_w):
                fl = False
                for j in range(self.cell_h):
                    if self.numbers[j][i] == -1:
                        continue
                    if fl:
                        fl = False
                        continue
                    for q in range(j + 1, self.cell_h):
                        if self.numbers[q][i] != -1:
                            if self.numbers[q][i] == self.numbers[j][i]:
                                self.numbers[q][i] += self.numbers[j][i]
                                self.numbers[j][i] = -1
                                self.score += self.numbers[q][i]
                                ans = True
                                fl = True
                            else:
                                c = self.numbers[j][i]
                                self.numbers[j][i] = -1
                                self.numbers[q - 1][i] = c
                            break
                    else:
                        c = self.numbers[j][i]
                        self.numbers[j][i] = -1
                        self.numbers[-1][i] = c
        elif direction == 3:
            for i in range(self.cell_h - 1, -1, -1):
                fl = False
                for j in range(self.cell_w - 1, -1, -1):
                    if self.numbers[j][i] == -1:
                        continue
                    if fl:
                        fl = False
                        continue
                    for q in range(j - 1, -1, -1):
                        if self.numbers[q][i] != -1:
                            if self.numbers[q][i] == self.numbers[j][i]:
                                self.numbers[q][i] += self.numbers[j][i]
                                self.numbers[j][i] = -1
                                self.score += self.numbers[q][i]
                                ans = True
                                fl = True
                            else:
                                c = self.numbers[j][i]
                                self.numbers[j][i] = -1
                                self.numbers[q + 1][i] = c
                            break
                    else:
                        c = self.numbers[j][i]
                        self.numbers[j][i] = -1
                        self.numbers[0][i] = c
        return ans

    def get_random_new_number(self):
        """Add new number to the polygon"""
        a = []
        for i in range(self.cell_h):
            for j in range(self.cell_w):
                if self.numbers[i][j] == -1:
                    a.append((i, j))
        if not a:
            # generate error
            error = 'Stack Overflow'
            display_error(error)
            return error
        chosen = random.choice(a)
        self.numbers[chosen[0]][chosen[1]] = self.built
        self.new_choose = chosen


# draw.circle(root, color, (x, y), 1, 1)

poly = Polygon()
poly.recalculate_best_score()
poly.redraw()

running = True


def display_error(error):
    global running
    root.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 50)
    img = font.render(error, True, 'RED')
    root.blit(img, (0, 0))
    display.flip()
    running = False


while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
            err = 'QUITING'
        if e.type == MOUSEBUTTONDOWN:
            print("DOWN")
        if e.type == MOUSEWHEEL:
            print("WHEEL")
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                poly.shift(1)
                err = poly.get_random_new_number()
                poly.redraw()
            if e.key == K_LEFT:
                poly.shift(3)
                err = poly.get_random_new_number()
                poly.redraw()
            if e.key == K_UP:
                poly.shift(2)
                err = poly.get_random_new_number()
                poly.redraw()
            if e.key == K_DOWN:
                poly.shift(0)
                err = poly.get_random_new_number()
                poly.redraw()
    display.flip()
    sleep(0.1)
display_error(err)
if err != 'QUITING':
    sleep(3)
poly.recalculate_best_score()
display.quit()
# You could understand nothing in this code because I have written it!
