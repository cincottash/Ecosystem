# Ecosystem

A simple evolution simulator analgous to The Game of Life.

## Features

* Animals move in random direction for a random amount of time

* Animal's velocity is based off their size

* Their hunger level decreases according to their size.

* When below 50% hunger they will search out food.

* Animals move to food within their sight radius(grows lineraly with size value)

* Food restores a fixed amount of hunger

* If animal hasn't reproduced in a time T, isn't hungry and there exists another animal which also satisfies those requirenments, move towards that animal and reproduce.

* The offspring's size will be an average of the parents(affecting the other stats).

* Offspring have a chance to mutate, changing their size.

* Foxes will try and eat rabbits, if there is a fox within a rabbit's sight, the rabbit will prioritize fleeing (until the fox is no longer visible) over eating and fucking.

* If no foxes around a rabbit, the rabbit will prioritize eating over fucking.

* Rabbits eat grass and move towards nearest grass if hungry.

* Grass respawns in a linear fashion.

* If an animal's hunger, H, is maxHunger/2 < H <  maxHunger, it will have a gradient between red and blue.  Fully blue when 100% Hunger and fully red when 50% hunger or less.

* If an animals hunger drops below 0, it will bleed health.  It's color will also turn black.

* Health regens when not starving.

* Pressing enter at any time during the simulation will stop the simulation and print a graph of data(population/time & size/time)

## Prerequisites

A list of required libraries is located in requirments.txt and can be installed via Pip with ```pip install -r requirments.txt```

## Built With

* Python3

* [Pygame](https://www.pygame.org/news)

## Authors

* **[Shane Cincotta](https://github.com/cincottash)**

## Usage
```python3 main.py InitialRabbitPop InitialGrassPop InitialFoxPop```

## Known Issues

* Foxes currently don't work


## Acknowledgments

[The Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
John Horton Conway, 26 December 1937 - 11 April 2020

  