#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import random
from math import cos
from math import sin
from math import pi
from pyglet.gl import *

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

    def circle(self, Sprite):
        x0 = Sprite.x
        y0 = Sprite.y
        radius = (Sprite.height + Sprite.width)/4 
        numPoints = 200
        coordinates = []
        for i in xrange(numPoints):
            angle = 2*i*pi/numPoints
            x = x0 + radius * cos(angle) 
            y = y0 + radius * sin(angle)
            coordinates += [x, y]
        return numPoints, ('v2f', coordinates)
    """
    def delete(self):
        objects.remove(self)
        !!! a vymazat sprite z batch
        return objects
    """   

class Spaceship(SpaceObject):
    def __init__(self, window, image):
        super(Spaceship, self).__init__(window, image)
        x = self.window.width/2
        y = self.window.height/2
        self.sprite = pyglet.sprite.Sprite(image, x, y, batch=batch)
        self.sprite.rotation = 0
        n, xy = self.circle(self.sprite)
        self.Circle = batch.add(n, GL_POINTS, None, xy)
        
    def tick(self, t):
        self.Circle.delete()
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
            """
            if distance < self.circle() + obj.circle():
                obj.hit_by_spaceship(self)
            """
        n, xy = self.circle(self.sprite)
        self.Circle = batch.add(n, GL_POINTS, None, xy)
        

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
        self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], batch=batch)
        self.sprite.rotation = 0
        # random initial velocity
        self.x_speed = random.uniform(-0.5, 0.5)
        self.y_speed = random.uniform(-0.5, 0.5)
        
    def tick(self, t):
        self.sprite.x += self.x_speed
        self.sprite.y += self.y_speed
        # when image moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.out_of_window()
        
    def hit_by_spaceship(self, ship):
        ship.delete()        
    
    
### HERE BEGINS THE GAME ###
# Create a window
window = pyglet.window.Window(resizable=True)

# Setup our keyboard handler
key = pyglet.window.key
keys = key.KeyStateHandler()
window.push_handlers(keys)

pressed_keys = set()
key_control = {key.UP: 'SPEED_UP', 
               key.DOWN: 'SLOW_DOWN',
               key.RIGHT: 'RIGHT', 
               key.LEFT: 'LEFT'}

batch = pyglet.graphics.Batch()

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

### Create a Ship ###   
ship_image = pyglet.image.load('PNG/playerShip1_blue.png')
Ship = Spaceship(window, ship_image)

### Create Asteroids ###
number_of_asteroids = 5
meteors = ['PNG/meteorBrown_big1.png', 
           'PNG/meteorBrown_med1.png', 
           'PNG/meteorBrown_small1.png', 
           'PNG/meteorBrown_tiny1.png']
asteroid_images = [pyglet.image.load(png) for png in meteors]
asteroids = []
for i in range(number_of_asteroids):
    asteroids.append(Asteroid(window, asteroid_images))

space_object = [Ship] + asteroids
for obj in space_object:
    pyglet.clock.schedule_interval(obj.tick, 1./60)

pyglet.app.run()