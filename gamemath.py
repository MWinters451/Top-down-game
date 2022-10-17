# import math module for trigonometric functions
import math

def Calc_Vel(velocity, obj, target_x, target_y): # to colculate the direction an object needs to travel

    if target_x == obj.x and target_y == obj.y: # if at target dont move
        return 0, 0

    #this will prevent the chance that there is a division by 0
    
    if target_x == obj.x and not target_y == obj.y: # checking x coordinate
        diff = target_y-obj.y
        if diff <= 0:
            return 0, max(-velocity,diff)
        else:
            return 0, min(diff,velocity)

    if not target_x == obj.x and target_y == obj.y: # checking y coordinate
        diff = target_x-obj.x
        if diff >=0:
            return min(diff, velocity), 0
        else:
            return max(diff, -velocity), 0    
    
    if obj.y < target_y:
        angle = math.atan((target_x-obj.x)/(target_y-obj.y)) # no longer a possible division by 0
        x_velocity =velocity*math.sin(angle)
        y_velocity =velocity*math.cos(angle)
        return x_velocity, y_velocity
    else:
        angle = math.atan((target_y-obj.y)/(target_x-obj.x)) # no longer a possible division by 0
        x_velocity =velocity*math.cos(angle)
        y_velocity =velocity*math.sin(angle)
        if obj.y>target_y and obj.x > target_x:
            return-x_velocity,-y_velocity
        else:
            return x_velocity, y_velocity

def Did_Hit(obj1, obj2):
    distance = obj1.width + obj2.width
    # checking if the objects overlap
    if obj1.x - obj2.x < distance and obj1.x - obj2.x > -distance and obj1.y - obj2.y < distance and obj1.y - obj2.y > -distance:
        return True
    return False
