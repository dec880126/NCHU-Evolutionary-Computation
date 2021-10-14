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
from math import pi
from random import Random
from statistics import stdev


#EV1 Config class 
class EV1_Config:
    """
    EV1 configuration class
    """
    # class variables
    sectionName='EV1'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'minLimit': (float,True),
             'maxLimit': (float,True),
             'mutationProb': (float,True),
             'mutationStddev': (float,True)}
     
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EC_Engine section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing EV1 section in cfg file')
         
        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval=eccfg[opt]
 
                #verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))
                 
                #create attributes on the fly
                setattr(self,opt,optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self,opt,None)
     
    #string representation for class data    
    def __str__(self):
        return str(yaml.dump(self.__dict__,default_flow_style=False))


 #A trivial Individual class
class Individual:
    def __init__(self, x=0, fit=0) -> None:
        self.x=x
        self.fit=fit

    def __lt__(self, other) -> bool:
         return self.fit < other.fit


#Simple 1-D fitness function example
#        
def fitnessFunc(x):
    # −10 − (0.04")+ + 10 cos(0.040")
    # return 50.0 - x*x
    return -10 - (0.04 * x)**2 + 10*np.cos(0.04*pi*x)

maxvalList = []
avgvalList = []

#Print some useful stats to screen
def printStats(pop, gen):
    global sca
    global maxvalList, avgvalList

    print('Generation:',gen)

    avgval=0
    maxval=pop[0].fit
    for p in pop:
        avgval+=p.fit
        if p.fit > maxval:
            maxval=p.fit
        print(f"{p.x=}\t{p.fit=}")
        if 'sca' in globals():
            sca.remove()
        sca = plt.scatter(p.x, p.fit, lw=0, s=200, c='red', alpha=0.5)
        # plt.pause(0.1)
    
    maxvalList.append(maxval)
    avgvalList.append(avgval/len(pop))
    # print(f'Max fitness: {maxval}')
    # print(f'Avg fitness: {avgval/len(pop)}\n')

#EV1: The simplest EA ever!
#            
def ev1(cfg):
    # start random number generator
    prng=Random()
    prng.seed(cfg.randomSeed)
    
    #random initialization of population
    population=[]
    for i in range(cfg.populationSize):
        x=prng.uniform(cfg.minLimit,cfg.maxLimit)
        ind=Individual(x,fitnessFunc(x))
        population.append(ind)
        
    plt.ion()
    graph_length = int(100)
    plot_x = np.linspace(-graph_length, graph_length, graph_length*2)
    plt.plot(plot_x, fitnessFunc(plot_x))
    
    #print stats 
    printStats(population,0)
    stddevList = []
    stddevList.append(stdev([pop.fit for pop in population]))

    #evolution main loop
    for i in range(1, cfg.generationCount+1):
        parentGroup = []
        childGroup = []

        # replace 3 child in every generation
        for idx in range(3):
            # randomly select two parents
            parentGroup.append(prng.sample(population,2))
            # recombine using simple average
            childGroup.append((parentGroup[idx][0].x + parentGroup[idx][1].x)/2)
        
            #random mutation using normal distribution
            if prng.random() <= cfg.mutationProb:
                childGroup[idx]=prng.normalvariate(childGroup[idx], cfg.mutationStddev)
            
            #survivor selection: replace worst
            child=Individual(childGroup[idx],fitnessFunc(childGroup[idx]))
            
            population.sort()
            if child.fit > population[0].fit:
                population[0]=child

        stddevList.append(stdev([pop.fit for pop in population]))
        
        #print stats  
        printStats(population,i)
    
    plt.ioff()
    plt.show()

    plt.subplot(2, 2, 1)
    plt.plot([i for i in range(cfg.generationCount + 1)], maxvalList)
    plt.xlabel('Generation')
    plt.ylabel('Max Fitness')

    plt.subplot(2, 2, 2)
    plt.plot([i for i in range(cfg.generationCount + 1)], avgvalList)
    plt.xlabel('Generation')
    plt.ylabel('Avg Fitness')

    plt.subplot(2, 2, 3)
    plt.plot([i for i in range(cfg.generationCount + 1)], stddevList)
    plt.xlabel('Generation')
    plt.ylabel('Standard deviation of fitness')

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
        cfg=EV1_Config(options.inputFileName)
        
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
