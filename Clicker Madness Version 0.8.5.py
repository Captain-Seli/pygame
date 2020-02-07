#Clicker Madness (Final Project)
#Clicker Madness 0.8.5.py
#Jonathan Williams
#Jon
#jwilli66

#Version 0.8.5
#Version Patch Notes: Add rough elapsed time, difficulty selection.
#Clicker Game that displays targets the player must click for points.

from graphics import *
import math
import time
from random import randrange
import pygame
from playsound import playsound
pygame.init()

#Player Class. Saves Name and Final Score. (CLOD) My own class
class Player:
    def __init__(self,name,highscore):
        self.name=name
        self.highscore=int(highscore)
    #Method returns name
    def getName(self):
        return self.name
    #Method returns high score.
    def getHighScore(self):
        return self.highscore
    #method displays high scores.
    def display(self):
        print("{:<15}".format(self.name),"{:>}".format(self.highscore))

#Target Class (CLOD) My own class.
class Target:
    #Parameters for Target: Circle Center, amount of points its worth, color, x and y direction,
    def __init__(self, center,points,color,dirx=-1,diry=-1):
        self.circle=Circle(center,1)
        self.circle.setFill(color)
        self.dirx=dirx
        self.diry=diry
    #Class method gets center of circles.   
    def getCenter(self):
        return self.circle.getCenter()
    #Class method for drawing circles.
    def draw(self,win):
        self.circle.draw(win)
    #Class method for checking if the mouse is clicked inside a circle.
    def checkClick(self,win,mouse):
        if mouse == None:
            mouse=0
        else:
            dx=mouse.getX()-self.circle.getCenter().getX()#Get X Corrds
            dy=mouse.getY()-self.circle.getCenter().getY()#Get Y Coords
            dist=math.sqrt(dx*dx + dy*dy)##Distance Formula
            return dist <= self.circle.getRadius()##Check if distance is less than radius.

    #Move method. Moves circles randomly around the screen.
    def move(self):
        dx=self.circle.getCenter().getX()#return x coord of center
        dy=self.circle.getCenter().getY()#return y coord of center
        if dy>=10:
            self.diry=-1
        elif dx>=10:
            self.dirx=-1
        elif dx<=-10:
            self.dirx=1
        elif dy<=-10:
            self.diry=1
        elif dx>=10 and dy>=10:
            self.dirx=-1
            self.diry=-1
        elif dx<=-10 and dy<=-10:
            self.dirx=1
            self.dirx=1
        else:
            self.dirx=randrange(-8,8)#(RND)  Random Elements.
            self.diry=randrange(-8,8)#(RND)  Random Elements.
        self.circle.move(self.dirx,self.diry)

#Creates the game board. (GW) Graph Window
def window():
    win=GraphWin("Clicker Madness", 600,600)
    win.setBackground("black")
    win.setCoords(-10,-10,10,10)
    return win

#Function for difficulty selection.
def difSelec(win):
    easy=Rectangle(Point(-6,-6),Point(-4,-3))
    easy.setFill("green")
    easy.draw(win)
    med=Rectangle(Point(-2,-6),Point(0,-3))
    med.setFill("yellow")
    med.draw(win)
    hard=Rectangle(Point(2,-6),Point(4,-3))
    hard.setFill("red")
    hard.draw(win)
    diff=0
    while True:
        ##(IMS) Mouse click and location.
        click=win.getMouse()
        dx=click.getX()
        dy=click.getY()
        #Easy Mode
        if dx>=-6 and dx<=-4 and dy>=-6 and dy<=-3:
            print("easy")
            easy.undraw()
            med.undraw()
            hard.undraw()
            diff=0.8
            return diff
        #Medium Mode
        elif dx>=-2 and dx<=0 and dy>=-6 and dy<=-3:
            print("medium")
            easy.undraw()
            med.undraw()
            hard.undraw()
            diff=0.65
            return diff
        #Hard Mode
        elif dx>=2 and dx<=4 and dy>=-6 and dy<=-3:
            print("hard")
            easy.undraw()
            med.undraw()
            hard.undraw()
            diff=0.4
            return diff
             
