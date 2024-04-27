# SnakeAI
A comprehensive Python toolkit for training, testing, and visualizing a NEAT-driven AI that plays the snake game. This repository includes scripts for running the game, configuring the NEAT algorithm, and visualizing training progress.

## Overview
This project uses the NeuroEvolution of Augmenting Topologies (NEAT) algorithm to train an AI capable of playing the Snake game. It features tools for training new models, testing pre-trained AIs, and visualizing the evolution process. The project uses Pygame for game visualization and matplotlib with graphviz for training visualization.
While the project is fully operational, it includes several areas for potential improvement, which are noted in the source code comments. 

## Getting Started
### Prerequisites
- Python 3.8 or higher
- Pygame
- NEAT-Python
- matplotlib
- graphviz
- pickle

### Installation
1. Download the content of this repository.
2. Install required packages: 
pip install pygame neat-python matplotlib graphviz

It is recomended to have all the files in the same folder to make sure the code will properly execute.

### Usage
Run the `AI.py` script and choose to train or test the AI based on the on-screen prompts.

## Configuration
The NEAT parameters can be customized in `config-feedforward.txt`. Adjust settings such as population size, mutation rates, and fitness thresholds to experiment with different evolutionary strategies. The settings used as a baseline in this project are:

- **fitness_criterion**: max
- **fitness_threshold**: 40

This means the script will continue running until an AI that can achieve a score of 40 points emerges. At this point, the training will automatically stop, the graphical results of the training will be displayed, and the trained AI will be saved in the folder from which the script is run.

For detailed information on each configuration option, read the online NEAT documentation available at [NEAT-python documentation](https://neat-python.readthedocs.io/en/latest/config_file.html).

## License
This project is licensed under the GPL v3 License - see the LICENSE file for details.

## Acknowledgements
- NEAT-Python team for the NEAT implementation.
- Pygame and matplotlib communities for their powerful libraries.
