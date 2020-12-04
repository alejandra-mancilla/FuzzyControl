from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ruta_curvas import CubicSplinePath, Pi_2_pi
import math
from My_FIS import fis_tip

L= 2.9  # longitud del vehiculo en mts
KTH = 1.0   # constante de ajuste k2
KE = 0.3    # constanste k
Kp = 1

#hacer el modelo matematico de la moto que es lo que se va a controlar
def modelo(z, t, delta, aceleracion):
    x, y, teta, v = z
    dx_dt    = v * np.cos(teta)
    dy_dt    = v * np.sin(teta)
    dteta_dt = v / L * np.tan(delta)
    dv_dt    = aceleracion

    return [dx_dt, dy_dt,dteta_dt,dv_dt]

# este metodo lo reemplazaremos con el FIS para que nos regrese delta
def control_rueda_trasera(v, yaw0, e, k, yaw_ref):
    #calcular el error
    error_teta = Pi_2_pi(yaw0 - yaw_ref)
    #omega = v * k * math.cos(error_teta) / (1.0-k*e) - KTH * abs(v) * error_teta- KE * v * math.sin(error_teta) / error_teta * e

    # sustituir la formula con el fis sin optimizar
    # mandas el error teta y aerror


    omega = fis_tip(error_teta, e)
    # if error_teta > 0:
    #     omega*=-1

    #print("omega",omega, "error teta ", error_teta, "error ", e)

    if error_teta == 0.0 or omega == 0.0 or v == 0.0:
        return 0.0

    delta = math.atan2(L * omega / v, 1.0)
    return delta


def calc_target_speed(yaw, yaw_ref, direction):
    target_speed = 10 / 3

    dyaw = yaw_ref - yaw
    switch = math.pi / 4.0 <= dyaw < math.pi / 2.0

    if switch:
        direction *= -1
        return 0.0, direction

    if direction != 1:
        return -target_speed, direction

    return target_speed, direction

def pid_control(velocidad_objetivo, v):
    a = Kp * (velocidad_objetivo - v)
    return a


# definir el estado inicial
def simulacion(ruta, meta_objetivo):
    # posiciones iniciales
    x0 = 0.0
    y0 = 0.0
    yaw0 = 0.0
    v0 = 0.0
    s0 = 0

    x=[x0]
    y=[y0]
    yaw=[yaw0]
    v=[v0]
    direction =1
    z0 = x0, y0, yaw0, v0
    error=[]

    # defines un arreglo de los tiempos que vas a medir de 0-10 seg, y los partes en 100 pedazos
    # lo pones en 101 para que haga 100 pedazos
    t = np.linspace(1, 50,501)

    # haces un arreglo en numpy de unos en el tiempo
   # deltai = np.zeros(len(t))
  #  aceleracioni=np.zeros(len(t))

    # llena el arreglo con estos valores en el rango de las posiciones indicadas
   # deltai[1:9] = .5
   # deltai[10:30] = 1
   # deltai[31:40] = -1
   # deltai[41:60] = 1
    #deltai[61-100] = .4

    #aceleracioni[:10] = 2
  #  aceleracioni[11:30] = 2
   # aceleracioni[31:40] = 1
   # aceleracioni[41:50] = -1
  #  aceleracioni[71:100] = 2
    di=0
    aceleracion = 0


    for i in range(len(t)-1):
        # se inicializan por lo pronto el angulo y la aceleracion

        # esto se controlara con el metodo pid_control
        # para contolar la aceleracion
        #if i < 10:      # el 10 seria en el primer segundo
         #   aceleracion = 3    # dado en m
        #elif i > 11 and i < 30:
         #   aceleracion = 1.5
        #else:
         #   aceleracion =0

        #if i > 10 and i < 20:
         #   di = -.8  # dado en radianes, seria un cuarto de radian
        #else:
        #    di = 0.05
        # inputs(deltai[i], aceleracioni[i])

        goal_flag=False

        # hacer el control de acuerdo al angulo y error

        # di = metodo de control
        # aceleracion
        # control_rueda_trasera = feedback por la retroaliemntacion que da
        e, k, yaw_ref, s0 = ruta.calc_track_error(x0, y0, s0)
        error.append(e)
        di = control_rueda_trasera(v0, yaw0, e, k, yaw_ref)

        speed_ref, direction = calc_target_speed(yaw0, yaw_ref, direction)
        aceleracion = pid_control(speed_ref, v0)

        inputs = (di, aceleracion)

        # correr el modelo
        z=odeint(modelo, z0, [0,0.1], args=inputs)

        z0 = z[-1]
        x0, y0, yaw0, v0 = z0  #le asignas el ultimo valor de z que es donde estan los valores

        x.append(x0)
        y.append(y0)
        yaw.append(yaw0)
        v.append(v0)

        dx = x0 - meta_objetivo[0]
        dy = y0 - meta_objetivo[1]

        if math.hypot(dx,dy) <= 0.3:
            print("META")
            goal_flag = True
            break

    return x, y, yaw, v, goal_flag, i, error


# puntos para definir la ruta m
ax = [0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0]
ay = [0.0, 0.0,  5.0, 6.5, 3.0, 5.0, -2.0]
# puntos para definir la ruta A
#ax = [0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0]
#ay = [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]
# puntos para definir la ruta s
#ax = [0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0]
#ay = [0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]

ruta_referencia = CubicSplinePath(ax,ay)
meta_objetivo = [ax[-1], ay[-1]]
x, y, yaw, v, goal_flag, i, error = simulacion(ruta_referencia, meta_objetivo)
#assert goal_flag
spline = np.arange(0, ruta_referencia.length, 0.1)
t = np.linspace(0, 50, 501)
t= t[:i+2]
yaw_pi = map(Pi_2_pi,yaw)

print(sum([i**2 for i in error])/len(error)**.5)

#plt.plot(ax,ay, "xb", label="Input")
#plt.plot(-1,1, "*b",label = "punto")
#valor_s=ruta_referencia.__find_nearest_point(.1, -1, 1)

plt.subplots(1)
plt.plot(ax, ay, "xb", label="Input")
plt.plot(ruta_referencia.X(spline),ruta_referencia.Y(spline), "-r", label= "Ruta ")
plt.plot(x, y, "-g", label= "Seguimiento")
plt.axis("equal")
plt.grid(True)
plt.xlabel("X(mts)")
plt.ylabel("Y(mts)")
plt.legend()


# plt.subplots(1)
# plt.plot(x, y, "-g", label="movimiento")
# plt.grid(True)
# plt.axis("equal")
# plt.xlabel("x (mts)")
# plt.ylabel("y(mts)")
# plt.legend()


plt.subplots(1)
plt.plot(t, np.rad2deg(list(yaw_pi)), "-r", label="yaw")
plt.grid(True)
plt.xlabel("tiempo (seg)")
plt.ylabel("theta (grados)")
plt.legend()

plt.subplots(1)
plt.plot(spline, np.rad2deg(ruta_referencia.calc_yaw(spline)),"-r", label="yaw-Ruta ref")
plt.grid(True)
plt.xlabel("line length (mts)")
plt.ylabel("yaw angle (grados)")
plt.legend()

plt.subplots(1)
plt.plot(t, v, "-b", label="velocidad")
plt.grid(True)
plt.xlabel("tiempo (seg)")
plt.ylabel("velocidad (m/s)")
plt.legend()

plt.show()
