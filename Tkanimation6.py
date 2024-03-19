from tkinter import *
from TkinterMeth import move, draw
from random import randrange
import time
from math import sqrt

def movemanual(event):
    global after_id, running, j, dimension, space, track, t
    t += 1
    timer[t % 2] = time.time()
    if timer[t % 2] - timer[t % 2 - 1] > 0.015 * speed:
        if event.keysym == "Left":
            if track[0][j - 1] != "Right":
                for i in after_id:
                    if i:
                        window1.after_cancel(i)
                if len(track[0]) != 0:
                    temp = track[0][j - 1]
                    if event.keysym != temp:
                        for i in range(0, space):
                            track[0].append(temp)
                running = [True, False, False, False]
                after_id[1] = window1.after(speed, moveleft())
        if event.keysym == "Right":
            if track[0][j - 1] != "Left":
                for i in after_id:
                    if i:
                        window1.after_cancel(i)
                if len(track[0]) != 0:
                    temp = track[0][j - 1]
                    if event.keysym != temp:
                        for i in range(0, space):
                            track[0].append(temp)
                running = [False, True, False, False]
                after_id[1] = window1.after(speed, moveright())
        if event.keysym == "Up":
            if track[0][j - 1] != "Down":
                for i in after_id:
                    if i:
                        window1.after_cancel(i)
                if len(track[0]) != 0:
                    temp = track[0][j - 1]
                    if event.keysym != temp:
                        for i in range(0, space):
                            track[0].append(temp)
                running = [False, False, True, False]
                after_id[1] = window1.after(speed, moveup())
        if event.keysym == "Down":
            if track[0][j - 1] != "Up":
                for i in after_id:
                    if i:
                        window1.after_cancel(i)
                if len(track[0]) != 0:
                    temp = track[0][j - 1]
                    if event.keysym != temp:
                        for i in range(0, space):
                            track[0].append(temp)
                running = [False, False, False, True]
                after_id[1] = window1.after(speed, movedown())

def moveleft():
    global track, after_id, j, dimension
    movement = move(can1, coo, snake)
    movement.left(0)
    if len(track[0]) - j == 0:
        track[0].append("Left")
    recurse(1, track)
    collision(dimension)
    eat()
    if running[0]:
        if after_id[0]:
           window1.after_cancel(after_id[0])
        after_id[0] = window1.after(speed, moveleft)

def moveright():
    global track, after_id, j, dimension
    movement = move(can1, coo, snake)
    movement.right(0)
    if len(track[0]) - j == 0:
        track[0].append("Right")
    recurse(1, track)
    collision(dimension)
    eat()
    if running[1]:
        if after_id[0]:
           window1.after_cancel(after_id[0])
        after_id[0] = window1.after(speed, moveright)

def moveup():
    global track, after_id, j, dimension
    movement = move(can1, coo, snake)
    movement.up(0)
    if len(track[0]) - j == 0:
        track[0].append("Up")
    recurse(1,  track)
    collision(dimension)
    eat()
    if running[2]:
        if after_id[0]:
           window1.after_cancel(after_id[0])
        after_id[0] = window1.after(speed, moveup)

def movedown():
    global track, after_id, j, dimension
    movement = move(can1, coo, snake)
    movement.down(0)
    if len(track[0]) - j == 0:
        track[0].append("Down")
    recurse(1, track)
    collision(dimension)
    eat()
    if running[3]:
        if after_id[0]:
           window1.after_cancel(after_id[0])
        after_id[0] = window1.after(speed, movedown)

def recurse(p, track):
    global j, space
    movement = move(can1, coo, snake)
    if track[p - 1][j] != track[p - 1][j - 1]:
        if p != len(track):
            for i in range(0, space):
                track[p].append(track[p - 1][j - 1])
    if track[p - 1][j] == "Left":
        movement.left(p)
        if p != len(track) and len(track[p]) - j == 0:
            track[p].append("Left")
    if track[p - 1][j] == "Right":
        movement.right(p)
        if p != len(track) and len(track[p]) - j == 0:
            track[p].append("Right")
    if track[p - 1][j] == "Up":
        movement.up(p)
        if p != len(track) and len(track[p]) - j == 0:
            track[p].append("Up")
    if track[p - 1][j] == "Down":
        movement.down(p)
        if p != len(track) and len(track[p]) - j == 0:
            track[p].append("Down")
    p += 1
    if p != len(coo) and track[p - 1]:
        recurse(p, track)
    else:
       j += 1

def stop(event):
    global running
    running = [False, False, False, False]

