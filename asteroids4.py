#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import random
from math import cos
from math import sin
from math import pi
#from pyglet.gl import *

class SpaceObject(object):
    def __init__(self, window, image):
        # Sets an image's anchor point to its center
        image.anchor_x, image.anchor_y = image.width/2, image.height/2
        self.window = window
        
    def tick(self, dt, w, h):
        # update position of space object
        self.sprite.x += self.x_speed*dt
        self.sprite.y += self.y_speed*dt
        # if space object moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.backToWindow(w, h)
        
    def backToWindow(self, w, h):
        # when image moves out of window (pbc)
        return self.sprite.x % w, self.sprite.y % h  
    
    def delete(self):
        # delete sprite and space object from list of space objects
        space_object.remove(self)
        self.sprite.delete()     # re­move sprite from graph­ics batch
        
    def distance(self, other, W, H):
        # calculates minimal distance between two objects
        x = abs(self.sprite.x - other.sprite.x)
        y = abs(self.sprite.y - other.sprite.y)
        return pow(min(x, W-x)**2 + min(y, H-y)**2, 0.5)

    def hit_by_spaceship(self, other):
        pass
     
    def hit_by_laser(self, other):
        pass 
    

class Spaceship(SpaceObject):
    def __init__(self, window, img):
        super(Spaceship, self).__init__(window, img)
        self.x_speed = 0
        self.y_speed = 0
        x = self.window.width/2
        y = self.window.height/2
        self.sprite = pyglet.sprite.Sprite(img, x, y, batch=batch, group=foreground)
        self.sprite.rotation = 0
        self.radius = (self.sprite.height + self.sprite.width)/4
        self.fire = 0.0
        
    def tick(self, dt, w, h):
        acceleration = 0
        speed = pow(self.x_speed**2 + self.y_speed**2, 0.5)
        if 'SPEED_UP' in pressed_keys:
            acceleration = 100
        if 'SLOW_DOWN' in pressed_keys:
            acceleration = -100
        if 'RIGHT' in pressed_keys:
            self.sprite.rotation += 2
        if 'LEFT' in pressed_keys:
            self.sprite.rotation -= 2
        if 'FIRE' in pressed_keys:
            if self.fire < 0:
                fireLaser(self.sprite.x, self.sprite.y, 
                          speed, self.sprite.rotation, self.radius)
                self.fire = 0.3
        self.fire -= dt
        # new angle in radians, counterclockwise motion
        angle = - (self.sprite.rotation*pi/180 - pi/2)
        # rotation of velocity
        self.x_speed = speed*cos(angle)
        self.y_speed = speed*sin(angle)
        # acceleration
        self.x_speed += acceleration*cos(angle)*dt
        self.y_speed += acceleration*sin(angle)*dt
        self.sprite.x += self.x_speed*dt
        self.sprite.y += self.y_speed*dt
        # when image moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.backToWindow(w, h)
        # check if there's a collision with other space object
        for obj in [o for o in space_object if o != self]:
            d = self.distance(obj, w, h)
            if d < self.radius + obj.radius:
                obj.hit_by_spaceship(self)
                break
        

class Asteroid(SpaceObject):
    def __init__(self, window, asteroid_image, size, x=None, y=None, x_speed=None, y_speed=None):
        self.size = size
        img = pyglet.resource.image(asteroid_image)
        super(Asteroid, self).__init__(window, img)
        # random initial position of Asteroid at the edge of screen
        if x == None:
            position = [0, 0]
            window.dimension = [self.window.width, self.window.height]
            axis = random.choice([0, 1])
            position[axis] = random.uniform(0, window.dimension[axis])
            x, y = position[0], position[1]
        # random initial speed of Asteroid
        if x_speed == None:
            x_speed=random.uniform(-100, 100)
            y_speed=random.uniform(-100, 100)
        self.sprite = pyglet.sprite.Sprite(img, x, y, batch=batch, group=foreground)
        self.sprite.rotation = 0
        self.radius = (self.sprite.height + self.sprite.width)/4
        # random initial velocity
        self.x_speed = x_speed
        self.y_speed = y_speed
        
    def hit_by_spaceship(self, ship):
        # delete Spaceship and create new one
        ship.delete()
        createNewShip()
        
    def hit_by_laser(self, laser):
        # delete Asteroid when it's smallest
        # or create 2 smaller
        if self.size < min_size:
            for i in ([-1, 1],[1, -1]):
                size = self.size + 1
                img = random.choice(meteors[size])
                angle = - (laser.sprite.rotation*pi/180 - pi/2)
                x = self.sprite.x + self.radius*cos(angle)
                y = self.sprite.y + self.radius*sin(angle)
                x_speed = 1.5*i[0]*self.y_speed
                y_speed = 1.5*i[1]*self.x_speed
                space_object.append(Asteroid(window, img, size, x=x, y=y, x_speed=x_speed, y_speed=y_speed))
        laser.delete()
        self.delete()
        

