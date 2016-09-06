#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import random
from math import cos
from math import sin
from math import pi


class SpaceObject(object):
    def __init__(self, window, image):
        # Sets an image's anchor point to its center
        image.anchor_x, image.anchor_y = image.width/2, image.height/2
        self.window = window
        
    def out_of_window(self):
        # when image moves out of window (pbc)
        w = self.window.width
        h = self.window.height
        return self.sprite.x % w, self.sprite.y % h  
       

class Spaceship(SpaceObject):
    def __init__(self, window, image):
        super(Spaceship, self).__init__(window, image)
        x = self.window.width/2
        y = self.window.height/2
        self.sprite = pyglet.sprite.Sprite(image, x, y, batch=batch)
        self.sprite.rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        
    def tick(self, t):
        acceleration = 0
        speed = pow(self.x_speed**2 + self.y_speed**2, 0.5)
        if 'SPEED_UP' in pressed_keys:
            acceleration = 0.1
        elif 'SLOW_DOWN' in pressed_keys:
            acceleration = -1
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


class Asteroid(SpaceObject):
    def __init__(self, window, image):
        super(Asteroid, self).__init__(window, image)
        x = 0
        y = random.uniform(0, self.window.height)
        self.sprite = pyglet.sprite.Sprite(image, x, y, batch=batch)
        self.sprite.rotation = 0
        # alebo to urobit ze celkova rychlost v nejakom rozmedzi a potom 
        # vx (a vy) uz nahodne
        self.x_speed = random.uniform(-1,1)
        self.y_speed = random.uniform(-1,1)
        
    def tick(self, t):
        self.sprite.x += self.x_speed
        self.sprite.y += self.y_speed
        # when image moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.out_of_window()
        
# Create a window
window = pyglet.window.Window(resizable=True)

# Setup our keyboard handler
key = pyglet.window.key
keys = key.KeyStateHandler()
window.push_handlers(keys)
pressed_keys = set()

batch = pyglet.graphics.Batch()

# Create a ship    
ship_image = pyglet.image.load('PNG/playerShip1_blue.png')
Ship = Spaceship(window, ship_image)

# Create an Asteroid
asteroid_image = pyglet.image.load('PNG/meteorBrown_big1.png')
asteroid1 = Asteroid(window, asteroid_image)

space_object = [Ship, asteroid1]

for obj in space_object:
    pyglet.clock.schedule_interval(obj.tick, 1./60)

@window.event
def on_draw():
    Ship.window.clear()
    batch.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        pressed_keys.add('SPEED_UP')
    if symbol == key.DOWN:
        pressed_keys.add('SLOW_DOWN')
    if symbol == key.RIGHT:
        pressed_keys.add('RIGHT')
    if symbol == key.LEFT:
        pressed_keys.add('LEFT')
        
@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.UP:
        pressed_keys.discard('SPEED_UP')
    if symbol == key.DOWN:
        pressed_keys.discard('SLOW_DOWN')
    if symbol == key.RIGHT:
        pressed_keys.discard('RIGHT')
    if symbol == key.LEFT:
        pressed_keys.discard('LEFT')

pyglet.app.run()