#para probar que tan bueno es

from tip import fis_tip
from My_tip import fis_tip as tip_fis


def prueba_fis(params):
   # service = [0.1, 1, 3, 5, 6, 7, 7.8, 8, 9, 9.33, 9.5, 10]
   # food = [1, 3, 4, 5, 6, 7, 7.8, 8, 9, 9.33, 9.5, 10]
    service = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
    food = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
    errores = []
    for s in service:
        for f in food:
            my_tip= tip_fis(s, f, params)
            tip1 = fis_tip(s, f)
            errores.append((tip1-my_tip)**2)  # aqui muestra el error
    return (sum(errores)/len(errores))**.5,   #suma los error cuadratico medio

if __name__ == '__main__':
    #print(prueba_fis([9,4,6,8]))
    #print(prueba_fis([5,2,5,5]))
    #print(prueba_fis([5.000214963054668, 1.744337694131901, 4.998567906201472, 5.000027113644392]))
    print(prueba_fis([5.000214963054668, 1.6202882970029848, 4.998567906201472, 4.998978112017097]))