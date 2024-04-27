from __future__ import annotations
from typing import Tuple, List
import visualize
import pickle
import random
import pygame
import math
import neat
import sys
import os

print('------------------------------------')
print('                                    ')
print('Snake AI Trainer & Tester v.0.1')
print('                                    ')
print('------------------------------------')

print('Type 1 to train an AI with NEAT')
print('Type 2 test an already trained AI')
print('Type 3 to exit the script')
choice = input('What do you want to do? ')

# script input selection
try:
    if int(choice) not in [1, 2, 3]:
        print('The written value does not correspond to any of the script functions')
        close = input('Press any button to exit...')
        sys.exit()
except:
    print('?...')
    close = input('Press any button to exit...')
    sys.exit()

# screen width & height and block size
bg_width = 400
bg_height = 400
block_size = 20

# direction strings
left = "LEFT"
right = "RIGHT"
up = "UP"
down = "DOWN"

# colors (RGB)
bg_color = black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
green = (0, 128, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# pygame & font initialization
pygame.init()
window = pygame.display.set_mode((bg_width, bg_height))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Times New Roman', 20)
text_colour = pygame.Color('White')
fps = pygame.time.Clock()


class Snake:
    """This class represents a snake object. Every snake object consists of a head
        and its body.
        ===Attributes===
        hunger : snake hunger
        head: snake head
        color: snake color
        body: snake body
        direction: direction of head
        size: size of snake (head and body)
        """
    head: List[int, int]
    color: Tuple[int, int, int]
    body: List[List[int, int]]
    direction: str
    size: int
    hunger: int

    def __init__(self, color=green, hunger=200) -> None:
        self.head = [int(10 * block_size), int(5 * block_size)]
        self.color = color
        self.hunger = hunger
        self.body = [self.head, [9 * block_size, 5 * block_size]]
        self.direction = right
        self.size = 2

    def change_dir(self, direc: str) -> None:
        if self.direction != left and direc == right:
            self.direction = right
        elif self.direction != right and direc == left:
            self.direction = left
        elif self.direction != down and direc == up:
            self.direction = up
        elif self.direction != up and direc == down:
            self.direction = down

    def move(self) -> None:
        if self.direction == right:
            self.head[0] += block_size
        elif self.direction == left:
            self.head[0] -= block_size
        elif self.direction == up:
            self.head[1] -= block_size
        elif self.direction == down:
            self.head[1] += block_size
        self.body.insert(0, list(self.head))
        self.body.pop()
        if self.body[0] != self.head:
            self.head = self.body[0]

    def add_to_tail(self) -> None:
        new_part = [self.body[-1][0], self.body[-1][1]]
        self.body.append(new_part)
        self.size += 1

    def get_body(self) -> List[List[int, int]]:
        return self.body


class Food:
    """This class represents a food object. Each food object has an x
       and a y value, a color and a state.
       ===Attributes===
       x: x-coordinate of food object
       y: y-coordinate of food object
       color: color of food object
       state: whether food object is on screen or not
       position: x,y-coordinates pair of food object
       """
    x: int
    y: int
    color: Tuple[int, int, int]
    state: bool
    position: Tuple[int, int]

    def __init__(self, color=red) -> None:
        self.x = random.randint(0, bg_width // block_size - 1) * block_size
        self.y = random.randint(0, bg_height // block_size - 1) * block_size
        self.color = color
        self.state = True
        self.position = self.x, self.y

    def spawn(self) -> Tuple[int, int]:
        if self.state:
            return self.x, self.y
        else:
            self.state = True
            self.x = random.randint(0, bg_width // block_size - 1) * block_size
            self.y = random.randint(0, bg_height // block_size - 1) * block_size
            return self.x, self.y

    def update(self, state) -> None:
        self.state = state

    def get_cords(self):
        x = self.x
        y = self.y
        cords = [x, y]
        return cords


def check_collision(rect1, rect2):
    if rect1.x == rect2.x and rect1.y == rect2.y:
        return True
    else:
        return False


def collision_food(snake_: Snake, food_target_x: int, food_target_y: int) -> int:
    snake_rect = pygame.Rect(*snake_.head, block_size, block_size)
    food_rect = pygame.Rect(food_target_x, food_target_y, block_size,
                            block_size)
    if check_collision(snake_rect, food_rect):
        return 1
    return 0


def wall_collision(s: Snake) -> bool:
    if (s.head[0] < 0) or (s.head[0] > bg_width - block_size) or (s.head[1] < 0) \
            or (s.head[1] > bg_height - block_size):
        return True
    return False


def body_collision(s_: Snake) -> bool:
    head_rect = pygame.Rect(*s_.head, block_size, block_size)
    for cell in s_.body[2:]:
        cell_rect = pygame.Rect(cell[0], cell[1], block_size, block_size)
        if check_collision(head_rect, cell_rect):
            return True
    return False


def check_block(snake: Snake, block: list):
    body = snake.get_body()
    if block in body:
        return 1
    elif block[0] < 0 or block[0] == bg_width or block[1] < 0 or block[1] == bg_height:
        return 1
    return 0


def angle_to_apple(point_1, point_2):
    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]
    rads = math.atan2(-dy, dx)
    angle = math.degrees(rads)
    return angle


def senses(snake_: Snake, apple_: Food) -> list:
    # return distance from an obstacle
    # return angle to the food
    """
    This function is very simplistic, the snake is currently able to "see" only one block in front of him in each direction
    modifying it to include more depth would make the AIs perform much better
    """ 

    if snake_.direction == up:
        pos = snake_.head
        a_pos = apple_.get_cords()
        angle = 90 - angle_to_apple(pos, a_pos)
        if angle > 180:
            angle -= 2 * 180
        elif angle <= -180:
            angle += 2 * 180
        block_up = check_block(snake_, [pos[0], pos[1] - block_size])
        block_left = check_block(snake_, [pos[0] - block_size, pos[1]])
        block_right = check_block(snake_, [pos[0] + block_size, pos[1]])
        return [angle / 180, block_up, block_right, block_left]

    elif snake_.direction == right:
        pos = snake_.head
        a_pos = apple_.get_cords()
        angle = 0 - angle_to_apple(pos, a_pos)
        if angle > 180:
            angle -= 2 * 180
        elif angle <= -180:
            angle += 2 * 180
        block_up = check_block(snake_, [pos[0] + block_size, pos[1]])
        block_left = check_block(snake_, [pos[0], pos[1] - block_size])
        block_right = check_block(snake_, [pos[0], pos[1] + block_size])
        return [angle / 180, block_up, block_right, block_left]

    elif snake_.direction == left:
        pos = snake_.head
        a_pos = apple_.get_cords()
        angle = 180 - angle_to_apple(pos, a_pos)
        if angle > 180:
            angle -= 2 * 180
        elif angle <= -180:
            angle += 2 * 180
        block_up = check_block(snake_, [pos[0] - block_size, pos[1]])
        block_left = check_block(snake_, [pos[0], pos[1] + block_size])
        block_right = check_block(snake_, [pos[0], pos[1] - block_size])
        return [angle / 180, block_up, block_right, block_left]

    elif snake_.direction == down:
        pos = snake_.head
        a_pos = apple_.get_cords()
        angle = -90 - angle_to_apple(pos, a_pos)
        if angle > 180:
            angle -= 2 * 180
        elif angle <= -180:
            angle += 2 * 180
        block_up = check_block(snake_, [pos[0], pos[1] + block_size])
        block_left = check_block(snake_, [pos[0] + block_size, pos[1]])
        block_right = check_block(snake_, [pos[0] - block_size, pos[1]])
        return [angle / 180, block_up, block_right, block_left]


def eval_genomes(genomes, config):
    # variables
    running = True

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # snake object that uses that network to play
    nets = []
    snakes = []
    foods = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake())
        foods.append(Food())
        ge.append(genome)

    while running and len(snakes) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                break

        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            # give inputs to the net and determine the 'right' direction
            inputs = senses(snake, apple)
            outputs = nets[x].activate(inputs)

            max_value = max(outputs)
            max_index = outputs.index(max_value)

            if max_index == 0:
                pass

            if max_index == 1:
                if snake.direction == up:
                    snake.change_dir(right)
                elif snake.direction == down:
                    snake.change_dir(left)
                elif snake.direction == right:
                    snake.change_dir(down)
                elif snake.direction == left:
                    snake.change_dir(up)

            if max_index == 2:
                if snake.direction == up:
                    snake.change_dir(left)
                elif snake.direction == down:
                    snake.change_dir(right)
                elif snake.direction == right:
                    snake.change_dir(up)
                elif snake.direction == left:
                    snake.change_dir(down)

        # fill window and draw snake
        window.fill(black)
        for item in snakes[0].get_body():
            pygame.draw.rect(window, snakes[0].color, [item[0], item[1], block_size,
                                                       block_size])

        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            snake.move()
            snake.hunger -= 1

        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            if snake.hunger < 1:
                # death by starvation
                ge[x].fitness -= 2
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
                foods.pop(x)

        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            # check for collision with wall:
            collision_with_wall = wall_collision(snake)
            if collision_with_wall:
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
                foods.pop(x)

        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            # check for collision with body:
            collision_with_body = body_collision(snake)
            if collision_with_body:
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
                foods.pop(x)

        n = 0
        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            # check if food is still on screen and draw it
            apple_pos = apple.spawn()
            collision_ = collision_food(snake, *apple_pos)
            if collision_ == 1:
                ge[x].fitness += 1  # snake length uses as fitness function (not optimal)
                snake.add_to_tail()
                snake.hunger = 200
                apple.update(False)
            if n == 0:
                pygame.draw.rect(window, apple.color, [apple_pos[0], apple_pos[1],
                                                       block_size, block_size])
            n += 1

        # renders display
        pygame.display.flip()

        # time delay
        pygame.time.delay(60)
        fps.tick(30)


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play snakes.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 100 generations.
    winner = p.run(eval_genomes, 100)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()

    # Display the winning genome
    print('\nBest genome:\n{!s}'.format(winner))

    # Draw stats and NN structure
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.draw_net(config, winner, True)


def replay_genome(config_file, genome_path="winner.pkl"):
    # Load required NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Draw the NN structure
    visualize.draw_net(config, genome, True)

    # Call game with only the loaded genome
    eval_genomes(genomes, config)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    if int(choice) == 1:
        run(config_path)
    elif int(choice) == 2:
        try:
            replay_genome(config_path)
        except:
            print('There is no genome to test in the program directory or it has been renamed')
            print('If you renamed it change the name back to "winner.pkl" if you want the program to run correctly')
            close = input('Press Enter to exit...')
            sys.exit()
    elif int(choice) == 3: sys.exit()


