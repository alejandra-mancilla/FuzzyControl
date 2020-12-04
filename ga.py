# hacer un GA para buscar los parametros

import random

import numpy
from prueba_tip import prueba_fis
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# minimizar el error por eso es neg en weigth
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# typecode es d por double?
creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator busca de 0 a 10
toolbox.register("attr_float", random.uniform,  1, 9)

# Structure initializers 4 es el largo del individuo que le estamos enviando
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 4)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


toolbox.register("evaluate", prueba_fis)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian, mu=2.0,sigma=0.2,indpb=0.2) # optimiza parametro de GA
toolbox.register("select", tools.selTournament, tournsize=4)


def main(conf):
    random.seed(64)

    if 'pop' not in conf:
        config['pop'] = toolbox.population(n=conf['pop_size'])

    conf['hof'] = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

#    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.6, mutpb=0.3, ngen=20, stats=stats, halloffame=hof, verbose=True)
    pop, log = algorithms.eaSimple(config['pop'], toolbox, cxpb=conf['cxpb'], mutpb=conf['mutpb'], ngen=conf['ngen'], stats=stats, halloffame=conf['hof'],
                                   verbose=True)
    return conf


if __name__ == "__main__":
    config = {'pop_size': 10, 'cxpb': 0.3, 'mutpb': 0.3, 'ngen': 5}
    config= main(config)

    for i in range(4):
        config = main(config)