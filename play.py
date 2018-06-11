
import pickle
import os
import numpy as np

import neat
import checkpoint_plus
import super_mario

actions_list = [66,386,130,128,131]

timeout_constant = 20
radius = 3
display = True
random_seed = 20

with open('winner', 'rb') as f:
  c = pickle.load(f)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)
mario = super_mario.SuperMario(radius, display, random_seed)

timeout = timeout_constant
inputs, x, y = mario.reset()

rightmost = x
step = 0
fitness = 0
done = False

while not done:
  inputs = inputs.flatten()
  output = net.activate(inputs)
  
  a = np.argmax(output)
  action = 0
  if (output[a] > 0):
    action = actions_list[a]

  inputs, xn, yn, done = mario.step(action)
  
  if (xn > rightmost):
    rightmost = xn
    timeout = timeout_constant
      
  timeout = timeout - 1
  timeout_bonus = step / 4
  fitness = rightmost - step / 2
  
  if (timeout + timeout_bonus <= 0):
    break;
  
  step = step + 1

print('fitness = {0}'.format(fitness))
print('distance = {0}'.format(rightmost))
