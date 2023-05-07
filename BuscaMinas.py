from math import *
import tkinter as tk
import random as ran

#Codificacion de problema
# B = Bomba ; 1-8 = Numero de bombas ; '-' = Vacío

def Ubicacion( t, n):
    # j de arriba abajo // i de izquierda derecha
    j = floor( (n)/8 )
    i = n-(8*j)
    return j, i

AMARILLO = "#FFED00"
AZUL = "#0047AB"
ROSADO = "#FF80D5"
BLANCO = "#FFFFFF"
GRIS = "#AAD2D5"
GRIS_MUERTO = "#809D9F"


class Juego:
    def __init__(self):
        self.pantalla= tk.Tk()
        self.pantalla.geometry("510x653")   #"ratio de error de pixel" es de 3
        self.pantalla.resizable(0,0)
        self.pantalla.title("-_-_-BUSCAMINAS-_-_-")
        self.pantalla.config(bg=AZUL, padx=28, pady=30)
        self.pantalla.grid_propagate( False )

        self.escenario = tk.Frame(self.pantalla, height=544, width=455, bg=AMARILLO)
        self.escenario.grid(row=2)
        self.escenario.grid_propagate( False )
        
        '''
        self.problema = [   ['-','1','-','-','-','-','-','-'], #Para debugear
                            ['-','1','-','1','-','-','-','-'],
                            ['-','1','1','-','1','-','-','-'],
                            ['-','1','1','-','-','1','-','-'],
                            ['-','1','1','1','1','1','-','-'],
                            ['-','1','1','-','-','1','1','-'],
                            ['-','1','-','-','-','1','1','-'],
                            ['-','1','-','-','-','-','1','-']   ]
        '''

        self.problema = self.Crear_Problema()
        self.celdaborrar = 0
        self.texto = tk.StringVar()
        self.Espacio_texto()
        self.Crear_Texto()
        self.lista_botones = self.Crear_Botones()



    def Crear_Texto(self):
        for j in range(8):
            for i in range(8):
                boton = tk.Label(self.escenario,  height=2, width=3, text=( self.problema[j][i] ),
                                    font=("Arial", 16, "bold"), borderwidth=5, bg=ROSADO )
                boton.grid( row=j, column=i, padx=3, pady=4 )


    def Crear_Botones(self):
        LisBotones = []
        ene = 0
        for j in range(8):
            for i in range(8):
                boton = tk.Button(self.escenario, height=8, width=10, 
                                   font=("Arial", 5, "bold"), borderwidth=5, bg= GRIS)

                boton.config( command = lambda x=ene: self.BorrarBoton(x) )
                boton.grid( row=j, column=i )
                LisBotones.append(boton)
                ene += 1

        return LisBotones


    def Espacio_texto(self):
        self.texto.set( "MINAS" )
        lab1 = tk.Label(self.pantalla, textvariable=self.texto, bg=BLANCO, width=50, justify='left', font=('Arial', 10, 'normal'))
        lab1.grid(row=0)
        lab1.grid_propagate(False)


    def Inp_rpta(self, n):
        rpta_j, rpta_i = Ubicacion(8, n)
        #print("nice", str(n))
        #print("Formado por -> " + str(rpta_j) + "y" + str(rpta_i))
        rpta = self.problema[ rpta_j ][ rpta_i ]

        # SI LO QUE PISA ES UN -
        if rpta == "-":
            
            guiones = [ n ]        #   El ultimo de la lista "desbloquear[-1]"
            a = 0
            while a < len(guiones):

                guion = guiones[a]
                rpta_j, rpta_i = Ubicacion(8, guion)

                if rpta_i == 0:
                    for i in check[3:]:
                        borrar = i + guion
                        if i != 0 and (borrar>=0 and borrar<=63):
                            self.lista_botones[borrar].grid_forget()
                            y,x = Ubicacion(8, borrar)
                            if self.problema[y][x] == "-" and (guiones.count( borrar ) == 0) and (i!=-7 and i!=9) :
                                guiones.append( borrar )

                elif rpta_i == 7:
                    for i in check[:6]:
                        borrar = i + guion
                        if i != 0 and (borrar>=0 and borrar<=63):
                            self.lista_botones[borrar].grid_forget()
                            y,x = Ubicacion(8, borrar)
                            if self.problema[y][x] == "-" and (guiones.count( borrar ) == 0) and (i!=7 and i!=-9):
                                guiones.append( borrar )

                else:
                    for i in check:
                        borrar = i + guion
                        if i != 0 and (borrar>=0 and borrar<=63):
                            self.lista_botones[borrar].grid_forget()
                            y,x = Ubicacion(8, borrar)
                            if self.problema[y][x] == "-" and (guiones.count( borrar ) == 0) and (i!=-7 and i!=-9 and i!=7 and i!=9):
                                guiones.append( borrar )

                a += 1


        # SI LO QUE PISA ES UNA MINA
        elif rpta == "B":       
            self.texto.set(" WN!!! PERDISTE ")
            for i in self.lista_botones:
                i.config( command = "", bg=GRIS_MUERTO ) #state= "disabled"
            


        # SI LO QUE PISA ES UN NÚMERO.... Nada xd


    def Crear_Problema(self):
        #        Generador de problema (Un problema 8x8 con 10 minas)
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

        global check
        check = [-9, 7, -1, -8, 0, 8, 1, -7, 9]
        contadorB = 0
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
        
        return problem


    #   Funciones aparte
    def BorrarBoton(self, boton):
        self.lista_botones[boton].grid_forget()
        self.celdaborrar = boton
        self.Inp_rpta( boton )
        #print( boton )
        #print( "Sí furufa" )


    def run(self):
        self.pantalla.mainloop()



juga = Juego()
juga.run()