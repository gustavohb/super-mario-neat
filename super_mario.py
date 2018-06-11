

import sys
import pickle
import os
from rle_python_interface.rle_python_interface import RLEInterface
import numpy as np
from numpy.random import uniform, choice, random
from itertools import product


class SuperMario(object):
  
  actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3, 
               'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67, 
               'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131, 
               'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
               }
  
  def __init__(self, radius=3, display=False, random_seed = 20):
    self.radius = radius
    self.random_seed = random_seed
    self.display = display
    
    self._load_interface()
    
  
  def _load_interface(self):
    self.rle = RLEInterface()

    self.rle.setInt(b'random_seed', self.random_seed)
    self.rle.setBool(b'sound', False)
    
    if sys.platform == 'darwin':
      import pygame
      pygame.init()
    self.rle.setBool(b'display_screen', self.display)

  def get_xy(self):
    ram = self.rle.getRAM()
    x = ram[0x95]*256 + ram[0x94]
    y = ram[0x97]*256 + ram[0x96]
    
    return x.astype(np.int16), y.astype(np.int16)
  
  def get_sprites(self):
    sprites = []
    ram = self.rle.getRAM()
    
    for slot in range(12):
      status = ram[0x14C8+slot]
      if status != 0:
        sprite_x = ram[0xE4+slot] + ram[0x14E0+slot]*256
        sprite_y = ram[0xD8+slot] + ram[0x14D4+slot]*256
        
        sprite_size = ram[0x0420+ram[0x15EA+slot]]
        sprite_id   = ram[0x15EA+slot]
        
        if sprite_id != 44 and sprite_id != 216:
          size = 1
          
          if sprite_size == 0:
            size = 4
          sprites.append({'x': sprite_x, 'y': sprite_y, 'size': size})
        
    return sprites
    
  def get_tile(self, dx, dy):
    
    x = np.floor(dx/16)
    y = np.floor(dy/16)
    ram = self.rle.getRAM()
    
    return ram[0x1C800 + np.int(np.floor(x/16)*432 + y*16 + x%16)]
  
  def _within_limits(self, idx, ds1, ds2):
    maxlen = (self.radius*2+1)*(self.radius*2+1)
    return (idx%(2*self.radius + 1) + ds2 < 2*self.radius + 1) and (idx + ds1*(2*self.radius + 1) + ds2 < maxlen)
     
      
  def get_inputs(self):
    x, y = self.get_xy()
    sprites = self.get_sprites()
    
    maxlen = (self.radius*2+1)*(self.radius*2+1)
    inputs = np.zeros(maxlen, dtype=int)
    
    window = (-self.radius*16, self.radius*16 + 1, 16)
    j = 0
    
    for dy, dx in product(range(*window), repeat=2):
      tile = self.get_tile(x+dx+8, y+dy)
    
      if tile==1 and y+dy < 0x1B0:
        inputs[j] = 1
      
      for i in range(len(sprites)):
        distx = np.abs(sprites[i]['x'] - x - dx)
        disty = np.abs(sprites[i]['y'] - y - dy)
        size = sprites[i]['size']
        
        if distx <= 8 and disty <= 8:
        
          for s1, s2 in product(range(size), repeat=2):
            if self._within_limits(j, s1, s2):
              inputs[j + s1*(self.radius*2 + 1) + s2] = -1
        
      j = j + 1
    
    return inputs, x, y
    
  def reset(self):
    self.rle.loadROM('super_mario_world.smc', 'snes')
    return self.get_inputs()
  
  def step(self, action):

    if action == 64 or action == 128:
      for it in range(8):
        self.rle.act(action)
    elif action == 66 or action == 130:
      for it in range(4):
        self.rle.act(action)
    elif action == 131 or action == 67:
      for it in range(8):
        self.rle.act(action)
    elif action == 386 or 322:
      for it in range(4):
        self.rle.act(action)
    else:
      self.rle.act(action)
      
    inputs, x, y = self.get_inputs()
    done = self.rle.game_over()
    
    return inputs, x, y, done


