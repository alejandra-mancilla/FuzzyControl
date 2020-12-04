# hacer al que inicia el experimento y ver como avanza y mezclando poblaciones
import redis
import json
import time

def Generador_de_poblaciones(num_poblaciones = 5):
      # se van a ahacer 5 poblaciones iniciales
    poblaciones = []

    for i in range(num_poblaciones):
        configBasica = {'pop_size': 8,'cxpb': 0.7, 'mutpb': 0.3, 'ngen': 10}
        configBasica['id']=i
        #configBasica['cxpb']= 0.1 * i + 0.2
        #configBasica['mutpb'] = 0.3 + i * 0.1
        #configBasica['ngen']= random.randint(2,6)
        poblaciones.append(configBasica)
    return poblaciones


def Setup(num_poblaciones):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_ready = False
    # intenta hasta que este listo el contenedor
    while not redis_ready:
        try:
            redis_ready = r.ping()
        except:
            print("waiting for redis")
            time.sleep(3)

    #enviamos las 5 poblaciones, lo vamos a hacer varias veces (for)
    for poblacion in Generador_de_poblaciones(5):
        mensaje = json.dumps(poblacion).encode('utf-8')
        r.lpush('cola_de_mensajes', mensaje)

def Combina():
    inicio_tiempo = time.time()

    num_poblaciones_recibidas = 0
    poblaciones_recibidas = []
    num_total = 0
    total_evals = 0

    while True:

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        _, mensaje_poblacion = r.brpop('cola_evolucionada')

        if mensaje_poblacion:
            poblacion = json.loads(mensaje_poblacion)
            #print('Población recibida ... ')
            num_total+=1
            num_poblaciones_recibidas+=1
            poblaciones_recibidas.append(poblacion)
            total_evals+=poblacion['Total_num_eval']

            #imprimir los datos
            #print(poblacion['id'], poblacion['cxpb'], poblacion['mutpb'], poblacion['Best_fitness'],poblacion['Total_num_eval'])


            if num_total == 10:   # para salirse cuando llegue a 10 poblacioens
                #print('ya son 10 poblaciones recibidas ...')
                total_time= time.time()-inicio_tiempo
                print(total_evals/total_time, total_time, total_evals, poblacion['Best_fitness'])
                break

            if num_poblaciones_recibidas == 2:
                print('ya hay Dos poblaciones recibidas para migrar')
                print('pop1:', poblaciones_recibidas[0]['Best_fitness'])
                print('pop2:', poblaciones_recibidas[1]['Best_fitness'])

            # aqui se puede hacer la mezcla (suffle)
                mensajeA = poblaciones_recibidas[0]
                mensajeB = poblaciones_recibidas[1]

             # esta es otra manera de migrar mas elitista
                mensajeA['pop'].sort(key=lambda ind: ind['score'])
                mensajeB['pop'].sort(key=lambda ind: ind['score'])

                print(mensajeA['pop'][0:2]) # imprime los dos mejores porque estan ordenados
                print(mensajeB['pop'][0:2])

                # se hace el intercambio con los mejores de cada uno
               # los mejores dos se intercambian por los dos peores

                mensajeA['pop'] = mensajeA['pop'][:-2] + mensajeB['pop'][:2]
                mensajeB['pop'] = mensajeB['pop'][:-2] + mensajeA['pop'][:2]



             # esta es una manera de migrar
             #   mitad = len(mensajeA['pop'])//2  #sacas la long de la pop

              #  mensajeA['pop'] = mensajeA['pop'][mitad:] + mensajeB['pop'][:mitad]
               # mensajeB['pop'] = mensajeB['pop'][mitad:] + mensajeA['pop'][:mitad]

                mensaje1 = json.dumps(mensajeA).encode('utf-8')
                r.lpush('cola_de_mensajes', mensaje1)

                mensaje2 = json.dumps(mensajeB).encode('utf-8')
                r.lpush('cola_de_mensajes', mensaje2)

                num_poblaciones_recibidas = 0
                poblaciones_recibidas = []

Setup(5)
Combina()