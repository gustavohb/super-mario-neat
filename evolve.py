from __future__ import print_function

import super_mario

import neat
import numpy as np
import os
import pickle
import sys

import checkpoint_plus


actions_list = [66,386,130,128,131]

timeout_constant = 20
radius = 3
random_seed = 20
display = False

best_genome = None
best_fitness = 0
checkpointer = None
stats = None
pop = None
mario = None

def eval_genome(genome, config):
  global rle, best_fitness, best_genome, mario
  net = neat.nn.FeedForwardNetwork.create(genome, config)
  
  inputs, x, y = mario.reset()
  
  rightmost = x
  timeout = timeout_constant
  current_frame = 0
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
    timeout_bonus = current_frame / 4

    fitness = rightmost - current_frame / 2
    
    if (rightmost > 4816):
      fitness = fitness + 1000

    if (timeout + timeout_bonus <= 0):
      break;
    
    current_frame = current_frame + 1
    
  if (fitness > best_fitness):
    best_fitness = fitness
    best_genome = genome
    print('best_fitness = {0}'.format(best_fitness))
  print('rightmost = {0}'.format(rightmost))
  
  return fitness


def eval_genomes(genomes, config):
  filename = 'neat-checkpoint'
  
  for genome_id, genome in genomes:
    print('genome[{0}].fitness = {1}'.format(genome_id, genome.fitness))
    
    if (genome.fitness == None):
      genome.fitness = eval_genome(genome, config)   
      checkpointer.save_checkpoint(pop, best_genome, stats, filename)
      print('genome[{0}].fitness = {1}'.format(genome_id, genome.fitness))
  
  if (checkpointer.current_generation % 5 == 0):
    checkpointer.save_checkpoint(pop, best_genome, stats, '{0}-{1}'.format(filename, checkpointer.current_generation))


def run():
  global pop, stats, best_genome, checkpointer, best_fitness, mario
  
  mario = super_mario.SuperMario(radius, display, random_seed)
  
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config')
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path) 
  pop = neat.Population(config)
  stats = neat.StatisticsReporter()
  
  filename = 'neat-checkpoint'
  
  if (os.path.isfile(filename)):
    pop, stats =  checkpoint_plus.CheckpointerPlus.restore_checkpoint(filename)
    best_genome = pop.best_genome
    best_fitness = best_genome.fitness
    print('best_fitness = {0}'.format(best_fitness))
    
  pop.add_reporter(neat.StdOutReporter(True))
  pop.add_reporter(stats)
  checkpointer = checkpoint_plus.CheckpointerPlus()
  pop.add_reporter(checkpointer)
  
  winner = pop.run(eval_genomes)

  with open('winner', 'wb') as f:
    pickle.dump(winner, f)

  print(winner)

if __name__ == "__main__":
  if (not os.path.isfile('winner')):
    run()
