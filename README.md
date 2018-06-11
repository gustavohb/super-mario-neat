## SuperMario-Neat ##



Super Mario World playing agent developed using [Retro Learning Environment](https://github.com/nadavbh12/Retro-Learning-Environment) library as a final project for the Machine Learning course at Universidade Federal do ABC.

![super_mario_gif]](https://user-images.githubusercontent.com/3193712/41251592-c25e7b58-6d90-11e8-9b45-1b59b8f80663.gif)

This agent uses Neuroevolution of Augmenting Topologies (NEAT) in order to evolve a Neural Network capable of playing the stage.

For install requirements:
```
pip install -r requirements.txt
```

* Run `evolve.py`. When it completes, it will have created `winner`, a pickled version of the most fit genome.

* Run `play.py`. It will load the most fit genome from `winner` and run it in a new simulation to show the behavior. (See a sample movie [here](https://www.youtube.com/watch?v=dL2Q6-G3MGg).)