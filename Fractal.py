import pygame as g
from pygame.locals import *
import sys, math

global DEPTH, RES
RES = (500, 500) #trenutno mora bit kvadrat
DEPTH = 100
view = ((-2, -2), (2, 2)) #leva spodnja in desna zgornja koord.


def scalexy(x, y, res, view):
    x = x / res[0] * (view[1][0] - view[0][0]) + view[0][0]
    y = y / res[1] * (view[1][1] - view[0][1]) + view[0][1]
    return x, y

def f(x,y):
    """vrne po koliko korakih pobegne 2-okolici (0,0). max Depth korakov"""
    z = complex(x, y)
    z0 = z
    for step in range(DEPTH):
        z = z**2+z0
        if abs(z) > 2:
            return step
    return "konv"

def zoom_in(view, pos):
    """view je ((,),(,)). pos je (x,y)
    vrne nov view"""
    zoom_factor = 8
    dx = (view[1][0] - view[0][0]) / zoom_factor
    dy = (view[1][1] - view[0][1]) / zoom_factor
    pos = scalexy(pos[0], pos[1], RES, view)
    return ((pos[0] - dx/2, pos[1] - dy/2), (pos[0] + dx/2, pos[1] + dy/2))


def zoom_out(view, pos):
    zoom_factor = 8
    dx = (view[1][0] - view[0][0]) * zoom_factor
    dy = (view[1][1] - view[0][1]) * zoom_factor
    pos = scalexy(pos[0], pos[1], RES, view)
    return ((pos[0] - dx / 2, pos[1] - dy / 2), (pos[0] + dx / 2, pos[1] + dy / 2))

def coloring(steps):
    """vrne (r,g,b)"""
    c = steps/DEPTH
    if c <= 0.167:
        return (0, 0, 200 * (1 - 6 * c))
    elif 0.167 < c <= 0.333:
        return (0, 200 * (6 * c - 1), 0)
    elif 0.333 < c <= 0.5:
        return (0, 200 * (3 - 6 * c), 0)
    elif 0.5 < c <= 0.667:
        return (200 * (6 * c - 3), 200 * (6 * c - 3), 0)
    elif 0.667 < c <= 0.833:
        return (200 * (5 - 6 * c), 200 * (5 - 6 * c), 0)
    return (200 * (6 * c - 5), 0, 0)


def draw(main, RES, view):
    for y in range(RES[1]): #x,y so koordinate za resolucijo. xx, yy so koordinate za računat barvo
        for x in range(RES[0]):
            xx, yy = scalexy(x, y, RES, view)
            steps = f(xx,yy)
            if steps == "konv":
                color = (0, 0, 0)
            else:
                color = coloring(steps)

            main.set_at((x, y), color)


g.init()
main = g.display.set_mode(RES)
draw(main, RES, view)
g.display.update()

while 1:
    e = g.event.wait()
    if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
        g.quit()
        sys.exit()
    elif e.type == MOUSEBUTTONDOWN and g.mouse.get_pressed()[0]:
        view = zoom_in(view, g.mouse.get_pos())
        print(view)
        draw(main, RES, view)
        g.display.update()
    elif e.type == MOUSEBUTTONDOWN and g.mouse.get_pressed()[2]:
        view = zoom_out(view, g.mouse.get_pos())
        print(view)
        draw(main, RES, view)
        g.display.update()