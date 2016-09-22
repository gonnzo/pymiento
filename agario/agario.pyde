'''
#
# The Pymiento Project
#
# Project: Agar.io simulation
# Description: Bigger balls eat the smaller ones. The red balls, the splitters, blow white balls up keeping similar mass.
# Autor: Iván Gonzalo Moyano Pérez
# Version: Normalizing classes + gameTimeAlive
#
# gameTimeAlive: play the game pressing keys A, S or D
#
'''




###############################################################################################  Class Universe

class Universe:

    def __init__(self):

        self.amount = 30
        self.splitter_amount = 5
        
        
        self.timeAlive = []
        self.gameAlive = []
        
        self.NORMAL_COLOR = "#ffffff"
        self.SPLITTER_COLOR = "#ff0000"
        self.SAFE_COLOR = "#333333"
     
        
        self.game_TimeAlive =  {'gameYellow': {'color':'#ffcc00', 'key':'a', 'time': 0, 'record' : 0, 'alive': False, 'offset_x': width/3}, \
                                'gameBlue': {'color':'#0066ff', 'key':'s', 'time': 0, 'record' : 0, 'alive': False, 'offset_x': width/2}, \
                                'gameGreen': {'color':'#66ff00', 'key':'d', 'time': 0, 'record' : 0, 'alive': False, 'offset_x': width - width/3} }

        
        self.Balls = []
        self.BallsForDelete = []
        self.BallsForUpdate = []
        self.BallsForSplit = []
        
        
        self.totIni = 0
        self.totActual = 0

        for i in range(0, self.amount):
            self.appendBall('normal',self.NORMAL_COLOR)

        for i in range(0, self.splitter_amount):
            self.appendBall('splitter',self.SPLITTER_COLOR, '', '', 20, 0)




############################################################################################### appendBall()

    def appendBall(self, kind='', color='', x='', y='', diam='', safe=''):
        
        self.Balls.append(Ball(self, kind, color, x, y, diam, safe))




############################################################################################### killBall()

    def killBall(self, ball):
        
        self.BallsForDelete.append(ball)
        
        
        
############################################################################################### refreshUniverse()

    def refreshUniverse(self):
        

        for ball in self.Balls:
            ball.run()
    
        
        for ball in self.BallsForUpdate: 
            if ball[0] in self.Balls: 
                self.Balls[self.Balls.index(ball[0])].growTo +=  ball[1] 
             
        self.BallsForUpdate = []
        
        
        
        for ball in self.BallsForSplit:
            if ball in self.Balls: 
                ball.splitBall(ball) 
             
        self.BallsForSplit = []
        
        
        for ball in self.BallsForDelete:
            if ball in self.Balls: 
                self.Balls.remove(ball)
             
        self.BallsForDelete = []
        
        
        self.totActual = 0
        for ball in self.Balls:
            self.totActual += ball.diam
            
         
        if(self.totIni==0): 
            self.totIni= self.totActual
            
            
            
        self.gameTimeAlive()
                



############################################################################################### gameTimeAlive()        
        
    def gameTimeAlive(self):
        
        for k, gB in self.game_TimeAlive.items():
            gB['alive'] = False
            
        for ball in self.Balls:
            if 'game' in ball.kind:
                self.game_TimeAlive[ball.kind]['alive'] = True 
        
        for k, gB in self.game_TimeAlive.items():
            if not gB['alive']: 
                if(gB['time'] > gB['record']): 
                    gB['record'] = gB['time']
                gB['time'] = 0
                
            if gB['time'] > 0 :
                fill(gB['color'])
                text(gB['time'], gB['offset_x'], height/2)
                gB['time'] += 1
                
        
            if gB['record'] > 0 :
                fill(gB['color'])
                text(gB['record'], gB['offset_x'], 100)
        
        for k, gBall in self.game_TimeAlive.items():
            if keyPressed == True and key==gBall['key'] and not gBall['alive']:
                self.game_TimeAlive[k]['time'] = 1
                self.appendBall(k , self.game_TimeAlive[k]['color'], width/2, height/2,'',100)






###############################################################################################  Class Ball
        