#Function to create title screen and player inputs.
def title(win):
    #(IEB)Entry box.
    nameEntry=Entry(Point(0,0),8)
    nameEntry.setText("")
    nameEntry.getText()
    nameEntry.setSize(28)
    #(OTXT) Title text and instructions.
    text=Text(Point(0,3),"Clicker Madness!").draw(win)
    text.setSize(28)
    text.setFill("cyan")
    text2=Text(Point(0,1.8),"Enter Player Name, then Click a color:").draw(win)
    text2.setFill("cyan")
    text3=Text(Point(0,-1.3),"Press q at anytime to quit")
    text3.draw(win)
    text3.setFill("cyan")
    text4=Text(Point(0,-2),"Green=Easy, Yellow=Medium, Red=Hard")
    text4.setFill("cyan")
    text4.draw(win)
    #Gets name, difficulty selection, and clears window for game board.
    nameEntry.draw(win)
    diff=difSelec(win)
    name = nameEntry.getText()
    if name == " " or name == "":#Gives player "NoName" name if nothing is entered.
        name="NoName"
    name=name[0:9]#Disallows names that are to long.
    player=Player(name,0)#Player class creation (0 is default HS)
    if name != " ": 
        nameEntry.undraw()
        text.undraw()
        text2.undraw()
        text3.undraw()
        text4.undraw()
                 
    #Displays current player name and word "score".
    nameDisplay=Text(Point(-3,9.5),name)
    nameDisplay.setFill("cyan")
    nameDisplay.draw(win)
    scoreDisplay=Text(Point(0,9.5),"Score: ")
    scoreDisplay.setFill("cyan")
    scoreDisplay.draw(win)
    return player, diff#returns player class and difficulty selection.

#Function that returns player score.
def useHighScore(player):
    return player.getHighScore()

#(OFL) Saves Player data to outfile.
def save(player):
    outfile=open("Saves.txt","a")
    outfile.write(player.getName()+"\t"+str(player.getHighScore())+"\n")
    outfile.close()
    
#Function to draw targets.    
def drawCircle(win,circle_list):
    for c in circle_list:
        c.draw(win)
        
#Function to move the circles.
def moveCircle(win,circle_list):
    for c in circle_list:
        c.move()
               
#Main Game Play Function
def gamePlay(win,diff):
    #playsound('gnat.wav')
    #Create each target.
    green=Target(Point(1,1),2,"green")
    blue=Target(Point(2,1),5,"blue")
    yellow=Target(Point(3,1),3,"yellow")
    red=Target(Point(4,1),0,"red")
    purple=Target(Point(5,1),10,"purple")
    lime=Target(Point(6,1),0,"lime")
    indigo=Target(Point(6,1),-5,"indigo")
    circle_list=[green,blue,yellow,red,purple,lime,indigo]
    drawCircle(win,circle_list)
    #Initialize score to 0
    score=0
    #Set up to display live score after main game play loop.
    dispScore=Text(Point(1.5,9.5),score)
    dispScore.setFill("cyan")
    dispScore.draw(win)
    #Sets up elapsed time text for screen.
    time_text=Text(Point(9,9.5),"--")
    time_text.setFill("cyan")
    time_text.draw(win)
    #Start time to begin count for elapsed time.
    start_time=time.time()
    #Main game play loop.
    while True:
        if closeWin(win):
            break
        #Moves Targets.
        moveCircle(win,circle_list)
        time.sleep(diff)#Target move speed. Changes based on difficulty.
        #Main loop to detect clicks and award points.
        mouse=win.checkMouse()
        if green.checkClick(win,mouse):
            print("+2!")
            score=score+2
        elif red.checkClick(win,mouse):#terminates game. Loss condition.
            print("Game Over!")
            highscore=score
            score=0
            print(highscore)
            return highscore 
        elif blue.checkClick(win,mouse):
            print("+5!")
            score=score+5
        elif yellow.checkClick(win,mouse):
            print("+3!")
            score=score+3
        elif purple.checkClick(win,mouse):
            print("+10!")
            score=score+10
        elif lime.checkClick(win,mouse):#Zeros out current score.
            print("Zero'd Out!")
            score=0
        elif indigo.checkClick(win,mouse):#Subtracts 5 points from score.
            print("-5!")
            score=score-5
        #Current Time
        current_time=time.time()
        elapsed=(current_time-start_time+0.65)//1
        #Line displays live score.
        dispScore.setText(score)
        #Displays elapsed time.
        time_text.setText(elapsed)
        
    print(score)
    return score

