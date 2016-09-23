'''
#
# The Pymiento Project
#
# Project: soundWaves
# Description: 
# - Generate the sound waves from an audio file. 
# - The intention of this code is create a template with the shape of the sound wave, to trace onto a plank of wood and then saw it with a jigsaw. 
# - It uses the averrages of data to get a softer drawing output // step var
# - Connect all the points with bezier lines to make it even softer
# Instructions for use: 
# - zoomToFit default "1". You can move this value some points up or down, e.g. "0.8" or "1.3" to make the wave smaller or bigger, respectively. 
# - In order to make a stronger piece of wood, if the shape shows narrow paths in the middle (a kind of isthmi), you can optimize the shape by pressing the key "o" making it wider.  But it only works if you set up the sound as isAloud = False
# - Finally, pressing the key "s", you can capture and save the image into the "generatedImages" folder. 
# - Move the index "sound_index" to render each wave, one by one.
# Autor: Iván Gonzalo Moyano Pérez
# Version: 1.0
# Known bugs: the wave endings don't close.
# TODO: 
# - fit the frameRate with the audio buffer in order to get an acurrate wave ending.
# - get the sound lenght to auto-fit the wave into the screen (replacing the manual value of zoomToFit)
#
'''

def setup():
    
    global minim, sample, x, prom, prevPoint, dots, drawn, fileName, isAloud, zoomToFit, saved

    fullScreen(P2D,2)

    add_library('minim') # audio library
    minim = Minim(this)
    
    drawn = False
    saved = False
    x = 20
    prom = 0
    prevPoint = [0,0]
    
    
    
    sounds = []
    
    sounds.append(['i-have-a-dream',False,1])
    sounds.append(['king-africa-bomba',True,1])
    sounds.append(['pinochet-dictablanda',False,1.4])
    sounds.append(['gran-dictador',False,1.2])
    sounds.append(['stalin',False,1])
    sounds.append(['imagine',True,0.85])
    sounds.append(['hitler',True,0.8])

    sound_index = 2 # Choose the index of the sound to render

    fileName = sounds[sound_index][0]
    isAloud =  sounds[sound_index][1]
    zoomToFit = sounds[sound_index][2]
     
    
    sample = minim.loadSample("../sounds/" + fileName + ".wav", 1024)
    
    dots = [[0,0]]
    
    background(255)
    noFill()
    smooth(10)
    stroke(0)
    frameRate(30)
    
    delay(1000) 

    sample.trigger()
    #sample.mute() ####################################### MUTE the sound
    
    
def draw():
    global x, prom, prevPoint, dots, drawn, isAloud

    
    zoomX = zoomToFit
    zoomY = 1
    zoom = 3
    steps = 10
    
    
    for i in xrange(sample.bufferSize()-1): 
        prom += sample.left.level()
    
    if(prom!=0 and x % steps == 0):
        prom = prom /  steps
        
        xEl = x * zoomX * zoom
        yEl = height / 2
        hEl = prom * zoomY * zoom
    
        currPoint = [xEl, abs(hEl)/2]
        
        if prevPoint[0]!=0:
            half = (xEl - prevPoint[0]) / 2
            
            pX = prevPoint[0]
            pY = prevPoint[1]
            
            cX = currPoint[0]
            cY = currPoint[1]
            
            
            lpY = normalize(pY)
            lcY = normalize(cY)
            
            if isAloud:
                dots.append([cX, cY])
            else:
                dots.append([cX, lcY])
            
            if isAloud:
                bezier(pX, yEl - pY,   pX + half, yEl - pY,          cX - half, yEl - cY, xEl, yEl - cY)
                bezier(pX, yEl + pY,   pX + half, yEl + pY,          cX - half, yEl + cY, xEl, yEl + cY)
            else:
                bezier(pX+2, yEl - lpY,   pX + half+2, yEl - lpY,          cX - half+2, yEl - lcY, xEl+2, yEl - lcY)
                bezier(pX+2, yEl + lpY,   pX + half+2, yEl + lpY,          cX - half+2, yEl + lcY, xEl+2, yEl + lcY)
 
        prevPoint = [xEl, abs(hEl)/2]
        
        prom = 0

    x += 1

    
def keyPressed():
    global saved
    
    if((key == 's' or key == 'S') and not saved):
        print("Image created!")
        saveFrame("../generatedImages/" + fileName + "-#####.png")
        saved = True
        
    if(key=='o' or key=='O'):
        drawOptimization()
        
        
def drawOptimization():
    global dots, drawn, fileName, isAloud, saved
    
    if not drawn and not isAloud:
        
        background(255)
    
        max = 0
        for i in range(0,len(dots)):
            if dots[i][1] > max:
                max = dots[i][1]
                
        for i in range(0,len(dots)):
            dots[i][1] = dots[i][1] * (height / 2 - 20) / max
            dots[i][1] = dots[i][1] + cosenize(dots[i][1], max)
    
        max = 0
        for i in range(0,len(dots)):
            if dots[i][1] > max:
                max = dots[i][1]
        
        for i in range(1,len(dots)):
            
            pX = dots[(i-1)][0]
            pY = dots[(i-1)][1] * (height / 2 - 20) / max 
            
            cX = dots[i][0]
            cY = dots[i][1] * (height / 2 - 20) / max
            
            
            half = (cX-pX) / 2
        
            yEl = height / 2
        
            stroke(0,0,0)
            bezier(pX, yEl - pY,   pX + half, yEl - pY,          cX - half, yEl - cY, cX, yEl - cY)
            bezier(pX, yEl + pY,   pX + half, yEl + pY,          cX - half, yEl + cY, cX, yEl + cY)
    
    drawn = True
        
                
def cosenize(v, m):
    v = (v * PI * 2 / m) - PI 
    v = (cos(v)+1)*40 
    return v   
    
    
def normalize(value):     
    value = height/2 + log(value - height/2) - log(value)*10 if value > height/2 else value
    value = value + log(value+1)*10 if value < height/4 else value
    return value


def stop():
    sample.close()
    minim.stop()