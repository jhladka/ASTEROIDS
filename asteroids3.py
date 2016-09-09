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
        self.x_speed = 0
        self.y_speed = 0
        
    def out_of_window(self):
        # when image moves out of window (pbc)
        w = self.window.width
        h = self.window.height
        return self.sprite.x % w, self.sprite.y % h  
    
    def delete(self):
        space_object.remove(self)
        self.sprite.delete()
        return space_object
     

class Spaceship(SpaceObject):
    def __init__(self, window, image):
        super(Spaceship, self).__init__(window, image)
        x = self.window.width/2
        y = self.window.height/2
        self.sprite = pyglet.sprite.Sprite(image, x, y, batch=batch, group=foreground)
        self.sprite.rotation = 0
        self.radius = (self.sprite.height + self.sprite.width)/4
        
    def tick(self, t):
        acceleration = 0
        speed = pow(self.x_speed**2 + self.y_speed**2, 0.5)
        if 'SPEED_UP' in pressed_keys:
            acceleration = 0.05
        elif 'SLOW_DOWN' in pressed_keys:
            acceleration = -0.05
        elif 'RIGHT' in pressed_keys:
            self.sprite.rotation += 2
        elif 'LEFT' in pressed_keys:
            self.sprite.rotation -= 2
        # new angle in radians, counterclockwise motion
        angle = - (self.sprite.rotation*pi/180 - pi/2)
        # rotation of velocity
        self.x_speed = speed*cos(angle)
        self.y_speed = speed*sin(angle)
        # acceleration
        self.x_speed += acceleration * cos(angle)
        self.y_speed += acceleration * sin(angle)
        self.sprite.x += self.x_speed
        self.sprite.y += self.y_speed
        # when image moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.out_of_window()
        # check if there's a collision with other space object
        w = self.window.width
        h = self.window.height
        for obj in [o for o in space_object if o != self]:
            # calculates miminal distance between ship and object
            x = abs(self.sprite.x - obj.sprite.x)
            y = abs(self.sprite.y - obj.sprite.y)
            distance = pow(min(x, w-x)**2 + min(y, h-y)**2, 0.5)
            if distance < self.radius + obj.radius:
                obj.hit_by_spaceship(self)
                print Ship2
                break
        

class Asteroid(SpaceObject):
    def __init__(self, window, asteroid_images):
        # random image of Asteroid
        image = random.choice(asteroid_images)
        super(Asteroid, self).__init__(window, image)
        # random initial position of Asteroid at the edge
        position = [0, 0]
        window.dimension = [self.window.width, self.window.height]
        axis = random.choice([0, 1])
        position[axis] = random.uniform(0, window.dimension[axis])
        self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], batch=batch, group=foreground)
        self.sprite.rotation = 0
        self.radius = (self.sprite.height + self.sprite.width)/4
        # random initial velocity
        self.x_speed = random.uniform(-0.5, 0.5)
        self.y_speed = random.uniform(-0.5, 0.5)
        
    def tick(self, t):
        self.sprite.x += self.x_speed
        self.sprite.y += self.y_speed
        # when image moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.out_of_window()
        
    def hit_by_spaceship(self, ship):
        print space_object
        ship.delete()
        print space_object
        
        ship2_image = pyglet.image.load('PNG/playerShip1_green.png')
        global Ship2 
        Ship2 = Spaceship(window, ship2_image)
        space_object.append(Ship2)
        print space_object
        
    
### HERE BEGINS THE GAME ###
    
# Create a window
    
window = pyglet.window.Window(fullscreen=True)

# Setup our keyboard handler

key = pyglet.window.key
keys = key.KeyStateHandler()
window.push_handlers(keys)

pressed_keys = set()
key_control = {key.UP: 'SPEED_UP', 
               key.DOWN: 'SLOW_DOWN',
               key.RIGHT: 'RIGHT', 
               key.LEFT: 'LEFT'}

# ordered groups
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

batch = pyglet.graphics.Batch()

# resource paths. Resources folder must be on same level as this file.
pyglet.resource.path = ['PNG']
pyglet.resource.reindex()

# background
bg_image = pyglet.resource.image('blue.png')
universe = []
W = window.width
H = window.height
w = bg_image.width
h = bg_image.height
Nw = W/w + 1
Nh = H/h + 1
for i in xrange(Nw):
    for j in xrange(Nh):
        print i,j
        x = i*w
        y = j*h
        universe.append(pyglet.sprite.Sprite(img=bg_image, x=x, y=y, batch=batch, group=background))

### Create Ship ###   

ship_image = pyglet.resource.image('playerShip1_blue.png')
Ship = Spaceship(window, ship_image)

### Create Asteroids ###

number_of_asteroids = 5

meteors = ['meteorBrown_big1.png', 
           'meteorBrown_med1.png', 
           'meteorBrown_small1.png', 
           'meteorBrown_tiny1.png']
           
asteroid_images = [pyglet.resource.image(png) for png in meteors]

asteroids = []

for i in range(number_of_asteroids):
    asteroids.append(Asteroid(window, asteroid_images))

### all space objects ###

space_object = [Ship] + asteroids

for obj in space_object:
    pyglet.clock.schedule_interval(obj.tick, 1./60)
    
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