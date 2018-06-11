from __future__ import print_function

import gzip
import pickle
import random
import time

import neat
from neat.reporting import BaseReporter


class CheckpointerPlus(BaseReporter):
    def __init__(self):
        self.current_generation = None       
        self.species = None   
        self.population = None
        self.config = None 

    def start_generation(self, generation):
        self.current_generation = generation

    def end_generation(self, config, population, species):     
        self.species = species
        self.population = population
        self.config = config

    def save_checkpoint(self, pop = None, best_genome = None, stats = None, filename = 'checkpoint'):
        if self.population is None:
          population = pop.population   
          config = pop.config
          species = pop.species                 
        else:
          population = self.population
          config = self.config
          species = self.species
        if best_genome is None:
          best_genome = population.best_genome
          
        generation = self.current_generation
       
        """ Save the current simulation state. """
        print("Saving checkpoint to: " + filename)

        with gzip.open(filename, 'w', compresslevel=5) as f:
            data = (generation, config, population, species, random.getstate(), best_genome, stats)
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def restore_checkpoint(filename):
        '''Resumes the simulation from a previous saved point.'''
        with gzip.open(filename) as f:
            generation, config, population, species, rndstate, best_genome, stats = pickle.load(f)
            random.setstate(rndstate)
            pop = neat.Population(config, (population, species, generation))
            pop.best_genome = best_genome
            return pop, stats
