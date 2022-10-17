import time
import random
from gameclasses import *
from gamemath import *
from leaderboard import *

def HandleGameOver(Game, GameOverWindow):
    while GameOverWindow.player_name == "": # checking to see if the player has input a name
        Game.root.update()
    SaveScore(GameOverWindow.player_name, Game.player.score) # save that score and name
    #reset variables for when the player starts a new game
    Game.gamestate = 0
    Game.player.score = 0
    Game.player.health = 3


def HandleEnemySpawns(Game, objects, lastSpawn, spawnBoss, BossActive): # this is handle if we should spawn an enemy
    if spawnBoss and BossActive == False:
        BossActive = True
        objects.append(BossEnemy())
    if BossActive:
        counter = 0
        foundBoss = False
        for i in objects:
            if i.isBoss == True:
                foundBoss = True
                objects[counter].BossAi()
                if i.currentAi == 1: # if the boss object should be shooting
                    if time.time()-0.75 > lastSpawn:
                        obj = Enemy(i.x,i.y)
                        if obj.isSpecial:
                            xv, yv = Calc_Vel(6, obj, Game.player.x, Game.player.y)
                        else:
                            xv, yv = Calc_Vel(4, obj, Game.player.x, Game.player.y)                
                        obj.set_velocity(xv, yv)
                        objects.append(obj)
                        lastSpawn = time.time()  # set the last time that we spawned an enemy
            counter += 1
        if not foundBoss:
            BossActive = False
    elif time.time()-1 > lastSpawn:
        side = random.randint(1, 4)  # pick a random side to spawn the enemy on
        if side == 1: x = random.randint(0, 900); y = 0 
        elif side == 2: x = random.randint(0, 900); y = 600 
        elif side == 3: x = 0; y = random.randint(0, 600)
        else: x = 900;y = random.randint(0, 600)
        obj = Enemy(x,y)
        if obj.isSpecial:
            xv, yv = Calc_Vel(6, obj, Game.player.x, Game.player.y)
        else:
            xv, yv = Calc_Vel(4, obj, Game.player.x, Game.player.y)                
        obj.set_velocity(xv, yv)
        objects.append(obj)  # add this enemy to the object list
        lastSpawn = time.time()  # set the last time that we spawned an enemy

    return lastSpawn, BossActive

def HandleGameCollision(Game, Objects): # collision detection for game
    for bul in Game.player.bullets: # if the bullet goes off screen we dont need it anymore so pop it
        if bul.x > 900 or bul.x < 0 or bul.y > 600 or bul.y < 0:
            Game.player.bullets.pop(0)
            break
    counter = 0
    for obj in Objects: # checking the objects to see if they have hit anything
        for bul in Game.player.bullets: # if a bullet from the player had hit the object
            if Did_Hit(obj, bul):
                if obj.isBoss == False:
                    Objects.pop(counter)
                    if obj.isSpecial:
                        Game.player.score += 3 # give the player more poiunts for special
                    else:
                        Game.player.score += 1 # give the player a point for killing an enemy
                else:
                    Objects[counter].health-=1
                    if Objects[counter].health <= 0:
                        Objects.pop(counter)
                        Game.player.score += 10 # give the player a point for killing an enemy
                break
        if Did_Hit(obj, Game.player): # if the object has hit the player
            Objects.pop(counter)
            if Game.gamestate == 1:
                Game.player.health -= 1 # take away health for getting hit
                if Game.player.health <= 0: # if the player is dead
                    GameOverWindow = PopUp(Game.root, Game.player.score) # open a popup 
                    HandleGameOver(Game, GameOverWindow) # run game over function. 
            break
        counter += 1

# make all objects run their move function
def HandleGameMovement(Game,Objects):
    for bul in Game.player.bullets:
        bul.move()
    for obj in Objects:
        if obj.isBoss == False:
            obj.move()

    