def collision(dimension):
    global running
    rad = draw(can1, dimension, coo, snake)
    radius = sqrt((coo[0][0] - coo[0][2]) ** 2 + (coo[0][1] - coo[0][3]) ** 2) // 2
    if rad.select((coo[0][0] + coo[0][2]) // 2, (coo[0][1] + coo[0][3]) // 2, radius) != len(coo) and rad.select((coo[0][0] + coo[0][2]) // 2, (coo[0][1] + coo[0][3]) // 2, radius) != 0 and rad.select((coo[0][0] + coo[0][2]) // 2, (coo[0][1] + coo[0][3]) // 2, radius) != 1:
        running = [False, False, False, False]

def food():
    global a, b
    radius = sqrt((coo[0][0] - coo[0][2]) ** 2 + (coo[0][1] - coo[0][3]) ** 2) // 2
    a, b = randrange(dimension // 50, dimension * 49 // 50 - radius), randrange(dimension // 50, dimension * 49 // 50 - radius) 
    can1.coords(foods, a - radius, b - radius, a + radius, b + radius)

def eat():
    global n, speed, a, b
    if sqrt((a - coo[0][0])**2 + (b - coo[0][1])**2) < (sqrt((coo[0][0] - coo[0][2]) ** 2 + (coo[0][1] - coo[0][3]) ** 2) // 2) * 2:
        food()
        if len(track[len(track) - 1]) - len(track[len(track) - 1][:j - 1]) == 1:
            extend()
            if speed > 0:
                speed -= 1

def extend():
    global j
    temp = track[len(track) - 1][len(track[len(track) - 1]) - 1]
    if temp == "Left":
        coo.append([coo[len(coo) - 1][0] + space, coo[len(coo) - 1][1], coo[len(coo) - 1][2] + space, coo[len(coo) - 1][3]])
        snake.append([can1.create_line(coo[len(coo) - 1], width = dimension / 50)])
    elif temp == "Right":
        coo.append([coo[len(coo) - 1][0] - space, coo[len(coo) - 1][1], coo[len(coo) - 1][2] - space, coo[len(coo) - 1][3]])
        snake.append([can1.create_line(coo[len(coo) - 1], width = dimension / 50)])
    elif temp == "Up":
        coo.append([coo[len(coo) - 1][0], coo[len(coo) - 1][1] + space, coo[len(coo) - 1][2], coo[len(coo) - 1][3] + space])
        snake.append([can1.create_line(coo[len(coo) - 1], width = dimension / 50)])
    elif temp == "Down":
        coo.append([coo[len(coo) - 1][0], coo[len(coo) - 1][1] - space, coo[len(coo) - 1][2], coo[len(coo) - 1][3] - space])
        snake.append([can1.create_line(coo[len(coo) - 1], width = dimension / 50)])
    track.append(track[len(track) - 1])
    track[len(track) - 1] = track[len(track) - 1][:j - 1]
    for i in range(0, space):
        track[len(track) - 1].append(temp)

timer = [0, 0]
dimension, color, j, n, t, speed, a, b = 500, "white", 0, 5, 0, 20, 0, 0
space = dimension // 38
x, y =  randrange(dimension // 50, dimension * 49 // 50), randrange(dimension // 50, dimension * 49 // 50)

window1 = Tk()
can1 = Canvas(window1, width = dimension, height = dimension, bg = color)
can1.pack()
coo, snake, track, after_id, running = [], [], [], [None, None], [False, False, False, False]

foods = can1.create_oval(a, b, a, b, outline = "red", fill = "red")

if x < dimension // 2 and y < dimension // 2:
    if randrange(0, 2) == 1:
        for i in range(-n + 1, 1):
            coo.append([x + space * - i, y, -i * space + x + dimension / 50, y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension // 50)])
            if i < 0:
                track.append([])
        running = [False, True, False, False]
        moveright()
    else:
        for i in range(-n + 1, 1):
            coo.append([x, y + space * -i, x + dimension / 50, -i * space + y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension / 50)])
            if i < 0:
                track.append([])
        running = [False, False, False, True]
        movedown()
elif x > dimension // 2 and y > dimension // 2:
    if randrange(0, 2) == 1:
        for i in range(-n + 1, 1):
            coo.append([x + space * i, y, i * space + x + dimension / 50, y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension / 50)])
            if i < 0:
                track.append([])
        running = [True, False, False, False]
        moveleft()
    else:
        for i in range(-n + 1, 1):
            coo.append([x, y + space * i, x + dimension / 50, i * space + y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension / 50)])
            if i < 0:
                track.append([])
        running = [False, False, True, False]
        moveup()
elif x > dimension // 2 and y < dimension // 2:
    if randrange(0, 2) == 1:
        for i in range(-n + 1, 1):
            coo.append([x + space * i, y, i * space + x + dimension / 50, y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension / 50)])
            if i < 0:
                track.append([])
        running = [True, False, False, False]
        moveleft()
    else:
        for i in range(-n + 1, 1):
            coo.append([x, y + space * -i, x + dimension / 50, -i * space + y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension / 50)])
            if i < 0:
                track.append([])
        running = [False, False, False, True]
        movedown()
elif x <= dimension // 2 and y >= dimension // 2:
    if randrange(0, 2) == 1:
        for i in range(-n + 1, 1):
            coo.append([x + space * - i, y, -i * space + x + dimension / 50, y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension // 50)])
            if i < 0:
                track.append([])
        running = [False, True, False, False]
        moveright()
    else:
        for i in range(-n + 1, 1):
            coo.append([x, y + space * i, x + dimension / 50, i * space + y])
            snake.append([can1.create_line(coo[n - 1 + i], width = dimension / 50)])
            if i < 0:
                track.append([])
        running = [False, False, True, False]
        moveup()
food()

window1.bind("<Key-Up>", movemanual)
window1.bind("<Key-Down>", movemanual)
window1.bind("<Key-Left>", movemanual)
window1.bind("<Key-Right>", movemanual)
window1.bind("<Return>", stop)

window1.mainloop()