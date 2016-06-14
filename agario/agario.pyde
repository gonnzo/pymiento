#########################################################
#
# The Pymiento Project
# Idea: Agar.io simulation
# Description: Bigger balls eat the smaller ones. The red balls, the splitters, blow white balls up keeping similar mass.
# Autor: Iván Gonzalo Moyano Pérez
#
#########################################################


class ballUniverse(object):

    def __init__(self):
        self.Balls = []
        self.amount = 30
        self.splitter_amount = 5

        for i in range(0, self.amount):
            self.Balls.append(Ball(self))

        for i in range(0, self.splitter_amount):
            self.Balls.append(Ball(self, 'splitter', '', '', 20, 0))


class Ball(object):

    def __init__(self, parent, splitter='', x='', y='', diam='', safe=''):

        self.direction = [-1, 1]
        self.parent = parent
        self.diam = random(20, 50)
        self.step = random(2, 3)
        self.dir_x = self.direction[int(random(0, 2))]
        self.dir_y = self.direction[int(random(0, 2))]
        self.deg_x = random(0, 2)
        self.deg_y = random(0, 2)
        self.x = random(50, width)
        self.y = random(50, height)
        self.id = random(0, 10000)
        self.splitter = splitter
        self.safe = 50
        self.growTo = 0

        if(x != ''):
            self.x = x
        if(y != ''):
            self.y = y
        if(diam != ''):
            self.diam = diam
        if(safe != ''):
            self.safe = safe

    def isCollision(self, b1, b2):

        return sqrt((b1.x - b2.x) * (b1.x - b2.x) + (b1.y - b2.y) * (b1.y - b2.y)) < b1.diam / 2 + b2.diam / 2

    def splitBall(self, b1):

        diam = b1.diam

        for n in range(1, 100):
            nro = n
            if diam / nro < 20:
                break
        x = self.x
        y = self.y
        diam = diam / nro

        for j in range(0, nro):
            self.parent.Balls.append(Ball(self.parent, '', x, y, diam, 100))

        self.parent.Balls.remove(b1)
        background("#ff0000")

    def run(self):

        if(self.safe > 0):
            self.safe -= 1

        for i in range(0, len(self.parent.Balls)):

            if(self.id != self.parent.Balls[i].id and self.isCollision(self, self.parent.Balls[i]) and self.safe == 0 and self.parent.Balls[i].safe == 0 and self.splitter == '' and self.parent.Balls[i].splitter == ''):

                if(self.parent.Balls[i].diam < self.diam):

                    self.growTo += self.parent.Balls[i].diam
                    self.parent.Balls.remove(self.parent.Balls[i])
                else:
                    self.parent.Balls[i].growTo += self.diam
                    self.parent.Balls.remove(self)

                break

            elif(self.id != self.parent.Balls[i].id and self.safe == 0 and self.parent.Balls[i].safe == 0 and self.isCollision(self, self.parent.Balls[i])):

                self.splitBall(
                    self.parent.Balls[i] if(self.splitter == 'splitter') else self)

                break

        fill(("#333333" if self.safe > 0 else (
            "#ffffff" if self.splitter == '' else '#ff0000')))

        ellipse(self.x, self.y, self.diam, self.diam)

        if(self.growTo > 0):
            self.growTo -= 2
            self.diam += 2

        if(self.x > width - self.diam / 2):
            self.dir_x = -1
        if(self.y > height - self.diam / 2):
            self.dir_y = -1

        if(self.x < self.diam / 2):
            self.dir_x = 1
        if(self.y < self.diam / 2):
            self.dir_y = 1

        self.x = self.x + \
            ((self.step + self.safe / 10) * self.deg_x) * self.dir_x
        self.y = self.y + \
            ((self.step + self.safe / 10) * self.deg_y) * self.dir_y


def setup():

    global bU
    fullScreen(P2D, 2)
    noStroke()
    bU = ballUniverse()


def draw():

    background(0)
    for i in range(0, len(bU.Balls)):
        if(i >= len(bU.Balls)):
            break
        bU.Balls[i].run()