class Laser(SpaceObject):
    def __init__(self, img, x, y, x_speed, y_speed, rotation):
        super(Laser, self).__init__(window, img)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.sprite = pyglet.sprite.Sprite(img, x, y, batch=batch, group=foreground)
        self.sprite.rotation = rotation
        self.radius = (self.sprite.height + self.sprite.width)/4
    
    def tick(self, dt, w, h):
        super(Laser, self).tick(dt, w, h)
        # check if there's a collision with other space object
        for obj in [o for o in space_object if o != self]:
            d = self.distance(obj, w, h)
            if d < self.radius + obj.radius:
                obj.hit_by_laser(self)
                break
    

def fill_background(image):
    # fill background with image of universe
    bg_image = pyglet.resource.image(image)
    universe = []
    W, H = window.width, window.height
    w, h = bg_image.width, bg_image.height
    Nw, Nh = W/w + 1, H/h + 1
    for i in xrange(Nw):
        for j in xrange(Nh):
            x, y = i*w, j*h
            universe.append(pyglet.sprite.Sprite(img=bg_image, x=x, y=y, batch=batch, group=background))
    return universe
   
   
def update(dt):
    for obj in space_object:
        w = window.width
        h = window.height
        obj.tick(dt, w, h)


def createNewShip():
    # reset game; create new ship in the middle of screen
    global next_img
    img = ship_images[next_img]
    next_img = (next_img + 1)%nb_img
    ship_image = pyglet.resource.image(img)
    ship = Spaceship(window, ship_image)
    space_object[:] = [ship] + space_object
       

def fireLaser(ship_x, ship_y, ship_speed, rotation, ship_radius):
    img = 'laserGreen02.png'
    laser_img = pyglet.resource.image(img)
    # new angle in radians, counterclockwise motion
    angle = - (rotation*pi/180 - pi/2)
    x = ship_x + 1.55*ship_radius*cos(angle)
    y = ship_y + 1.55*ship_radius*sin(angle)
    speed = ship_speed + 500
    x_speed = speed*cos(angle)
    y_speed = speed*sin(angle)
    laser = Laser(laser_img, x, y, x_speed, y_speed, rotation)
    space_object[:] = [laser] + space_object
    dt = 1.1*window.width/speed
    pyglet.clock.schedule_once(deleteLaser, dt, laser=laser)
    
   
def deleteLaser(dt, laser):
    if laser in space_object:
        laser.delete()


### HERE BEGINS THE GAME ###
    
# Create a window
window = pyglet.window.Window(fullscreen=True)

# Setup our keyboard handler
key = pyglet.window.key
keys = key.KeyStateHandler()
window.push_handlers(keys)

pressed_keys = set()
key_control = {key.UP:    'SPEED_UP', 
               key.DOWN:  'SLOW_DOWN',
               key.RIGHT: 'RIGHT', 
               key.LEFT:  'LEFT',
               key.SPACE: 'FIRE'}

# ordered groups
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

batch = pyglet.graphics.Batch()

# resource paths. Resources folder must be on same level as this file.
pyglet.resource.path = ['PNG']
pyglet.resource.reindex()

# fill background with image of universe
universe = fill_background('blue.png')

### Create Asteroids ###
number_of_asteroids = 4
size = 0    # the biggest Asteroids
meteors = [['meteorBrown_big1.png',
            'meteorBrown_big2.png',
            'meteorBrown_big3.png',
            'meteorBrown_big4.png'],
           ['meteorBrown_med1.png'],
           ['meteorBrown_small1.png'], 
           ['meteorBrown_tiny1.png']]
min_size = len(meteors) - 1
space_object = []
for i in range(number_of_asteroids):
    img = random.choice(meteors[size])
    space_object.append(Asteroid(window, img, size))
    
# create Ship
ship_images = ['playerShip1_blue.png',
               'playerShip1_green.png',
               'playerShip1_orange.png',
               'playerShip1_red.png']
nb_img = len(ship_images)
next_img = 0
createNewShip()

pyglet.clock.schedule_interval(update, 1./60)
    
@window.event
def on_draw():
    window.clear()
    batch.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if symbol in key_control:
        pressed_keys.add(key_control[symbol])
        
@window.event
def on_key_release(symbol, modifiers):
    if symbol in key_control:
        pressed_keys.discard(key_control[symbol])
        
pyglet.app.run()