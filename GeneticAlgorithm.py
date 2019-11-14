from basePlayer import BasePlayer
import itertools
from math import inf
from random import choice
import numpy as np
from generals import State
import pickle
from game import Board
from game import Controller
from generals import *

class GeneticAlgorithm():
    def __init__(self, pop_size, generations, parents_number, learnMatch_number, 
                 testMatch_number, elitism_num, mutation_num, mutation_prob):
        self.pop_size = pop_size
        self.generations = generations
        self.parents_number = parents_number
        self.learnMatch_number = learnMatch_number
        self.testMatch_number = testMatch_number
        self.mutation_num = mutation_num
        self.mutation_prob = mutation_prob
        self.elitism_num = elitism_num
        
    def makeInitialPopulation(self):
        population = []
        for _ in itertools.repeat(None, self.pop_size -1):
            population.append(np.random.uniform(low=0.0, high=1.0, size=3))
        population.append([0.2, 0.3, 0.9])
        return population


    def fitnessFunction(self, population, board_size):
        #mivan ha pop_size páratlan??
        ''' if self.pop_size % 2 == 0:
            game_number = self.pop_size / 2
        else:
            game_number = (self.pop_size - 1) / 2 '''
        game_number = self.pop_size
        fitness = []
        for i in range(int(game_number)):
            board = Board(board_size)
            cont = Controller(PlayerEnum.QLearningPlayer, PlayerEnum.Random, board)
            cont.player1.alpha = population[i][0]
            cont.player1.exp_rate = population[i][1]
            cont.player1.decay_gamma = population[i][2]
            for _ in itertools.repeat(None, self.learnMatch_number):
                cont.trainLoop()
            cont.player1.exp_rate = 0.01
            ''' cont.player2.alpha = population[i + 1][0]
            cont.player2.exp_rate = population[i + 1][1]
            cont.player2.decay_gamma = population[i + 1][2] '''
            player1Win = 0
            player2Win = 0
            draw = 0
            for _ in itertools.repeat(None, self.testMatch_number):
                winner = cont.trainLoop()
                if winner == cont.player1:
                    player1Win = player1Win + 1
                elif winner == cont.player2:
                    player2Win = player2Win + 1
                else:
                    draw = draw + 1
            fitness.append(player1Win-player2Win)
            ''' fitness.append(player2Win-player1Win) '''
        ''' if self.pop_size % 2 != 0:
            board = Board(board_size)
            cont = Controller(PlayerEnum.QLearningPlayer, PlayerEnum.QLearningPlayer, board)
            cont.player1.alpha = population[i][0]
            cont.player1.exp_rate = population[i][1]
            cont.player1.decay_gamma = population[i][2]
            cont.player2.alpha = population[i][0]
            cont.player2.exp_rate = population[i][1]
            cont.player2.decay_gamma = population[i][2]
            player1Win = 0
            player2Win = 0
            draw = 0
            for _ in itertools.repeat(None, self.match_number):
                winner = cont.trainLoop()
                if winner == cont.player1:
                    player1Win = player1Win + 1
                elif winner == cont.player2:
                    player2Win = player2Win + 1
                else:
                    draw = draw + 1
            fitness.append(player1Win-player2Win) '''
        return fitness

    def tournamentParents(self, fitness, population, K):
        parents = []
        for _ in itertools.repeat(None, self.parents_number):
            possible_parents = []
            for _ in itertools.repeat(None, K):
                possible_parents.append(np.random.randint(0, self.pop_size))
            for _ in itertools.repeat(None, possible_parents):
                idx = fitness.index(max(fitness))
            parents.append(population[idx])
        return parents

    def bestParents(self, fitness, population):
        parents = []
        for _ in itertools.repeat(None, self.parents_number):
            idx = fitness.index(max(fitness))
            parents.append(population[idx])
            fitness[idx] = -inf
        return parents

    def rouletteWheelParents(self, fitness, population):
        parents = []
        fix_points = np.random.uniform(low=0.0, high=np.sum(fitness), size=self.parents_number))
        sum_part = 0
        for i in range(self.pop_size)
            sum_part = sum_part + fitness[i]
            for j in range(len(fix_points))
                if fix_points[j] <= sum_part:
                    parents.append(population[i])
        return parents

    def selectParents(self, fitness, population, selection_mode):
        parents = []
        if selection_mode = 0:
            return self.rouletteWheelParents(fitness, population)
        elif selection_mode = 1:
            return self.tournamentParents(fitness, population, K=5)
        else:
            return self.bestParents(fitness, population)

    def crossover(self, parents): #lehetne, hogy sorban megyünk végig szűlőkön, lehetne, hogy random választunk szülőt, és nem lehet overlap, de most az van, hogy lehet overlap
        new_population = []
        for i in range(self.elitism_num):
            new_population.append(parents[i])
        while len(new_population) < self.pop_size:
            #new_parents = []
            #mi van, ha páratlan a parents_num
            print("hahaha")
            print(new_population)
            if self.parents_number % 2 == 0:
                dating_number = self.parents_number / 2
            else:
                dating_number = (self.parents_number - 1) / 2
            for _ in itertools.repeat(None, int(dating_number)):
                parent1idx = np.random.randint(0, self.parents_number)
                parent2idx = parent1idx
                while parent1idx == parent2idx:
                    parent2idx = np.random.randint(0, self.parents_number)
                pruning = np.random.randint(0, 3)
                newBorn1 = [0, 0, 0]
                newBorn2 = [0, 0, 0]
                for i in range(3):
                    if i < pruning:
                        newBorn1[i] = parents[parent1idx][i]
                        newBorn2[i] = parents[parent2idx][i]
                    else: 
                        newBorn2[i] = parents[parent1idx][i]
                        newBorn1[i] = parents[parent2idx][i]
                new_population.append(newBorn1)
                new_population.append(newBorn2)
        return new_population 
    
    def mutation(self, egyed):
        idx = np.random.randint(0, 3)
        egyed[idx] = np.random.random_sample()

    def training(self, start_population):
        population = start_population
        generation = 0
        for _ in itertools.repeat(None, self.generations):
            #calc fitness
            print("gen: " + str(generation))
            generation = generation + 1
            mutation = 0
            fitness = self.fitnessFunction(population, 3)
            #Selecting the best parents in the population for mating.
            parents = self.selectParents(fitness, population)
            # Generating next generation using crossover.
            new_population = self.crossover(parents)
            for _ in itertools.repeat(None, self.mutation_num):
                prob = np.random.randint(0, 101)
                if prob < self.mutation_prob:
                    mutation = mutation +1
                    idx = np.random.randint(0, self.pop_size)
                    #idx = np.random.randint(0, 3)
                    choosenOne = new_population[idx]
                    self.mutation(choosenOne)
            population = new_population
            print("mutation: "+ str(mutation))
        return population


ga = GeneticAlgorithm(16, 20, 6, 600, 3, 30)
print("start")
population = ga.makeInitialPopulation()
ga.training(population)
ga.fitnessFunction(population, 3)

