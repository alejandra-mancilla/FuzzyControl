
import random
from prueba_tip import prueba_fis
import time
import json  # formato de texto universal

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_float", random.uniform, 1, 9)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 4)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", prueba_fis)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma= 0.2, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)


def main(config):
    #empezar a contar el tiempo
    inicio_tiempo=time.time()  # te asigna el tiempo actual
    #random.seed(64)
    best = None

    #  Crea la pop  si no se encuentra en la configuracion
    if 'pop' not in config:
        # si no esta la etiqueta en el diccionario se crea en el diccionario
        # en este caso se crea con objetos de DEAP
        config['pop'] = toolbox.population(n=config['pop_size'])
    else:
        pop=[]   # crea una lista nueva
        # de ind tipo flotante pop=[[1.2,1.7,1.3,2.4],[1.2,1.7,1.3,2.4],[1.2,1.7,1.3,2.4],[1.2,1.7,1.3,2.4]]
        # porque se definio individuos de 4 elementos cromosoma
        # si se quiere accesar elementos se crea una lista de  diccionarios
        # pop = [{'individuo': [1.2,1.7,1.3,2.4], 'score': 1.23}, {,},{,}] etc
        # y se accesa a los elementos print([pop[0]['score'])
        # print (pop[0]['índividuo'])
        # o crear un diccionario de diccionarios y accesar con sus subindices
        #pop = [[  ],1.23],[[2,1,2],2.3]]
        #print(pop[0][0]
        #otra forma seria
        for ind_dict in config['pop']:     # recorre la lista y lo pone en ind
            # es un constructor que crea individuos de deap que son compatibles
            nuevo = creator.Individual(ind_dict['individuo'])
            pop.append(nuevo)   # y los agrega a la lista

        config['pop'] = pop[:]   # renombra la poblacion para usar el mismo nombre mas adelante

          #Calcular fitness
    fitnesses = map(toolbox.evaluate,config['pop']) # se evalua toda la poblacion

    tot_num_ev= len(config['pop'])
    #Asignar fitness a cada individuo

    for ind, fit in  zip(config['pop'],fitnesses):
        ind.fitness.values = fit

    #crear una lista para guardar los fitness de todas las generaciones
    #lista_fitness=[]
    #lista_gen=[]
    #lista_eval=[]
    # se hace mejor un una lista para guardar todos los datos anteriores
    estadistica_gen=[]

    for gen in range(config['ngen']):
        # decendencia

        offspring = toolbox.select(config['pop'], len(config['pop']))
        offspring = list(map(toolbox.clone, offspring))

        #cruce
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability cxpb
            if random.random() < config['cxpb']:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
        #mutacion
        for mutant in offspring:
            # mutate an individual with probability mutpb
            if random.random() < config['mutpb']:
                toolbox.mutate(mutant)
                del mutant.fitness.values


        #actualiza poblacion, son los ind que se les borro el fitness porque muto 

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # copia  la nueva
        config['pop'][:] = offspring

        #imprime estadistica
        num_ev_gen = len(invalid_ind)
        tot_num_ev = tot_num_ev + num_ev_gen
         #  ordenar los fitness
        fits = [ind.fitness.values[0] for ind in config['pop']]

        # imprimir los fitnes de cada generacion
     #   print(fits)  # lista de todos los fitness
      #  print(min(fits),tools.selBest(config['pop'], 1))

        # guardas las listas
        #lista_eval.append(num_ev_gen)
        #lista_fitness.append(min(fits))
        #lista_gen.append(gen+1)
        # aqui se guarda en la lista todos los append
       #generacion por generacion
        estadistica_gen.append([num_ev_gen,min(fits)])

        # se quitan las graficas no se ocuparan por el momento
    # hacer mas de dos graficas en una pasada
    # plt.figure()
    # #subplot (dos reng 1 colum y numero de figura)
    # # dos renglones porque en cada reng estara unas grafica
    # plt.subplot(2,1,1)
    # # hacer las graficas del fitness y generaciones
    # plt.plot(lista_gen,lista_fitness)
    # plt.xlabel('Número de Generación')
    # plt.ylabel('Raiz del Error cuadrático medio')
    #
    # plt.subplot(2,1,2)
    # plt.plot(lista_gen, lista_eval,'r*')
    # plt.xlabel('Número de Generación')
    # plt.ylabel('Número de Evaluaciones')  # por Generación)
    # plt.show()

    #print('gen:', gen,  "tot_num_ev:", tot_num_ev,"best_fitness:",min(fits), tools.selBest(config['pop'], 1),'mut',config['mutpb'],sep=',')
   # print('{},{},{:.16f},{},{},"{}"'.format(gen, tot_num_ev, min(fits), config['cxpb'], config['mutpb'], tools.selBest(config['pop'], 1)))
   # print(time.time()-inicio_tiempo,'segundos')
    #agregando al diccionario conf para regresarla toda

    #crear un diccionario para cambiar los individuos deap a formato
    pop_regreso=[]
    for individuo in config['pop']:
        # esto para que cada ind muestre su fitnes caundo lo imprima
        nuevo = {'individuo': individuo, 'score': individuo.fitness.values[0]}
        pop_regreso.append(nuevo)



    config['Tiempo_Total']=time.time()-inicio_tiempo
    config['Total_num_eval']=tot_num_ev
    config['Best_fitness']=min(fits)
    config['Best_solution']=tools.selBest(config['pop'], 1)
    config['Estadistica_gen']=estadistica_gen

    #ya que saco las estadisticas anteriores cambia la poblacion
    config['pop'] = pop_regreso
    return config


if __name__ == "__main__":
    #for mut in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    #   for cru in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    # cuando se use worker se leer de la cola la sig linea
    config = {'pop_size': 40,'cxpb':0.7, 'mutpb':0.3, 'ngen':20}
    config = main(config) # corre el algortimo

    print(config['Total_num_eval']/config['Tiempo_Total'], config['Tiempo_Total'],config['Total_num_eval'],config['Best_fitness'], config['Best_solution'][0])
    # esto no se ejecuta aqui solo es para probar
    #es lo que se guardo en la cola
    # para usarlo en redis se debe guardar como texto
    # entonces se cambia el formato a json
    # ordena de forma descendente
    #config['pop'].sort(key=lambda i : i['score'], reverse=True)
    # imprimes los mejores dos por ejemplo
    #print(config['pop'][:2])

    #for ind in config['pop']:
    #    print(ind)



    #mensaje=json.dumps(config).encode('utf-8')
    #print(mensaje) # estos son los datos que guardarias en redis
    # para leer el mensaje, se convierte de json a python en otro programa
    # redis.pop
    #mensaje_python = json.loads(mensaje)
    # simula que lo toma otro worker de la cola de mensajes

    #config = main(config)
    #print(config)
