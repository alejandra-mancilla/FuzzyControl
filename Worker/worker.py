import redis
import os
import time
from nuevoGA import main
import json
r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)

redis_ready = False

# intenta hasta que este listo el contenedor
while not redis_ready:
    try:
        redis_ready = r.ping()
    except:
        print("waiting for redis")
        time.sleep(3)

print("setup: redis alive")

while True:

    _, config_json = r.brpop('cola_de_mensajes') #esta configurado en json
    if config_json:
        mensaje_python = json.loads(config_json)
        print("poblacion recibida... ")
        pob_evolucionada = main(mensaje_python)

        convierteAmensaje = json.dumps(pob_evolucionada).encode('utf-8')
        r.lpush('cola_evolucionada', convierteAmensaje)
        print("poblacion enviada... ",pob_evolucionada['Best_fitness'])
       # print(str(config['hof']))

