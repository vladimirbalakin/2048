import random
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
                root.blit(img, ((ip + 0.5) * self.cell_width, (jp + 0.5) * self.cell_width))
                display.flip()

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


# draw.circle(root, color, (x, y), 1, 1)

poly = Polygon()
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
                if not poly.shift(1):
                    err = poly.get_random_new_number()
                poly.redraw()
            if e.key == K_LEFT:
                if not poly.shift(3):
                    err = poly.get_random_new_number()
                poly.redraw()
            if e.key == K_UP:
                if not poly.shift(2):
                    err = poly.get_random_new_number()
                poly.redraw()
            if e.key == K_DOWN:
                if not poly.shift(0):
                    err = poly.get_random_new_number()
                poly.redraw()
    display.flip()
    sleep(0.1)
display_error(err)
if err != 'QUITING':
    sleep(3)
display.quit()
# You could understand nothing in this code because I have written it!
