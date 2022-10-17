import tkinter, time, random
from gamemath import *
from leaderboard import *

# this is the main class that stores the functions and information for the gui to function
class GameGui():
    def __init__(self): # setting up the gui
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, bg="black", height=600, width=900) # this is where the game will be rendered to 
        self.canvas.pack()
        self.gamestate = 0
        self.player = Player()

    def MouseClick(self, event): #this is where the controles for the game will be managed
        # if the game is running
        if self.gamestate == 1:
            vx, vy = Calc_Vel(10, self.player, event.x, event.y) #getting velocity between player and mouse click
            if self.player.lastshot + 0.55 < time.time(): # check that it has been a specific time since last time player shot a bullet
                self.player.bullets.append(Bullet(vx, vy)) # create bullet object and give it a velicity
                self.player.lastshot = time.time()  # set the last time the player shot
        # of we are at the menu
        elif self.gamestate == 0:
            if event.y >150 and event.y < 250: # start the game
                self.gamestate = 1
            elif event.y > 250 and event.y < 350: # view the leaderboard
                self.gamestate = 2
            elif event.y > 350 and event.y < 450: # exit the game
                self.gamestate = 3

                
        elif self.gamestate == 2:
            if event.y < 100 and event.x < 150:
                self.gamestate = 0

    def renderMenu(self): # this is just to render the menu for the player to look at.
        if self.gamestate == 0:
            self.canvas.create_text(450,100, text = "Meteor Survival!", fill= "Red", font=("Arial", 42, 'bold'))
            self.canvas.create_text(450,200, text = "Start Game", fill= "White", font=("Arial", 18, 'bold'))
            self.canvas.create_text(450,300, text = "Leaderboard", fill= "White", font=("Arial", 18, 'bold'))
            self.canvas.create_text(450,400, text = "Exit", fill= "White", font=("Arial", 18, 'bold'))
        elif self.gamestate == 2:
            self.canvas.create_text(75,50, text = "Back to\n Menu", fill= "White", font=("Arial", 12, 'bold'))
            
            self.canvas.create_text(450,75, text = "Leaderboard's top scores!", fill= "Red", font=("Arial", 24, 'bold'))
            HS_names, HS_scores = FetchScores()
            for i in range(min(len(HS_names),15)):
                self.canvas.create_text(450,150+25*i, text = str(i+1)+".   "+str(HS_names[i])+":  "+str(HS_scores[i]), fill= "White", font=("Arial", 12, 'bold'))
    
    def Update(self,  objects): # this is called to update the menu and rendert all of the game objects
        for obj in objects:
            obj.render(self.canvas) # render game objects
        if self.gamestate == 1:
            self.player.render(self.canvas) # render the player
            for bul in self.player.bullets:
                bul.render(self.canvas) # render the bullets from the player
                
            # just a lable so the player knows what it is            
            self.canvas.create_text(20,20, text = "Health:", fill= "white", font=("Arial", 18), anchor="w")
            # this is the health bar            
            self.canvas.create_rectangle(120, 10,100+(self.player.health*30),30,fill="lime")
            # this is the text that displays the players score
            self.canvas.create_text(20,50, text = "Score: "+ str(self.player.score), fill= "white", font=("Arial", 18), anchor="w")
        elif self.gamestate == 0 or self.gamestate == 2:
            self.renderMenu()
        self.root.update() # update the canvas so it will show to the screen
        self.canvas.delete("all") # remove everything on the screen for when we next render things
        

class GameObject(): # this is the main structure class that the gmae objects inherit from 
    def __init__(self, x, y, width, col): # this sets up all of the information that is given to be stored
        # these are basic variables that all of the classes will use or need
        self.x = x
        self.y = y
        self.width = width
        self.x_velocity = 0
        self.y_velocity = 0
        self.colour = col
        
    def render(self,canvas): # this uses the stored co-ordinates and a canvas imnput to render the object to the screen
        coords = self.x-self.width, self.y-self.width, self.x+self.width, self.y+self.width
        canvas.create_rectangle(coords, fill=self.colour)

    def set_velocity(self, xv, yv): # used to set/change the stored velocity of an object easier
        self.x_velocity = xv
        self.y_velocity = yv

    def move(self): # used to "move" the object by adding the velocity to the position.
        self.x+= self.x_velocity
        self.y+= self.y_velocity


class Player(GameObject): # player that inherits from base
    def __init__(self):
        super().__init__(450, 300, 12, "lime")  # this is the setup for the game object
        self.health = 3 # this is players health
        self.score = 0 # this is the players score
        self.bullets = [] # where the bullets that the player has shot are stored
        self.lastshot = 0 # this is the time that last bullet shot was so that te player can't just shoot forever

class Enemy(GameObject):    
    def __init__(self,x,y):
        self.isBoss = False
        self.isSpecial = bool(random.randint(1,10) == 1) # setting isSpecial to true every 1/10 times

        # set up for base class
        if self.isSpecial:
            #special are orange with a larger width
            super().__init__(x, y, 13, "orange") 
        else:
            super().__init__(x, y, 10, "red") 

class Bullet(GameObject):
    def __init__(self, vx, vy):
        super().__init__(450, 300, 4, "yellow") # setup for base class
        self.set_velocity(vx, vy) # set its velocity

class BossEnemy(GameObject): # Boss enemy class
    def __init__(self):
        self.currentpos = random.randint(0,3)
        start_pos = [[-100,150], [1000,150], [1000,450], [-100,450]]
        start_xvel = [5,-5,-5,5]
        super().__init__(start_pos[self.currentpos][0],start_pos[self.currentpos][1],35,"red")
        self.set_velocity(start_xvel[self.currentpos],0)
        self.isBoss = True
        self.health = 50
        self.currentAi = 0  # this is where the ai is stored
        self.aiTimer = 0  # this is to keep track of when the last time the ai changed
        self.positions = [[200,150],[700,150],[700,450],[200,450]] # Positions where the boss will sit around the player
    
    def BossAi(self):
        notMoving = False
        for i in self.positions:
            if self.x == i[0] and self.y == i[1]: # checking for the boss is in one of the outside positions  
                notMoving = True
                self.set_velocity(0, 0)
        if notMoving == True:
            if self.aiTimer + 2 < time.time():  # while the boss is not moving we cycle the ai
                self.currentAi = random.randint(0, 1)
                self.aiTimer = time.time()
                if self.currentAi == 0: # if the boss should move
                    target_pos = self.currentpos + random.choice([1,-1]) # choose where to move
                    if target_pos < 0: target_pos = 3
                    elif target_pos > 3: target_pos = 0
                    # move to that new position and set current position
                    xvel, yvel = Calc_Vel(5,self,self.positions[target_pos][0], self.positions[target_pos][1]) 
                    self.set_velocity(xvel,yvel)
                    self.currentpos = target_pos
        self.move() # make the boss move 

        
