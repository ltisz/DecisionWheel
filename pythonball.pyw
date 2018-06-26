import pygame
import time
import sys
import random

#Class to create background that stays behind all other graphics
class Background(pygame.sprite.Sprite):                 #Create background as a sprite
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)      #Grab image
        self.rect = self.image.get_rect()               #Grab dimensions
        self.rect.left, self.rect.top = location        #Grab location

#Quit function when click windows X
def quit():
    for event in pygame.event.get():                    #Check for events   
        if event.type == pygame.QUIT:                   #If event is  quit...  
            pygame.quit(); sys.exit();                  #...then quit!

#Function to display large result text
def displayresult(result):
    textsurface = font.render(result, True, (0, 0, 0))
    textrect = textsurface.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(textsurface,textrect)
    pygame.display.update()

##INPUT DECISION LIST HERE
##
decisionlist = ['Claymont','Mac Mart','Chicken','El Diablo','Caltor','Honeygrow','Roots']
##
##INPUT DECISION LIST ABOVE

pygame.init() #Initializing pygame
pygame.font.init()
font = pygame.font.SysFont(None, 48)                #Large font for end result
font2 = pygame.font.SysFont(None, 20)               #Small font for on wheel
screen = pygame.display.set_mode((400,400))         #Creating 400x400 window
degree = 0                                          #Spinner starts at 0 degrees
BackGround = Background('wheel.png', [0,0])
elapsedtime = 1                                     #Start time (ms)
end = random.randint(200,560)                       #End time (ms)
#clock = pygame.time.Clock()    

x = 1                                               #x is the variable that controls the main loop
resultlist = []                                     #List of results, needed in case decision list is < 8

for i in range(8):                                  #Iterate through decision list
    try:
        resultlist.append(random.choice(decisionlist))  #Append decision to result list randomly
        decisionlist.remove(resultlist[i])              #Remove used result
    except:
        resultlist.append('Free Space')                 #Assign "free space" if list is used up

#MAIN LOOP
while x == 1:  
    pygame.display.flip()
    screen.fill([255, 255, 255])                    #Fill with white
    screen.blit(BackGround.image, BackGround.rect)  #Use background class to create background
    
    surf = pygame.Surface((100,100))                #Creating surface for the spinner
    surf.fill((255, 255, 255))                      #White fill for the surface

    surf.set_colorkey((255,255,255))                #Colorkey out the white fill

    surf = pygame.image.load('cool.png').convert_alpha()    #Use convert_alpha to preserve transparency
    where = 180, 10                                 #Put it in the middle

    blittedRect = screen.blit(surf, where)          #Put the spinner on the screen
    screen.fill([255, 255, 255])                    #Re-draw screen
    screen.blit(BackGround.image, BackGround.rect)  #Re-draw background
    oldCenter = blittedRect.center                  #Find old center of spinner

    rotatedSurf = pygame.transform.rotate(surf, degree)     #Rotate spinner by degree (0 at first)
    
    rotRect = rotatedSurf.get_rect()                #Get dimensions of rotated spinner
    rotRect.center = oldCenter                      #Assign center of rotated spinner to center of pre-rotated

    screen.blit(rotatedSurf, rotRect)               #Put the rotated spinner on screen

    degree += 6                                     #Increase angle by six degrees
    if degree == 360:                               #Reset angle if greater than 360
        degree = 0
    
    ## Placements for choices on the background spinner
    textgreen = font2.render(resultlist[0],False,(0,0,0))
    screen.blit(textgreen,(110,65))
    textred = font2.render(resultlist[1],False,(0,0,0))
    screen.blit(textred,(40,150))
    textlimegreen = font2.render(resultlist[2],False,(0,0,0))
    screen.blit(textlimegreen,(40,220))
    textorange = font2.render(resultlist[3],False,(0,0,0))
    screen.blit(textorange,(120,340))
    textcyan = font2.render(resultlist[4],False,(0,0,0))
    screen.blit(textcyan,(210,340))
    textpink = font2.render(resultlist[5],False,(0,0,0))
    screen.blit(textpink,(300,220))
    textblue = font2.render(resultlist[6],False,(0,0,0))
    screen.blit(textblue,(300,150))
    textyellow = font2.render(resultlist[7],False,(0,0,0))
    screen.blit(textyellow,(210,65))

    pygame.display.flip()                           #Redraw screen
    
    quit()                                          #Allow for quitting
    
    #Change speed of spinner as time goes on
    if elapsedtime < end/6:
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
        pygame.time.wait(150)
        elapsedtime += 1
    elif elapsedtime < end:
        pygame.time.wait(300)
        elapsedtime += 1    
    elif elapsedtime == end:                        #If it hits the end...
        x = 2                                       #x = 2 kidnaps the main loop to a secondary main loop (stopped spinner)
        while x == 2:
            screen.blit(rotatedSurf, rotRect)       #Draw the stopped spinner
            degree = degree - 6                     #Degree result needs to be 6 degrees ago
            #Checking for the angle and printing the results
            if degree > 0 and degree < 45:
                x = 3                               #"Kidnap" main loop again
                result = resultlist[0]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:    #Click to spin again!
                            x = 1                                   #Go back to main loop
                            elapsedtime = 1                         #Reset elapsed time
                            end = random.randint(200,560)           #Randomly generate a new end
                            break
                    quit()                                          #Allow for quitting
            elif degree > 45 and degree < 90:
                x = 3
                result = resultlist[1]
                displayresult(result)             
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree > 90 and degree < 135:
                x = 3
                result = resultlist[2]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree > 135 and degree < 180:
                x = 3
                result = resultlist[3]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree > 180 and degree < 225:
                x = 3
                result = resultlist[4]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree > 225 and degree < 270:
                x = 3
                result = resultlist[5]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree > 270 and degree < 315:
                x = 3
                result = resultlist[6]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree > 315 and degree < 360:
                x = 3
                result = resultlist[7]
                displayresult(result)
                while x == 3:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x = 1
                            elapsedtime = 1
                            end = random.randint(200,560)
                            break
                    quit()
            elif degree%45 == 0:
                x = 3
                print 'on the line'
                result = 'Spinning Again...'
                displayresult(result)
                pygame.time.wait(300)
                x = 1
                elapsedtime = 1
                end = random.randint(200,560)
                while x == 3:
                    quit()   
            quit()
