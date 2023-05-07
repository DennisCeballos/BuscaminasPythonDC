#Generador de problemas prueba
from math import *
import random as ran

def Ubicacion( t, n):
    # j de arriba abajo // i de izquierda derecha
    j = floor( (n)/8 )
    i = n-(8*j)
    return j, i

def Generador_problema():
 #        Generador de problema (Un problema 8x8 con 10 minas)
    '''
    problem = [ ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'] ] Reemplazable con el sgt codigo
    ''' 
    problem = []
    for i in range(8):
        a = []
        for i in range(8):
            a.append('-')
        problem.append(a)

    # Primero poner las bombas
    for i in range(13):
        y, x = Ubicacion( 8, ran.randint(0,63) )
        problem[y][x] = "B"
    check = [-9,-1, 7, -8, 0, 8, -7, 1, 9]
    contadorB = 0

    for i in problem:
        print(i)
        print() 

    # Analizar cada punto para asignarle un numero
    for a in range(64):
        contadorB = 0
        y, x = Ubicacion(8, a)
        if problem[y][x] == "B":
            pass

        else:

            #Analizar los alrededores
            if x==0:
                for i in check[3:]:
                    y, x = Ubicacion(8, a+i)
                    if (a+i)>=0 and (a+i)<=63 and problem[y][x]=="B":
                        contadorB = contadorB + 1
            elif x==7:
                for i in check[:6]:
                    y, x = Ubicacion(8, a+i)
                    if (a+i)>=0 and (a+i)<=63 and problem[y][x]=="B":
                        contadorB = contadorB + 1
            else:
                for i in check:
                    y, x = Ubicacion(8, a+i)
                    if (a+i)>=0 and (a+i)<=63 and problem[y][x]=="B":
                        contadorB = contadorB + 1    
              
            #Asigna valor a la celda
            y, x = Ubicacion(8, a)
            if contadorB==0:
                problem[y][x] = str("-")  

            else:
                problem[y][x] = str(contadorB)

    print("---- Terminado proceso de poner numeros ----")
    

    #                   IMPRESIÓN DE PROBLEMA
    for i in problem:
        print(i)        

Generador_problema()