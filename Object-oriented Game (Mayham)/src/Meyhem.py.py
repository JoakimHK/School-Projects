import pygame as py
import random
import math
from pygame import Vector2 as vec
import config

# - make bullets
#
#


class VisualObject(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.size = (80, 80)

        self.position = vec(self.x, self.y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        self.angle = 0






class Obstacle(VisualObject):
    def __init__(self, PNG, PosXY):
        VisualObject.__init__(self)
        self.size = (config.OBSTACLE_SIZE)
        self.image = py.transform.scale(PNG, (self.size))
        self.position = (PosXY)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

class Player(VisualObject):
    def __init__(self, PNG, PNG2, ID):
        VisualObject.__init__(self)
        self.image = PNG
        self.boostIMG = py.transform.scale(PNG2, (self.size))
        self.image = py.transform.scale(self.image, (self.size))
        self.orig_image = self.image
        self.ID = ID
        self.isBoosting = False
        self.fuelP1 = config.Maxfuel
        self.fuelP2 = config.Maxfuel

        if self.ID == 1:
            self.position = config.P1_start
        if self.ID == 2:
            self.position = config.P2_start

        self.cooldown = 0
        self.scoreP1  = 0
        self.scoreP2  = 0

        self.Drops = py.sprite.Group()

        self.rect = self.image.get_rect()
        self.rect.center = self.position



    def keyPress(self):

        if self.ID == 1:
            if config.key()[py.K_a]:
                self.turn(config.rotationSpeed)
            if config.key()[py.K_d]:
                self.turn(-config.rotationSpeed)
            if config.key()[py.K_w]:
                self.boost()

            if config.key()[py.K_v]:
                if self.cooldown == 0:
                    bullet = Fire(config.Drop, self.angle, self.position)
                    self.Drops.add(bullet)  
                    self.cooldown = config.shotcooldown

        if self.ID == 2:
            if config.key()[py.K_LEFT]:
                self.turn(config.rotationSpeed) 
            if config.key()[py.K_RIGHT]:
                self.turn(-config.rotationSpeed)
            if config.key()[py.K_UP]:
                self.boost()
            
            if config.key()[py.K_m]:
                if self.cooldown == 0:
                    bullet = Fire(config.Drop, self.angle, self.position)
                    self.Drops.add(bullet)  
                    self.cooldown = config.shotcooldown
                

                
    def boost(self):
        self.acceleration += config.Boost.rotate(-self.angle)

        self.isBoosting = True

    
    def turn(self, number):
        self.angle += number
        self.angle %= 360


    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        self.keyPress()

        if self.isBoosting:
            self.image = py.transform.rotozoom(self.boostIMG, self.angle, 1)
        else:
            self.image = py.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect  = self.image.get_rect()
        self.rect.center = self.position

        self.acceleration += config.Gravity
        self.velocity += self.acceleration

        if self.velocity.length() > config.maxVel:
            self.velocity.scale_to_length(config.maxVel)
        self.position += self.velocity 
        self.rect.center = self.position

        self.acceleration *= 0
        self.position.x %= config.SCREEN_SIZE[0]
        self.position.y %= config.SCREEN_SIZE[1]

        self.isBoosting = False

        #print(self.angle)

class Fire(VisualObject):
    def __init__(self, PNG, angle, position):
        VisualObject.__init__(self)

        self.acceleration = vec(0, -1).rotate(-angle)
        self.image = py.transform.rotozoom(PNG, angle, 1)

        self.rect = self.image.get_rect()
        self.rect.center = position + self.acceleration*50

    def update(self):
        self.rect.center += self.acceleration*7
    

class Platform(VisualObject):
    def __init__(self, POS):
        VisualObject.__init__(self)
        self.image = config.PlatformPNG
        self.rect = self.image.get_rect()
        self.rect.center = POS
    





class Game():
    def __init__(self):
        self.screen = py.display.set_mode(config.SCREEN_SIZE)
        self.clock  = py.time.Clock()

        self.Turtles   = py.sprite.Group()
        self.Obstacles = py.sprite.Group()
        self.Platforms = py.sprite.Group()

        self.Turtles.add(Player(config.TurtleGreen1, config.TurtleGreen2, 1))
        self.Turtles.add(Player(config.TurtleBlue1, config.TrutleBlue2, 2))

        self.Platforms.add(Platform(config.P1_fuelpadPos))
        self.Platforms.add(Platform(config.P2_fuelpadPos))

        self.Obstacles.add(Obstacle(config.Obstacle, config.ObstaclePosition))

    def Collision(self):
        for turtle in self.Turtles:
            if py.sprite.spritecollide(turtle, self.Obstacles, 0, py.sprite.collide_mask):
                if turtle.ID == 1:
                    turtle.position  = config.P1_start
                    turtle.velocity *= 0
                    turtle.angle     = 0

                    turtle.scoreP1 -= 10
                    turtle.fuelP1   = config.Maxfuel

                if turtle.ID == 2:
                    turtle.position  = config.P2_start
                    turtle.velocity *= 0
                    turtle.angle     = 0

                    turtle.scoreP2 -= 10
                    turtle.fuelP2   = config.Maxfuel

            py.sprite.groupcollide(turtle.Drops, self.Obstacles, True, False, py.sprite.collide_mask)
            for other in self.Turtles:
                if other != turtle and py.sprite.spritecollide(turtle, other.Drops, True, py.sprite.collide_mask):
                    if turtle.ID == 1:
                        turtle.position  = config.P1_start
                        turtle.velocity *= 0
                        turtle.angle     = 0

                        turtle.scoreP1   -= 20
                        other.scoreP2    += 50
                        turtle.fuelP1   = config.Maxfuel

                    if turtle.ID == 2:
                        turtle.position  = config.P2_start
                        turtle.velocity *= 0
                        turtle.angle     = 0

                        turtle.scoreP2   -= 20
                        other.scoreP1    += 50
                        turtle.fuelP2   = config.Maxfuel

                if other != turtle and py.sprite.collide_mask(turtle, other):
                    turtle.velocity *= -1
        
            for drop in turtle.Drops:
                if drop.position.x < 0 - drop.size[0]:
                    turtle.Drops.remove(drop)

                if drop.position.x > config.SCREEN_SIZE[0]:
                    turtle.Drops.remove(drop)

                if drop.position.y < 0 - drop.size[1]:
                    turtle.Drops.remove(drop)

                if drop.position.y > config.SCREEN_SIZE[1]:
                    turtle.Drops.remove(drop)
            if py.sprite.spritecollide(turtle, self.Platforms, False, py.sprite.collide_mask):
                if turtle.ID == 1:
                    turtle.velocity *= 0
                    if turtle.fuelP1 < config.Maxfuel:
                        turtle.fuelP1 += config.FuelRefill
                if turtle.ID == 2:
                    turtle.velocity *= 0
                    if turtle.fuelP2 < config.Maxfuel:
                        turtle.fuelP2 += config.FuelRefill
        

            
    def main(self):
        py.init()
        
        while True:
            events = py.event.get()
            for event in events:
                if event.type == py.QUIT:
                    exit()
            
            self.screen.fill(config.white)
            self.clock.tick(60)

            self.Collision()
            self.Turtles.update()
            for turtle in self.Turtles:
                turtle.Drops.update()
                turtle.Drops.draw(self.screen)
            self.Turtles.draw(self.screen)

            self.Obstacles.draw(self.screen)

            self.Platforms.draw(self.screen)

            

        #Fuel bars dor the Turtles
            for turtle in self.Turtles:
                if turtle.ID == 1:
                    if turtle.fuelP1 > 0:
                        turtle.fuelP1 += config.FuelDegrade
                    else:
                        turtle.velocity *= 0
                    py.draw.rect(self.screen, config.red,(config.P1_FuelScorePos[0], config.P1_FuelScorePos[1], turtle.fuelP1, 10))
                if turtle.ID == 2:
                    if turtle.fuelP2 > 0:
                        turtle.fuelP2 += config.FuelDegrade 
                    else:
                        turtle.velocity *= 0
                    py.draw.rect(self.screen, config.red,(config.P2_FuelScorePos[0], config.P2_FuelScorePos[1], turtle.fuelP2, 10))
            
            
            
        #Turtle player scores 
            for turtle in self.Turtles:
                font = py.font.Font(None, 44)
                if turtle.ID == 1:
                    text1 = font.render("Player 1:" + str(turtle.scoreP1), True, config.black)
                if turtle.ID == 2:
                    text2 = font.render("Player 2:" + str(turtle.scoreP2), True, config.black)
            self.screen.blit(text1, config.P1_textPos)
            self.screen.blit(text2, config.P2_textPos)

            py.display.update()

if __name__ == '__main__':
    game = Game()
    game.main()