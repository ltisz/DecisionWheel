##-*- coding: utf-8 -*-

import pygame
from pygame import gfxdraw
import time
import sys
import random
import math
import json
import urllib2
from geopy.geocoders import Nominatim
from Tkinter import *

#Various constants/sizes/etc
screensquare = 800                                  #800x800 square
cx = cy = r = screensquare/2                        #Center, radius
radconvert = math.pi/180                            #Radian conversion
degree = 0                                          #Spinner starts at 0 degrees
elapsedtime = 1                                     #Start time (ms)
end = random.randint(200,560)                       #End time (ms)

def start_wheel():
    T.delete('1.0',END)
    global x
    global screen
    try:
        ##GEOLOCATION
        geolocator = Nominatim()
        location = geolocator.geocode(address.get())    #Address is from tkinter input
        lat = str(location.latitude)                    #Get lat and long of location
        long = str(location.longitude)

        foodurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyC-rkQPd73r5y0GAVCnIUxpVsHJ38mmDNs&location=" + lat + "," + long + "&rankby=distance&keyword=restaurant&opennow"   #Google maps API url
        json_string = json.load(urllib2.urlopen(foodurl))

        for k in range(int(choices.get())):
            try:
                decisionlist.append(str(json_string["results"][k]["name"].encode('utf-8')))
            except:
                break
        T.insert(END,'Found Location! Lat: ' + lat + ' Long: ' + long + '\r\n')
        x = 1                                           #Initiate pygame main loop
        screen = pygame.display.set_mode((screensquare,screensquare))         #Creating window
        master.destroy()                                #Close tkinter window
    except:
        T.insert(END,'Location not found.\r\n')
    
#Quit function when click windows X
def quit():
    for event in pygame.event.get():                    #Check for events   
        if event.type == pygame.QUIT:                   #If event is  quit...  
            pygame.quit(); sys.exit();                  #...then quit!

#Function to display large result text
def displayresult(result):
    fanfare.play()
    textsurface = font.render(result, True, (0, 255, 0))
    textrect = textsurface.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(textsurface,textrect)
    pygame.display.update()

resultlist = []                                     #List of results
decisionlist = []

##TKINTER STUFF
master = Tk()
master.geometry("500x150")

Label(master, text="Address").grid(row=0)
Label(master, text="# of Results").grid(row=1)

address = Entry(master, width=50)
choices = Spinbox(master, width=50)
address.grid(row=0, column=1,columnspan=3)
choices.grid(row=1, column=1,columnspan=3)

T = Text(master, height=2, width = 65)
T.grid(row=5,column=0,columnspan=5)

Button(master, text='Verify', command=start_wheel).grid(row=3, column=2, sticky=W, pady=4)

x = 0                                               #Freeze wheel while getting input

mainloop()                                          #Run input tkinter

pygame.init()                                       #Initializing pygame
font = pygame.font.SysFont(None, 78)                #Large font for end result
font2 = pygame.font.SysFont(None, 28)               #Small font for on wheel

#Sounds
spin1 = pygame.mixer.Sound("spin1.wav")
spin3 = pygame.mixer.Sound("spin3.wav")
fanfare = pygame.mixer.Sound("fanfare.wav")

for t in range(len(decisionlist)):                  #Iterate through decision list
    resultlist.append(str(random.choice(decisionlist)))  #Append decision to result list randomly
    decisionlist.remove(resultlist[t])              #Remove used result

print resultlist
dividers = len(resultlist)

#MAIN LOOP
while x == 1:  
    pygame.display.flip()
    screen.fill([255, 255, 255])                                        #Fill with white
    
    surf = pygame.Surface((screensquare/2,screensquare/2))              #Creating surface for the spinner
    surf.fill((255, 255, 255))                                          #White fill for the surface

    surf.set_colorkey((255,255,255))                                    #Colorkey out the white fill

    surf = pygame.image.load('cool.png').convert_alpha()                #Use convert_alpha to preserve transparency
    spinwidth = surf.get_rect().width
    spinheight = surf.get_rect().height
    where = (screensquare/2)-(spinwidth/2),(screensquare/2)-(spinheight/2)  #Put it in the middle

    blittedRect = screen.blit(surf, where)                              #Put the spinner on the screen
    screen.fill([255, 255, 255])                                        #Re-draw screen
    pygame.draw.circle(screen, (0,0,0), (cx, cy), r, 3)                 #Draw circle with center @ center, radius r
    for i in range(dividers):
        gfxdraw.pie(screen, cx, cy, r, i*(360/dividers), (360/dividers), (0,0,0))   #Draw "Pie Slices"
    i = 1
    iters = range(1,dividers*2,2)                                       #Generates list of odd numbers
    for i in iters:
        textChoice = font2.render(resultlist[iters.index(i)],False,(0,0,0)) #Render text for each choice
        textwidth = textChoice.get_rect().width                             #Get width & height of text rect
        textheight = textChoice.get_rect().height
        textChoice = pygame.transform.rotate(textChoice,(i-(2*i))*(360/(dividers*2)))   #Rotate it to the correct angle
        textwidth = textChoice.get_rect().width                                         #Get center of rotated text
        textheight = textChoice.get_rect().height
        screen.blit(textChoice,(                                                            #Place text on screen
                                (cx-(textwidth/2))                                          #In a circle 200 pixels smaller
                                +((r-200)*math.cos(((i*(360/(dividers*2))))*radconvert)),   #in diameter, with each text
                                (cy-(textheight/2))                                         #between the dividers
                                +((r-200)*math.sin(((i*(360/(dividers*2))))*radconvert))
                                )
                            )
        textChoice = ''
    oldCenter = blittedRect.center                                  #Find old center of spinner

    rotatedSurf = pygame.transform.rotate(surf, degree)             #Rotate spinner by degree (0 at first)
    
    rotRect = rotatedSurf.get_rect()                                #Get dimensions of rotated spinner
    rotRect.center = oldCenter                                      #Assign center of rotated spinner to center of pre-rotated

    screen.blit(rotatedSurf, rotRect)               #Put the rotated spinner on screen

    degree -= 2                                     #Increase angle by six degrees
    if degree == -360:                              #Reset angle if greater than 360
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
        spin1.stop()                                #Stop playing the spin sound
        degCheck = degree                           #We don't want to mess with degree
        degCheck = (-1*degCheck)-90                 #Text is offset from actual angle
        if degCheck < 0:                            #...so we need to correct it
            degCheck = degCheck + 360
        x = 2                                       #x = 2 kidnaps the main loop to a secondary main loop (stopped spinner)
        while x == 2:   
            screen.blit(rotatedSurf, rotRect)       #Draw the stopped spinner                
            for i in range(len(resultlist)):        #For loop to see where the spinner stopped
                if degCheck > i*(360/len(resultlist)) and degCheck < (i+1)*(360/len(resultlist)):
                    x = 3                           #Kidnap the loop again
                    result = resultlist[i]
                    displayresult(result)
                    while x == 3:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:    #Allow to spin again
                                x = 1
                                elapsedtime = 1
                                end = random.randint(200,560)
                                break
                        quit()
                elif degCheck%(360/len(resultlist)) == 0:               #Check if it's on the line
                    x = 3
                    displayresult('Spinning Again')
                    pygame.time.wait(1)
                    x = 1
                    elapsedtime = 1
                    end = random.randint(200,560)
                    while x == 3:
                        quit()   
            quit()
