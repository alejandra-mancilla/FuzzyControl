#ruta de splines cubicos
import numpy as np
from scipy import interpolate
from scipy import optimize
import math
import  matplotlib.pyplot as plt



class CubicSplinePath:
    def __init__(self, x, y):
        x, y = map(np.asarray, (x, y))
        s = np.append([0], (np.cumsum(np.diff(x) ** 2) + np.cumsum(np.diff(y) ** 2)) ** 0.5)

        self.X = interpolate.CubicSpline(s, x)
        self.Y = interpolate.CubicSpline(s, y)

        self.dX = self.X.derivative(1)
        self.ddX = self.X.derivative(2)

        self.dY = self.Y.derivative(1)
        self.ddY = self.Y.derivative(2)

        self.length = s[-1]

    def calc_yaw(self, s):
        # Ref Theta
        dx, dy = self.dX(s), self.dY(s)
        return np.arctan2(dy, dx)

    def calc_curvature(self, s):
        # K(s) La curvatura de S en s
        dx, dy = self.dX(s), self.dY(s)
        ddx, ddy = self.ddX(s), self.ddY(s)
        return (ddy * dx - ddx * dy) / ((dx ** 2 + dy ** 2) ** (3 / 2))

    def __find_nearest_point(self, s0, x, y):

        def calc_distance(_s, *args):
            # Se busca un parámetro gamma para S(t) el cual
            # minimize la distancia
            # s(t) = argmin/g  (xr(t), yr(t)) - (xref(g),yref (g))
            # s0 es el punto de inicio de la búsqueda
            # _s son las opciones que se prueban po fmin_cg
            _x, _y = self.X(_s), self.Y(_s)
            return (_x - args[0]) ** 2 + (_y - args[1]) ** 2


        def calc_distance_jacobian(_s, *args):
            # gradiente del error para encontrar gamma
            _x, _y = self.X(_s), self.Y(_s)
            _dx, _dy = self.dX(_s), self.dY(_s)
            return 2 * _dx * (_x - args[0]) + 2 * _dy * (_y - args[1])

        minimum = optimize.fmin_cg(calc_distance, s0, calc_distance_jacobian, args=(x, y), full_output=True, disp=False)
        return minimum

    def calc_track_error(self, x, y, s0):
        ret = self.__find_nearest_point(s0, x, y)

        s = ret[0][0] # punto gamma en la ruta con distancia más corta
        e = ret[1]    # distancia minima

        k = self.calc_curvature(s)
        yaw = self.calc_yaw(s) # ref

        dxl = self.X(s) - x
        dyl = self.Y(s) - y
        angle = Pi_2_pi(yaw - math.atan2(dyl, dxl))
        if angle < 0:
            e *= -1
        # No se usan, solo e, Theta, k, s
        return e, k, yaw, s


def Pi_2_pi(angle):
    while(angle > math.pi):
        angle= angle - 2.0 * math.pi
    while(angle < -math.pi):
        angle=angle + 2.0 * math.pi
    return angle


