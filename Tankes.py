from tkinter import *
import time as t
import math as math
from random import *

delta_x = 0
delta_y = 0
InGame = True
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800
TANK_WIDTH = 217
TANK_HEIGHT = 127

USSR_TANK_WIDTH = 119
USSR_TANK_HEIGHT = 192

USSR_TANK_X = 500
USSR_TANK_Y = 700

MISSLE_WIDTH = 41
MISSLE_HEIGHT = 57

TANK_SPEED = 2
MISSLE_SPEED = 5

USSR_TANK_X_1 = 500
USSR_TANK_Y_1 = 700

Missles_images1 = "d:\\USERDATA\\Gleb\\Python\\Training\\res\\MissleNew.png"
Missles_images2 = "d:\\USERDATA\\Gleb\\Python\\Training\\res\\MissleNew2.png"
Missles_images3 = "d:\\USERDATA\\Gleb\\Python\\Training\\res\\MissleNew3.png"
tk = Tk()
tk.title("Game")
tk.wm_attributes("-topmost")
canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bd=1, bg='white')
R_dETH = 20
# It`s our GLOBALS
canvas.pack()

# список текущих выпущенных ракет
missles = []
tanks = []


class Coords:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tank:
    coords = Coords(0, 0)
    radius = 0
    picPath = "d:\\USERDATA\\Gleb\\Python\\Training\\res\\default.png"
    photoImage = PhotoImage(file=picPath)
    is_forward = True

    # tankImage = canvas.create_image(coords.x, coords.y, image=photoImage)

    def __init__(self, coords, radius, pic, loc_canvas):
        self.canvas = loc_canvas
        self.coords = coords
        self.radius = radius
        self.picPath = pic
        self.photoImage = PhotoImage(file=pic)
        self.tankImage = self.canvas.create_image(self.coords.x, self.coords.y, image=self.photoImage)

    def clear(self):
        self.canvas.delete(self.tankImage)

    def explose(self):
        self.canvas.delete(self.tankImage)

        expImage = PhotoImage(file='d:\\USERDATA\\Gleb\\Python\\Training\\res\\Bang.png')
        self.canvas.create_image(self.coords.x, self.coords.y, image=expImage)
        self.canvas.delete(expImage)

        tk.update()
        t.sleep(1)

    def draw(self):
        # self.canvas.delete(self.tankImage)
        # print(self.tankImage)
        self.tankImage = self.canvas.create_image(self.coords.x, self.coords.y, image=self.photoImage)

    def go(self, delta_x, delta_y):
        if self.is_forward and self.coords.x + delta_x > CANVAS_WIDTH:
            self.is_forward = False

        if not self.is_forward and self.coords.x - delta_x < 0:
            self.is_forward = True

        if self.is_forward and self.coords.y + delta_y > CANVAS_HEIGHT:
            self.is_forward = False

        if not self.is_forward and self.coords.y - delta_y < 0:
            self.is_forward = True

        if self.is_forward:
            self.coords.x = self.coords.x + delta_x
            self.coords.y = self.coords.y + delta_y
            self.canvas.move(self.tankImage, delta_x, delta_y)
        else:
            self.coords.x = self.coords.x - delta_x
            self.coords.y = self.coords.y - delta_y
            self.canvas.move(self.tankImage, -delta_x, -delta_y)
        USSR_TANK_X = delta_x
        USSR_TANK_Y = delta_y


def calc_distance(x1, y1, x2, y2):
    c = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return c


class Missle:
    def __init__(self, coords, image, loc_canvas):
        self.canvas = loc_canvas
        self.coords = coords
        self.image = PhotoImage(file=image)
        self.direction = -1
        self.MissleImage = self.canvas.create_image(self.coords.x, self.coords.y, image=self.image)

    def fly(self, delta_x, delta_y):
        self.coords.x = self.coords.x + self.direction * delta_x
        self.coords.y = self.coords.y + self.direction * delta_y
        # print("Missle Coords (%d, %d)" % (self.coords.x, self.coords.y))
        self.canvas.move(self.MissleImage, self.direction * delta_x, self.direction * delta_y)

    def clear(self):
        self.canvas.delete(self.MissleImage)

    def check_is_tank_in_zone(self, tank):
        distance = calc_distance(self.coords.x + MISSLE_WIDTH / 2, self.coords.y, tank.coords.x + TANK_WIDTH / 2,
                                 tank.coords.y + TANK_HEIGHT / 2)
        if distance < tank.radius:
            print("DESTROYED!!!")
            return True
        else:
            # print(distance)
            return False

    def is_missle_in_battle_field(self):
        if self.coords.x > 0 and self.coords.x < CANVAS_WIDTH and self.coords.y > 0 and self.coords.y < CANVAS_HEIGHT:
            return True
        else:
            return False


tankUSSR = Tank(Coords(USSR_TANK_X, USSR_TANK_Y), TANK_WIDTH / 2,
                'd:\\USERDATA\\Gleb\\Python\\Training\\res\\USSRTank.png', canvas)
tankDeutsch1 = Tank(Coords(30, 150), TANK_WIDTH / 2, 'd:\\USERDATA\\Gleb\\Python\\Training\\res\\GermanTank.png',
                    canvas)
tankDeutsch2 = Tank(Coords(30, 350), TANK_WIDTH / 2, 'd:\\USERDATA\\Gleb\\Python\\Training\\res\\GermanTank.png',
                    canvas)
USSR_TANK_X_Y_2 = canvas.coords(tankUSSR)

tanks.append(tankDeutsch1)
tanks.append(tankDeutsch2)


def Bang(event):
    global USSR_TANK_X
    if event.keysym == 'Up':
        new_missle = Missle(Coords(USSR_TANK_X, USSR_TANK_Y - 60),
                            "d:\\USERDATA\\Gleb\\Python\\Training\\res\\MissleNew.png", canvas)
        missles.append(new_missle)
    elif event.keysym == 'Left':
        if (USSR_TANK_X - 5 > USSR_TANK_WIDTH/2):
            USSR_TANK_X = USSR_TANK_X - 5
            tankUSSR.go(-5, 0)
        tk.update()
        t.sleep(0.01)
    elif event.keysym == 'Right':
        if (USSR_TANK_X + 5 < CANVAS_WIDTH - USSR_TANK_WIDTH/2):
            tankUSSR.go(5, 0)
            USSR_TANK_X = USSR_TANK_X + 5
        tk.update()
        t.sleep(0.01)
    else:
        pass


canvas.bind_all('<KeyPress-Up>', Bang)
canvas.bind_all('<KeyPress-Left>', Bang)
canvas.bind_all('<KeyPress-Right>', Bang)

while InGame:

    for current_missle in missles:
        current_missle.fly(0, MISSLE_SPEED)

    for current_tank in tanks:
        current_tank.go(TANK_SPEED + randint(1, 4), 0)
        for current_missle in missles:
            if current_missle.check_is_tank_in_zone(current_tank):
                if len(tanks) == 1:
                    InGame = False
                    canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, fill='red',
                                       font="Times 20 italic bold",
                                       text="GAME OVER!!!\n YOU WIN!")
                current_missle.clear()
                current_tank.explose()
                tanks.remove(current_tank)
                missles.remove(current_missle)
                break

            if not current_missle.is_missle_in_battle_field():
                print("Ракета улетела за пределы !")
                current_missle.clear()
                missles.remove(current_missle)

    tk.update()
    t.sleep(0.01)

# canvas.mainloop()
