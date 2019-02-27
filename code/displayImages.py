#!/usr/bin/python
"""
This script will handle messages to display by iterating through pictures

This script receives a mesage as a string and basesd on the content of the argument
it displays a squence of picture containing messages
"""

import pygame
import time
import sys



msg = []
#load initial pictures: range => 0, 6
msg.append(pygame.image.load("messages/initial1.png"))
msg.append(pygame.image.load("messages/initial2.png"))
msg.append(pygame.image.load("messages/initial3.png"))
msg.append(pygame.image.load("messages/initial4.png"))
msg.append(pygame.image.load("messages/initial5.png"))
msg.append(pygame.image.load("messages/initial6.png"))
msg.append(pygame.image.load("messages/initial7.png"))
#load instruction pictures: range => 7, 12
msg.append(pygame.image.load("messages/instruction1.png"))
msg.append(pygame.image.load("messages/instruction2.png"))
msg.append(pygame.image.load("messages/instruction3.png"))
msg.append(pygame.image.load("messages/instruction4.png"))
msg.append(pygame.image.load("messages/instruction5.png"))
msg.append(pygame.image.load("messages/instruction6.png"))
#load score picture: range => 13, 13
msg.append(pygame.image.load("messages/score.png"))
#load paddle picture: range => 14, 14
msg.append(pygame.image.load("messages/paddle.png"))
#load ball picture: range => 15, 15
msg.append(pygame.image.load("messages/ball.png"))

width = 90
height = 80
screen = pygame.display.set_mode((width, height))
score = 0



#arguments:
# arg ::: reference to the pictures that need to be iteratred through
# x ::: x coordinates of where to draw picture
# y ::: y coordinates of where to draw picture
def main(arg, x, y):

    ind = 0
    last = 0
    running = True
    oldTime = time.time() 
    newTime = 0 
    
    #initialise indexes
    if arg == "init":
        ind = 0
        last = 6
    elif arg == "ins":
        ind = 7
        last = 12
    elif arg == "score":
        ind = 13
        last = 13

    index = ind

    #go trough pictures
    displayPic(index, x, y)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False

        newTime = time.time()
        if int(newTime-oldTime) > 0.7:
            oldTime = newTime
            if index >= last:
                #all pictures were shown
                index = ind
            else:
                index+=1
            #show next picture
            displayPic(index, x, y)
    



def displayPic(index, x, y):
    name = str(index)
    print("displaying"+name)
    screen.blit(msg[index], (x, y))
    pygame.display.flip()


    

def animateGame():
    
    paddle = drawObject("paddle", 20, height-10, True, False, 14)
    ball = drawObject("ball", 0, 0, True, True, 15)
    running = True
    past = time.time()
    present = 0
    global score
    
    while running:
        present = time.time()
        screen.fill((0, 0, 0))
        
        #handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pressedkeys = pygame.key.get_pressed()
                if pressedkeys[pygame.K_a]:
                    paddle.animateObject(9, 0, direction="left");
                elif pressedkeys[pygame.K_d]:
                    paddle.animateObject(9, 0);
        
        #handle animation
        if (present - past) > 0.1:
            past = present
            ball.animateObject(4, 4)
            paddle.animateObject(0, 0);

            if (ball.x < paddle.x or ball.x > paddle.x) and ball.y > paddle.y+12:
                running = False

            elif (ball.x >= paddle.x and ball.x <= paddle.x+21):
                if (ball.y+14 >= height-10):
                    ball.down = False
                    score = score+1
                    print score

            print ("paddle x&y: "+str(paddle.x)+"-"+str(paddle.y)+"===="+"ball x&y"+str(ball.x)+"-"+str(ball.y))



class drawObject:
    def __init__(self, objToDraw, x, y, right, bottom, imgIndex):
        self.obj = objToDraw
        self.x = x
        self.y = y
        self.right = right
        self.down = bottom
        self.imgIndex = imgIndex

    def animateObject(self, x, y, direction = "right"):
        if self.obj == "paddle":
            if direction == "right":
                if self.x <= (width-25):
                    self.x += x
            elif direction == "left":
                if self.x >= 0:
                    self.x -= x

        elif self.obj == "ball":
            if self.right:
                if self.x <= (width-25):
                    self.x += x
                else:
                    self.right = False
            else:
                if self.x >= 0:
                    self.x -= x
                else:
                    self.right = True
            if self.down:
                    self.y += y
            else:
                if self.y >= 0:
                    self.y -= y
                else:
                    self.down = True
        displayPic(self.imgIndex, self.x, self.y)




if __name__ == "__main__":
    
    pygame.init()
    
    try:
        argument = sys.argv[2]
        if argument == "init" or "ins" or "score":
            main(argument, 0, 0)
            main("ins", 0, 0)
            animateGame()

            running = True
            present = 0
            past = time.time()
            future = 8
            remote = time.time()
            points = False
            
            font = pygame.font.SysFont("comicsansms", 72)
            text = font.render(str(score), True, (255, 0, 0))
            print "score: "
            print score
            while running:
                
                present = time.time()
                if present - remote > future:
                    running = False
                if present - past > 0.7:
                    past = present
                    #screen.fill((0, 0, 0))

                    if points:
                        screen.fill((0, 0, 0))
                        screen.blit(text,(35,40))
                        pygame.display.flip()
                    else:
                        screen.fill((0, 0, 0))
                        displayPic(13, 0, 0)

                    points = not points

                    print points
        else:
            print("Error reading arguments1.")
    except Exception as err:
        print("Error reading arguments2: ")
        print(err)

#for event in pygame.event.get():
#    if event.type == pygame.QUIT:
#        running = False
#    else:
