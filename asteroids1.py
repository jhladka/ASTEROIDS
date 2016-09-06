#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
from math import cos
from math import sin
from math import pi

class Spaceship():
    def __init__(self, window, image):
        self.window = window
        self.x_speed = 0
        self.y_speed = 0
        # Sets an image's anchor point to its center
        image.anchor_x, image.anchor_y = image.width/2, image.height/2
        x, y = self.window.width/2, self.window.height/2
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.sprite.rotation = 0
    
    def out_of_window(self):
        # when image moves out of window (pbc)
        w = self.window.width
        h = self.window.height
        return self.sprite.x % w, self.sprite.y % h
    
    def tick(self, t):
        acceleration = 0
        if 'SPEED_UP' in pressed_keys:
            acceleration = 1
        elif 'SLOW_DOWN' in pressed_keys:
            acceleration = -1
        elif 'RIGHT' in pressed_keys:
            self.sprite.rotation += 2
        elif 'LEFT' in pressed_keys:
            self.sprite.rotation -= 2
        angle = - (self.sprite.rotation*pi/180 - pi/2)
        self.x_speed += acceleration * cos(angle)
        self.y_speed += acceleration * sin(angle)
        self.sprite.x += self.x_speed
        self.sprite.y += self.y_speed
        #self.sprite.x += self.x_speed 
        #self.sprite.y += self.y_speed
        # when image moves out of window (pbc)
        self.sprite.x, self.sprite.y = self.out_of_window()
        
        
# Create a window
window = pyglet.window.Window(resizable=True)

# Setup our keyboard handler
key = pyglet.window.key
keys = key.KeyStateHandler()
window.push_handlers(keys)
pressed_keys = set()

# Create a ship    
ship_image = pyglet.image.load('playerShip1_blue.png')   
Ship = Spaceship(window, ship_image)

pyglet.clock.schedule_interval(Ship.tick, 1./60)

@window.event
def on_draw():
    Ship.window.clear()
    Ship.sprite.draw()
    
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