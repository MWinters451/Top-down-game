# import modules and from other files 
from gameclasses import *
from gamemath import *
from gameloop import *
import time, random

if __name__ == "__main__":
    #setting up everything used for the game
    Game = GameGui() # class that controls the gui of the program
    Game.canvas.bind("<Button-1>", Game.MouseClick) # binding game controls
    # other variables used
    objects = []
    lastSpawn = 0
    Game.gamestate = 0
    lastgamestate = Game.gamestate
    bossActive = False
    bossTrigger = 25
    # main game loop
    while Game.gamestate != 3:
        # update what is rendered
        Game.Update(objects)
        # spawning enemies
        lastSpawn, bossActive = HandleEnemySpawns(Game, objects, lastSpawn,Game.player.score > bossTrigger, bossActive)
        # if there is a boss increase the trigger to the next value
        if bossActive and Game.player.score > bossTrigger: bossTrigger += 50
        # these are what control the game logic
        HandleGameCollision(Game, objects)
        HandleGameMovement(Game, objects)
        # if game state changes, clear background
        if not lastgamestate == Game.gamestate:
            objects = []
            lastgamestate = Game.gamestate
            bossTrigger = 25
            
        # this is to control how fast the game is running
        time.sleep(0.05)
    # close the window if exiting game
    Game.root.destroy() 