class Ball(object):

    def __init__(self, parent, kind='', color='#ffffff', x='', y='', diam='', safe=''):
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
        self.safe = 50
        self.growTo = 0
        self.kind = kind
        self.color = color

        if(x != ''): self.x = x
        if(y != ''): self.y = y
        if(diam != ''): self.diam = diam
        if(safe != ''): self.safe = safe
   
            
            
            
############################################################################################### isCollision()

    @staticmethod
    def isCollision(b1, b2):
        return sqrt((b1.x - b2.x) * (b1.x - b2.x) + (b1.y - b2.y) * (b1.y - b2.y)) < b1.diam / 2 + b2.diam / 2



############################################################################################### splitBall()
    
    def splitBall(self, b1):
        u = self.parent
        diam = b1.diam
        kind = b1.kind
        color = b1.color
        
    
        minsize = 30 if diam > 30 else diam
        nro = int(diam/minsize)
        
        
        x = self.x
        y = self.y
        oldd = diam
        
        diam = diam / nro
        
        # compensación de masa perdida para divisiones mayores a 2 bolas
        if nro > 2 and u.totActual * 100 / u.totIni < 95: 
            dif = u.totIni - u.totActual
            if dif > minsize:
                nro += int(dif/minsize)
        # fin compensación
                 
                    
                
        
        
        for j in range(0, nro):
            self.parent.appendBall(kind, color, x, y, diam + random(-10,10), 100)

        self.parent.killBall(b1)
        
        background("#ff0000")
        
        
        
############################################################################################### eatBall() 
   
    def eatBall(self, balls):
        b1 = balls[0]
        b2 = balls[1]
        
        u = self.parent
        new_ball_diam = [b1, b2.diam]
        if new_ball_diam not in u.BallsForUpdate: 
            u.BallsForUpdate.append(new_ball_diam)
            u.killBall(b2)
        
        
        
############################################################################################### run()


    def run(self):
        u = self.parent  # 'u' of universe

                
        if(self.safe > 0):
            self.safe -= 1
        
    
        for ball in u.Balls:
            
            if(self.isCollision(self, ball) and self != ball):
                
                if(self.safe <= 0 and ball.safe <= 0):
                    
                    if(self.kind != 'splitter' and ball.kind != 'splitter' ):
                        
                        self.eatBall([self, ball] if(ball.diam < self.diam) else [ball, self])
                        
                 
                    elif(self.kind != 'splitter' or ball.kind != 'splitter'):
        
                        new_ball_for_split = ball if self.kind == 'splitter' else self
                        
                        if new_ball_for_split not in u.BallsForSplit: 
                            
                            u.BallsForSplit.append(new_ball_for_split)
                     
                        
        
                       
        bColor = self.color
        
        if self.safe > 0:
            bColor = u.SAFE_COLOR
        
        if 'game' in self.kind:
            stroke(bColor)
            strokeWeight(2)
            noFill()
            ellipse(self.x, self.y, self.diam+20, self.diam+20)
            noStroke()
        
        fill(bColor)
        
        
        
        
        ellipse(self.x, self.y, self.diam, self.diam)
        
        
        if(self.growTo > 0):
            self.diam += 3
            self.growTo -= 3
        elif(self.growTo < 0):
            self.diam += self.growTo
            self.growTo = 0
         

        if(self.x > width - self.diam / 2):
            self.dir_x = -1
        if(self.y > height - self.diam / 2):
            self.dir_y = -1

        if(self.x < self.diam / 2):
            self.dir_x = 1
        if(self.y < self.diam / 2):
            self.dir_y = 1

        self.x = self.x + ((self.step + self.safe / 10) * self.deg_x) * self.dir_x
        self.y = self.y + ((self.step + self.safe / 10) * self.deg_y) * self.dir_y
 
 
 
 

############################################################################################### PROCESSING SETUP

def setup():

    global univ
    
    myfont = createFont("oswald",82, True)
    textFont(myfont)
    
    
    fullScreen(P2D, 2)
    #size(1900,700,P2D)
    noStroke()
    univ = Universe()



############################################################################################### PROCESSING DRAW

def draw():

    background(0)
    univ.refreshUniverse()
    
    
    