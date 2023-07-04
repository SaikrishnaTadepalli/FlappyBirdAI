import pygame
import neat
import time
import os
import random

from Bird import Bird
from Pipe import Pipe
from Base import Base
from images import BACKGROUND_IMAGE

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 800

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)

current_generation = 0

def draw_window(win, bird, pipes, base, score):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)

    pygame.display.update()

def draw_window_neat(win, birds, pipes, base, score, generation):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    
    for bird in birds:
        bird.draw(win)
    
    text_score = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text_score, (WINDOW_WIDTH - 10 - text_score.get_width(), 10))

    text_generation = STAT_FONT.render("Gen: " + str(generation), 1, (255, 255, 255))
    win.blit(text_generation, (10, 10))

    base.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]

    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    clock = pygame.time.Clock()

    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False

        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if (pipe.collide(bird)):
                pass

            if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe)

            if (not pipe.passed and pipe.x < bird.x):
                pipe.passed = True
                add_pipe = True

            pipe.move()
            
        if (add_pipe):
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)
        
        if (bird.y + bird.image.get_height() > 730):
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()

# main()

def eval_genome(genomes, config):
    global current_generation
    current_generation += 1

    networks = []
    genome = []
    birds = []

    for _, g in genomes:
        network = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(network)
        birds.append(Bird(230, 350))
        g.fitness = 0
        genome.append(g)

    base = Base(730)
    pipes = [Pipe(700)]

    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    clock = pygame.time.Clock()

    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if (len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                pipe_index = 1
        else:
            run = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            genome[i].fitness += 0.1

            output = networks[i].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom))) 

            if (output[0] > 0.5):
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if (pipe.collide(bird)):
                    genome[i].fitness -= 1
                    birds.pop(i)
                    networks.pop(i)
                    genome.pop(i)

                if (not pipe.passed and pipe.x < bird.x):
                    pipe.passed = True
                    add_pipe = True
            
            if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe)

            pipe.move()
            
        if (add_pipe):
            score += 1

            for g in genome:
                g.fitness += 5

            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height() >= 730) or bird.y < 0:
                birds.pop(i)
                networks.pop(i)
                genome.pop(i)

        base.move()
        draw_window_neat(win, birds, pipes, base, score, current_generation)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genome, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)