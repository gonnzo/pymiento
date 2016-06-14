#########################################################
#
# The Pymiento Project
# Idea: Agar.io simulation
# Description: Bigger balls eat the smaller ones. The red balls, the splitters, blow white balls up keeping similar mass.
# Autor: Iván Gonzalo Moyano Pérez
# Version: Normalizing classes
#
#########################################################


class ballUniverse(object):

    def __init__(self):

        self.NORMAL_COLOR = "#ffffff"
        self.SPLITTER_COLOR = "#ff0000"
        self.GAME_COLOR = "#ffcc00"
        self.SAFE_COLOR = "#333333"

        self.Balls = []
        self.amount = 20
        self.splitter_amount = 5

        for i in range(0, self.amount):
            self.appendBall()

        for i in range(0, self.splitter_amount):
            self.appendBall('splitter', '', '', 20, 0)

    def appendBall(self, kind='', x='', y='', diam='', safe=''):
        self.Balls.append(Ball(self, kind, x, y, diam, safe))

    def killBall(self, ball):
        self.Balls.remove(ball)

    def refreshUniverse(self):
        for i in range(0, len(self.Balls)):
            if(i >= len(self.Balls)):
                break
            self.Balls[i].run()


class Ball(object):

    def __init__(self, parent, kind='', x='', y='', diam='', safe=''):
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
        self.kind = 'normal'
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
            
        if(kind !=''):
            self.kind = kind

    def isCollision(self, b1, b2):
        return sqrt((b1.x - b2.x) * (b1.x - b2.x) + (b1.y - b2.y) * (b1.y - b2.y)) < b1.diam / 2 + b2.diam / 2

    def splitBall(self, b1):
        diam = b1.diam
        kind = b1.kind
        for n in range(1, 100):
            nro = n
            if diam / nro < 20:
                break
        x = self.x
        y = self.y
        diam = diam / nro

        for j in range(0, nro):
            self.parent.appendBall(kind, x, y, diam, 100)

        self.parent.killBall(b1)
        background("#ff0000")

    def run(self):
        u = self.parent  # u = universe

        if(self.safe > 0):
            self.safe -= 1

        for i in range(0, len(u.Balls)):

            if(self.isCollision(self, u.Balls[i]) and self != u.Balls[i]):
                
                if(self.safe == 0 and u.Balls[i].safe == 0):
                    
                    if(self.kind != 'splitter' and u.Balls[i].kind != 'splitter' ):
                
                        if(u.Balls[i].diam < self.diam):
        
                            self.growTo += u.Balls[i].diam
                            u.killBall(u.Balls[i])
                        else:
                            u.Balls[i].growTo += self.diam
                            u.killBall(self)
        
                        break
        
                    elif(self.kind != 'splitter' or u.Balls[i].kind != 'splitter'):
        
                        self.splitBall(u.Balls[i] if(self.kind == 'splitter') else self)
        
                        break
    
        if self.kind == 'normal':
            ball_color = u.NORMAL_COLOR
            
        if self.safe > 0:
            ball_color = u.SAFE_COLOR
            
        if self.kind == 'splitter':
            ball_color = u.SPLITTER_COLOR
    
        fill(ball_color)

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
    bU.refreshUniverse()