#Function to close game at any time when the q key is pressed.
def closeWin(win):
    key=win.checkKey()
    if key == "q":
        win.close()
        return True
    return False

#Function that displays the top 5 players based on highscore.
def display():
    win=GraphWin("High Scores!", 600,600)#Draws HS Screen.
    win.setBackground("black")
    win.setCoords(-10,-10,10,10)
    hsText=Text(Point(0,9.2),"High Scores")
    hsText.setFill("cyan")
    hsText.setStyle("bold italic")
    hsText.setSize(28)
    hsText.draw(win)
    credit=Text(Point(0,-8.2),"Designed and Programmed by: Jon Williams.")
    credit.setFill("cyan")
    credit.setStyle("italic")
    credit.draw(win)
    credit2=Text(Point(0,-9.2),"Special Thanks to Jason, Amin, and Magari")
    credit2.setFill("cyan")
    credit2.setStyle("italic")
    credit2.draw(win)
    textName=Text(Point(-2.9,6),"Name")
    textName.setFill("cyan")
    textName.setStyle("bold")
    textName.draw(win)
    textScore=Text(Point(2.9,6),"High Score")
    textScore.setFill("cyan")
    textScore.setStyle("bold")
    textScore.draw(win)
    sortFile=open("Saves.txt","r").readlines()#(IFL) Reads data from the saved file.
    playerList=[]#(LOOD)List of my own class objects.
    for line in sortFile:   #Sorts high score list by score (lowest to highest)
        name=line.split("\t")[0]#Splits Player Name from string.
        highscore=line.split("\t")[1]#Splits high score from string.
        plyr=Player(name,int(highscore))#Turns high score into an int.
        playerList.append(plyr)#Appends player data to playerList.
    playerList.sort(key=useHighScore)#sets the key for sorting and sorts the list.
    playerList.reverse()#Reverses sorted HS list.
    y=5#variable to display the top 5 scores.
    for p in playerList[:5]:#(OTXT)Displays top 5 highest scores on new window.
        text1 = Text(Point(-3,y),p.getName())
        text1.setFill("cyan")
        text1.draw(win)
        text2=Text(Point(3,y),p.getHighScore())
        text2.setFill('cyan')
        text2.draw(win)
        y-=1
    return win

#Function draws a button and lets player play again upon click.
def playAgain(win):
    button=Rectangle(Point(1,-3),Point(7,-6))
    button.setFill("green")
    button.draw(win)
    playAgain=Text(Point(4,-4.5),"Play Again.")
    playAgain.setStyle("bold")
    playAgain.draw(win)
    while True:
        click=win.getMouse()
        dx=click.getX()
        dy=click.getY()
        if dx>=1 and dx<=7 and dy<=-3 and dy>=-6:#(IMS) Mouse location/Check.
            win.close()
            main()
        
#Image drawing function.        
def image(win):
    kraken=Image(Point(-4.5,-4.5),"kraken.png")
    kraken.draw(win)
               
#(FNC) Calling functions of my own design.
def main():
    win=window()#Calls main window
    player,diff=title(win)#Calls title function.
    score=gamePlay(win,diff)#Calls main gameplay function.
    player.highscore=int(score)#turns the high score into an int.
    save(player)#Save function of player data.
    win.close()#Closes window
    win2=display()#Opens High Score screen.
    image(win2)#Displays HS image.
    playAgain(win2)#Button for playing again.
main()

#Requirments
##(IEB) somewhere you read from an Entry box CHECK
##(OTXT) somewhere you write to the screen using Text CHECK
##(IFL) somewhere you read from an input file CHECK
##(OFL) somewhere you write to an output file CHECK
##(IMS) somewhere you use the mouse's location CHECK
##(GW) where you open a GraphWin CHECK
##(FNC) somewhere you call a function of your own design CHECK
##(RND) where you use a random number generator. CHECK
##(CLOD) where you define a class of your own design CHECK
#AND somewhere create an object of a class of your own design. CHECK
##(LOOD) somewhere you use a list of objects of your own design CHECK

##FUTURE Improvements:
##Upgrade Graphics (Maybe Turtle.)
##New kinds of targets.
##New random events.
##Music.(Version 0.9.5 has Pygame Library with working music.)


