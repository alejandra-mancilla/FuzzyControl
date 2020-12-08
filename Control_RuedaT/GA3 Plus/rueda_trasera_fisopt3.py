from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from ruta_curvas import CubicSplinePath, Pi_2_pi
import math
from My_FIS_optimo import fis_opt
#from My_Fis_5FMFijo import fis_opt

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
def control_rueda_trasera(v, yaw0, e, k, yaw_ref, params):
    #calcular el error
    error_teta = Pi_2_pi(yaw0 - yaw_ref)
    #omega = v * k * math.cos(error_teta) / (1.0-k*e) - KTH * abs(v) * error_teta- KE * v * math.sin(error_teta) / error_teta * e

    # sustituir la formula con el fis sin optimizar
    # mandas el error teta y aerror

    ## llamar al fis optimizado
    omega = fis_opt(error_teta, e, params=params)
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
def simulacion(ruta, meta_objetivo, params):
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
        error_flag=False

        # hacer el control de acuerdo al angulo y error

        # di = metodo de control
        # aceleracion
        # control_rueda_trasera = feedback por la retroaliemntacion que da
        e, k, yaw_ref, s0 = ruta.calc_track_error(x0, y0, s0)
        if abs(e)>100:
            #pass
            error_flag = True
            break
        error.append(e)

        try:
            di = control_rueda_trasera(v0, yaw0, e, k, yaw_ref,params)
        except :
            error_flag = True
            break

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

    return x, y, yaw, v, goal_flag, i, error, error_flag

def prueba_simulador(params, grafica=False):
    # puntos para definir la ruta m
    #ax = [0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0]
    #ay = [0.0, 0.0,  5.0, 6.5, 3.0, 5.0, -2.0]
    # puntos para definir la ruta A
    #ax = [0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0]
    #ay = [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]
    # puntos para definir la ruta s
    #ax = [0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0]
    #ay = [0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]
    #print(params)

    lista_rutas=[[[0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0], [0.0, 0.0,  5.0, 6.5, 3.0, 5.0, -2.0]]]

              #  [[0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0],[0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]],
             #   [[0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0],[0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]]]
    suma_error=0
    for ax, ay in lista_rutas:

        error_ruta =  rutas(ax, ay, params, grafica)

        suma_error += error_ruta[0]

    fit_ruta = suma_error/float(len(lista_rutas))
    return fit_ruta,




def rutas(ax, ay, params, grafica=False):  # metodo a llamar 3 veces
        ruta_referencia = CubicSplinePath(ax,ay)
        meta_objetivo = [ax[-1], ay[-1]]
        x, y, yaw, v, goal_flag, i, error, error_flag = simulacion(ruta_referencia, meta_objetivo, params)

        #assert goal_flag
        #spline = np.arange(0, ruta_referencia.length, 0.1)
        #t = np.linspace(0, 50, 501)
        #t= t[:i+2]
        #yaw_pi = map(Pi_2_pi,yaw)
        if error_flag:
            print("Bad Controller")
            return 5000,
        if not goal_flag:
            print("no llego")
            return 2000,
        # error_rmse = sum([i**2 for i in error])/len(error)**.5
        # print(error_rmse)
        # return error_rmse,

        #plt.plot(ax,ay, "xb", label="Input")
        #plt.plot(-1,1, "*b",label = "punto")
        #valor_s=ruta_referencia.__find_nearest_point(.1, -1, 1)
        #grafica=True
        if grafica:

            spline = np.arange(0, ruta_referencia.length, 0.1)
            t = np.linspace(0, 50, 501)
            t= t[:i+2]
            yaw_pi = map(Pi_2_pi,yaw)

            plt.subplots(1)
            plt.plot(ax, ay, "xb", label="Input")
            plt.plot(ruta_referencia.X(spline),ruta_referencia.Y(spline), "-r", label= "Ruta")
            plt.plot(x[:300], y[:300], "-g", label= "Seguimiento")
            plt.axis("equal")
            plt.grid(True)
            plt.xlabel("x (mts)")
            plt.ylabel("y (mts)")
            plt.legend()


            # plt.subplots(1)
            # plt.plot(t, np.rad2deg(list(yaw_pi)), "-r", label="yaw")
            # plt.grid(True)
            # plt.xlabel("tiempo (seg)")
            # plt.ylabel("theta (grados)")
            # plt.legend()
            #
            # plt.subplots(1)
            # plt.plot(spline, np.rad2deg(ruta_referencia.calc_yaw(spline)),"-r", label="yaw-Ruta Ref")
            # plt.grid(True)
            # plt.xlabel("line length (mts)")
            # plt.ylabel("yaw angle (grados)")
            # plt.legend()
            #
            # plt.subplots(1)
            # plt.plot(t, v, "-b", label="velocidad")
            # plt.grid(True)
            # plt.xlabel("tiempo (seg)")
            # plt.ylabel("velocidad (m/s)")
            # plt.legend()

            plt.show()
        error_rmse = sum([i ** 2 for i in error]) / len(error) ** .5
        print(error_rmse)
        return error_rmse,

if __name__ == '__main__':
    # ruta m

    #prueba_simulador([0.9054750552355649, 1.313749939916838, 1.2115608804558582, 1.0984015671585659],True)
    #prueba_simulador([0.5352509072211054, 0.8290705366152646, 0.4913977583475415, 0.5530603377966343], True)
    prueba_simulador(
        [0.35573812412349537, 0.14097144606903278, 0.47316964441604503, 0.23642073771498867, 0.5270759254382571,
         0.4394496478286478, 1.2364306914050767, -0.22083350225600715, 0.429290361499984]
, True)

    # ruta A
    #prueba_simulador([0.08088644788091975, 2.8483486172253603, 0.8885607474620291, 0.5418827997757919],True)
    # ruta s
    #prueba_simulador([6.726928936568646, 4.693242467303574, 5.552748248812912, 0.7633253589418352], True)
    #rutas([1.1146003785318166, 5.419685453162956, 1.8528160709129537, 3.1013579161149276], True)
    #prueba_simulador([0.41192781559444747, 7.764405748264, 0.7381872279193622, 0.8387152453671036],True)
    #prueba_simulador([3.824353739502582, 1.1507662981789863, 1.2050211027497757, 0.12306023229956276],True)
    #prueba_simulador([0.7129072353481256, 0.6950511269226142, 0.4050757896004107, 0.5196998000235793, 0.59708268324291787, 0.48749702495492913, 0.3155646574417933, 0.4239541979859553],True)
    #prueba_simulador([0.699229139753049, 0.4694223323379423, 0.45265565822337295, 0.7055835655386178, 0.7892938318573711, 0.9128506262286898, 0.12208385398422117, 0.0027819470367980575],True)