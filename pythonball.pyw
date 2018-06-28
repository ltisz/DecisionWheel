import pygame
from pygame import gfxdraw
import time
import sys
import random
import math

#Quit function when click windows X
def quit():
    for event in pygame.event.get():                    #Check for events   
        if event.type == pygame.QUIT:                   #If event is  quit...  
            pygame.quit(); sys.exit();                  #...then quit!

#Function to display large result text
def displayresult(result):
    #cheer.play() 
    fanfare.play()
    textsurface = font.render(result, True, (0, 255, 0))
    textrect = textsurface.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(textsurface,textrect)
    pygame.display.update()

##INPUT DECISION LIST HERE
##
decisionlist = ['Claymont','Mac Mart','Jimmy Johns','Chicken','El Diablo','Caltor','Honeygrow','Roots']
##
##INPUT DECISION LIST ABOVE

pygame.init() #Initializing pygame
font = pygame.font.SysFont(None, 48)                #Large font for end result
font2 = pygame.font.SysFont(None, 28)               #Small font for on wheel
screen = pygame.display.set_mode((400,400))         #Creating 400x400 window
degree = 0                                          #Spinner starts at 0 degrees
elapsedtime = 1                                     #Start time (ms)
end = random.randint(200,560)                       #End time (ms)
spin1 = pygame.mixer.Sound("spin1.wav")
spin2 = pygame.mixer.Sound("spin2.wav")
spin3 = pygame.mixer.Sound("spin3.wav")
fanfare = pygame.mixer.Sound("fanfare.wav")
cheer = pygame.mixer.Sound("cheer.wav")
x = 1                                               #x is the variable that controls the main loop
resultlist = []                                     #List of results, needed in case decision list is < 8
cx = cy = r = 200
dividers = len(decisionlist)
radconvert = math.pi/180

for i in range(len(decisionlist)):                  #Iterate through decision list
    resultlist.append(random.choice(decisionlist))  #Append decision to result list randomly
    decisionlist.remove(resultlist[i])              #Remove used result

#resultlist=list(reversed(resultlist))
print resultlist
#MAIN LOOP
while x == 1:  
    pygame.display.flip()
    screen.fill([255, 255, 255])                    #Fill with white
    
    surf = pygame.Surface((100,100))                #Creating surface for the spinner
    surf.fill((255, 255, 255))                      #White fill for the surface

    surf.set_colorkey((255,255,255))                #Colorkey out the white fill

    surf = pygame.image.load('cool.png').convert_alpha()    #Use convert_alpha to preserve transparency
    where = 180, 10                                 #Put it in the middle

    blittedRect = screen.blit(surf, where)          #Put the spinner on the screen
    screen.fill([255, 255, 255])                    #Re-draw screen
    pygame.draw.circle(screen, (0,0,0), (cx, cy), r, 3)
    for i in range(dividers):
        gfxdraw.pie(screen, cx, cy, r, i*(360/dividers), (360/dividers), (0,0,0))
    i = 1
    iters = range(1,dividers*2,2)
    for i in iters:
        textChoice = font2.render(resultlist[iters.index(i)],False,(0,0,0))
        textwidth = textChoice.get_rect().width
        textheight = textChoice.get_rect().height
        textChoice = pygame.transform.rotate(textChoice,(i-(2*i))*(360/(dividers*2)))
        textwidth = textChoice.get_rect().width
        textheight = textChoice.get_rect().height
        screen.blit(textChoice,(
                                (cx-(textwidth/2))
                                +((r-100)*math.cos(((i*(360/(dividers*2))))*radconvert)),
                                (cy-(textheight/2))
                                +((r-100)*math.sin(((i*(360/(dividers*2))))*radconvert))
                                )
                            )
        textChoice = ''
    oldCenter = blittedRect.center                  #Find old center of spinner

    rotatedSurf = pygame.transform.rotate(surf, degree)     #Rotate spinner by degree (0 at first)
    
    rotRect = rotatedSurf.get_rect()                #Get dimensions of rotated spinner
    rotRect.center = oldCenter                      #Assign center of rotated spinner to center of pre-rotated

    screen.blit(rotatedSurf, rotRect)               #Put the rotated spinner on screen

    degree += 6                                     #Increase angle by six degrees
    if degree == 360:                               #Reset angle if greater than 360
        degree = 0
    
    pygame.display.flip()                           #Redraw screen
    
    quit()                                          #Allow for quitting
   
    #Change speed of spinner as time goes on
    if elapsedtime == 1:
        spin1.play(-1)
        elapsedtime += 1
    elif elapsedtime < end/6:
        pygame.time.wait(2)
        elapsedtime += 1
    elif elapsedtime < end/4:
        pygame.time.wait(5)
        elapsedtime += 1
    elif elapsedtime < end/2:
        pygame.time.wait(10)
        elapsedtime += 1
    elif elapsedtime < end/1.5:
        pygame.time.wait(15)
        elapsedtime += 1
    elif elapsedtime < end/1.2:
        pygame.time.wait(30)
        elapsedtime += 1
    elif elapsedtime < end/1.1:
        pygame.time.wait(70)
        elapsedtime += 1
    elif elapsedtime < end/1.05:
        spin1.fadeout(1000)
        spin3.stop()
        spin3.play()
        pygame.time.wait(150)
        elapsedtime += 1
    elif elapsedtime < end:
        spin1.stop()
        spin3.stop()
        spin3.play()
        pygame.time.wait(200)
        elapsedtime += 1    
    elif elapsedtime == end:                        #If it hits the end...
        spin1.stop()
        print 'raw degree: ' + str(degree)
        degCheck = degree-6
        x = 2                                       #x = 2 kidnaps the main loop to a secondary main loop (stopped spinner)
        
        if len(resultlist) < 3:
            resultlistnew = resultlist
        if len(resultlist) < 4:
            resultlistnew = list(reversed(resultlist))
        elif len(resultlist) < 6:
            resultlistnew = list(reversed(resultlist))
            resultlistnew.append(resultlistnew.pop(0))
        elif len(resultlist) < 10:
            resultlistnew=list(reversed(resultlist))
            resultlistnew.append(resultlistnew.pop(0))
            resultlistnew.append(resultlistnew.pop(0))
        while x == 2:   
            screen.blit(rotatedSurf, rotRect)       #Draw the stopped spinner                
            for i in range(len(resultlist)):
                if degCheck > i*(360/len(resultlistnew)) and degCheck < (i+1)*(360/len(resultlistnew)):
                    x = 3
                    print i
                    result = resultlistnew[i]
                    displayresult(result)
                    while x == 3:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x = 1
                                elapsedtime = 1
                                end = random.randint(200,560)
                                break
                        quit()
            quit()

