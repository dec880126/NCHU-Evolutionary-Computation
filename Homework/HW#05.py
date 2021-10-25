"""
 # Evolutionary Computation HW #04

 - Student ID: 7110064490
 - Name: Huang Sin-Cyuan(黃新荃)
 - Email: dec880126@icloud.com
"""
import optparse
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from math import pi, exp, sqrt
from random import Random, normalvariate
from statistics import stdev


#EV1 Config class 
class EV1_Config:
    """
    EV1 configuration class
    """
    # class variables
    sectionName='EV1'
    options={'populationSize': (int, True),
             'generationCount': (int, True),
             'randomSeed': (int, True),
             'minLimit': (float, True),
             'maxLimit': (float, True)}
     
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EC_Engine section
        infile = open(inFileName, 'r')
        ymlcfg = yaml.safe_load(infile)
        infile.close()
        eccfg = ymlcfg.get(self.sectionName,None)
        if eccfg is None:
            raise Exception('Missing EV1 section in cfg file')
         
        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval = eccfg[opt]
 
                #verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception(f'Parameter "{opt}" has wrong type')
                 
                #create attributes on the fly
                setattr(self,opt, optval)
            else:
                if self.options[opt][1]:
                    raise Exception(f'Missing mandatory parameter "{opt}"')
                else:
                    setattr(self, opt, None)
     
    #string representation for class data    
    def __str__(self):
        return str(yaml.dump(self.__dict__, default_flow_style=False))
 #A trivial Individual class


class Individual:
    minSigma=1e-100
    maxSigma=1
    tau = 1
    minLimit=None
    maxLimit=None
    prng=None

    def __init__(self, x = 0, fit = 0) -> None:
        self.DNA = {
            'x': x,
            'sigma': self.minSigma
        }
        self.fit = fit

    def __lt__(self, other) -> bool:
         return self.fit < other.fit

    def crossover(self, other):
        child = Individual()

        alpha = self.prng.random()
        for key in ('x', 'sigma'):
            child.DNA[key] = self.DNA[key]*alpha + other.DNA[key]*(1 - alpha)

        return child

    def mutate(self):
        # sigma's boundary rules
        if self.DNA['sigma'] < self.minSigma:
            self.DNA['sigma'] = self.minSigma
        if self.DNA['sigma'] > self.maxSigma:
            self.DNA['sigma'] = self.maxSigma
        print('='*50)
        print(f"sigma: {self.DNA['sigma']}")

        # sigma_prime mutate first
        # self.DNA['sigma'] = self.DNA['sigma'] * exp(self.tau * self.prng.normalvariate(0, 1))

        # then mutate x_prime
        # self.DNA['x'] = self.DNA['x'] + self.DNA['sigma']*prng.normalvariate(0, 1)
        self.DNA['x'] = self.DNA['x'] + (self.maxLimit - self.minLimit)*self.DNA['sigma']*self.prng.normalvariate(0, 1)

    def evaluateFitness(self):
        self.fit = fitnessFunc(self.DNA['x'])

#Simple 1-D fitness function example
#        
def fitnessFunc(x):
    return -10 - (0.04 * x)**2 + 10*np.cos(0.04*pi*x)

maxvalList = []
avgvalList = []

#Print some useful stats to screen
def printStats(pop, gen):
    global sca
    global maxvalList, avgvalList

    print(f'Generation: {gen}')

    avgval = 0
    maxval = pop[0].fit
    for p in pop:
        avgval += p.fit
        if p.fit > maxval:
            maxval = p.fit
        print(f"{p.DNA['x']=}\t{p.fit=}")
        if 'sca' in globals():
            sca.remove()
        plt.subplot(gs[0, :])
        plt.title(f'EC Training, now in gen {gen}')
        sca = plt.scatter(p.DNA['x'], p.fit, lw=0, s=200, c='red', alpha=0.5)
        plt.pause(0.01)
    
    maxvalList.append(maxval)
    avgvalList.append(avgval/len(pop))
    plt.subplot(gs[1, 0])
    plt.title('Max Fitness')
    plt.scatter(gen, maxval, s=50, c='blue')
    plt.xlabel('Generation')
    plt.ylabel('Max Fitness')

    plt.subplot(gs[1, 1])
    plt.title('Avg Fitness')
    plt.scatter(gen, avgval/len(pop), s=50, c='green')
    plt.xlabel('Generation')
    plt.ylabel('Avg Fitness')

    plt.subplot(gs[1, 2])
    plt.title('Standard deviation of fitness')
    plt.scatter(gen, stdev((p.fit for p in pop)), s=50, c='pink')
    plt.xlabel('Generation')
    plt.ylabel('Standard deviation of fitness')
    print(f'Max fitness: {maxval}')
    print(f'Avg fitness: {avgval/len(pop)}\n')

#EV1: The simplest EA ever!
#            
def ev1(cfg):
    # start random number generator
    prng = Random()
    prng.seed(cfg.randomSeed)
    Individual.prng=prng
    
    #random initialization of population
    population = []
    for i in range(cfg.populationSize):
        x = prng.uniform(cfg.minLimit, cfg.maxLimit)
        ind = Individual(x, fitnessFunc(x))
        population.append(ind)
    
    # Plotting
    plt.figure(figsize=(13, 8))
    plt.ion()
    global gs
    gs = gridspec.GridSpec(2, 3)  
    graph_length = int(100)
    plot_x = np.linspace(-graph_length, graph_length, graph_length*2)
    plt.subplot(gs[0, :])
    plt.title('EC Training')
    plt.plot(plot_x, fitnessFunc(plot_x))
    
    # Print stats 
    printStats(population, 0)
    stddevList = []
    stddevList.append(stdev((pop.fit for pop in population)))

    #evolution main loop
    for i in range(1, cfg.generationCount+1):
        parentGroup = []
        childGroup = []

        # replace 5 child in every generation
        for evolution in range(5):
            # randomly select two parents
            [parent_1, parent_2] = prng.sample(population, 2)

            # Crossover
            child = parent_1.crossover(parent_2)
            childGroup.append(child)
        
            # Mutate
            child.mutate()
            
            # Evaluate Fitness
            child.evaluateFitness()
            
            # Survivor Selection
            population.sort()
            if child.fit > population[0].fit:
                population[0] = child

        stddevList.append(stdev((pop.fit for pop in population)))
        
        #print stats  
        printStats(population,i)

    plt.ioff()
    plt.show()
        
        
#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)
        
        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")
        
        #Get EV1 config params
        cfg = EV1_Config(options.inputFileName)
        Individual.minLimit=cfg.minLimit
        Individual.maxLimit=cfg.maxLimit
        
        #print config params
        print(cfg)
                    
        #run EV1
        ev1(cfg)
        
        if not options.quietMode:                    
            print('EV1 Completed!')    
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()
