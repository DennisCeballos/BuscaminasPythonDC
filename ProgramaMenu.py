'''
REQUERIMIENTOS IMPORTANTES PARA EJECUTAR ESTE CODIGO

pip install pyautogui
pip install Pillow

'''

import pyautogui
import pymsgbox
import sys
import webbrowser
from time import sleep

#CONSTANTES
DIR_ARCHIVO =  "noBorrar.txt"

#Literalmente una copia del codigo de pyautogui.displayMousePosition(), pero adaptado a mis necesidades
def pedirAyudita(xOffset=0, yOffset=0):
    """This function is meant to be run from the command line. It will
    automatically display the location and RGB of the mouse cursor."""
    try:
        runningIDLE = sys.stdin.__module__.startswith("idlelib")
    except:
        runningIDLE = False

    print("Press Ctrl-C to quit.")
    if xOffset != 0 or yOffset != 0:
        print("xOffset: %s yOffset: %s" % (xOffset, yOffset))
    try:
        while True:
            # Get and print the mouse coordinates.
            x, y = pyautogui.position()
            positionStr = "X: " + str(x - xOffset).rjust(4) + " Y: " + str(y - yOffset).rjust(4)
            if not pyautogui.onScreen(x - xOffset, y - yOffset) or sys.platform == "darwin":
                # Pixel color can only be found for the primary monitor, and also not on mac due to the screenshot having the mouse cursor in the way.
                pixelColor = ("NaN", "NaN", "NaN")
            else:
                pixelColor = pyautogui.screenshot().getpixel(
                    (x, y)
                )  # NOTE: On Windows & Linux, getpixel() returns a 3-integer tuple, but on macOS it returns a 4-integer tuple.
            positionStr += " / RGB: (" + str(pixelColor[0]).rjust(3)
            positionStr += ", " + str(pixelColor[1]).rjust(3)
            positionStr += ", " + str(pixelColor[2]).rjust(3) + ")"
            sys.stdout.write(positionStr)
            if not runningIDLE:
                # If this is a terminal, than we can erase the text by printing \b backspaces.
                sys.stdout.write("\b" * len(positionStr))
            else:
                # If this isn't a terminal (i.e. IDLE) then we can only append more text. Print a newline instead and pause a second (so we don't send too much output).
                sys.stdout.write("\n")
                sleep(1)
            sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()
        #ubcX, ubcY, rC, gC, bC = pedirAyudita()
        rC, gC, bC = pixelColor
        return (x-xOffset), (y-yOffset), rC, gC, bC


class Accionador:
    def __init__(self, tipoAccion="a", msg="Default"):
        self.tipo = tipoAccion
        self.palabras = msg
        self.bandera = False #La bandera se pondra 1 cuando se ejecute la accion

    def Accionar(self):
        #Si ya se ejecuto una vez entonces
        if not self.bandera:

            self.bandera = True
            #De acuerdo al tipo es si mostrara un mensaje o un link
            if self.tipo=="a":
                pymsgbox.alert(text="Detector de cambios \n"+self.palabras, title="Detector de cambios", button='OK' )
            elif self.tipo=="b":
                webbrowser.open(url=self.palabras)

    #Funcion para guardar los datos de este ACCIONADOR en archivo
    def GuardarPredeterminado(self):
        try:
            #El esquema de guardado esta en moldePredeterminado.txt
            #Abrir el archivo en modo lectura
            archivo = open( DIR_ARCHIVO, "r")
            #Crear una lista copia de todo el txt file
            lista = archivo.readlines()

            #Cambia solo la info necesaria justo en laubicacion respectiva del file
            lista[1] = self.tipo + "\n"
            lista[2] = self.palabras + "\n"

            #Lo vuelve abrir, pero esta vez en modo escritura
            archivo = open( DIR_ARCHIVO, "w")
            #Reemplaza toda la info con los datos alterados
            archivo.writelines( lista )
            archivo.close()

            print("----- Se guardaron los siguientes datos ")
            print( "Un accionador que:")
            if (self.tipo=="a"):
                print(" > Mostrara un mensaje en pantalla con la frase: " + self.palabras)
            elif(self.tipo=="b"):
                print(" > Abrira un enlace en el navegador: " + self.palabras)

        except Exception as e:
            print("Hubo un error al guardar predeterminado en el Accionador")
            print(" > " + str(e))


class Observador:
    #Son ubcX,ubcY las coordenadas en la pantalla; color123 los valores RGB a observar; y accion una clase Accionador
    def __init__(self, ubcX: int, ubcY: int, color1: int, color2: int, color3: int, accionador:Accionador=None ):
        self.ubcX = ubcX
        self.ubcY = ubcY
        self.cR = color1
        self.cG = color2
        self.cB = color3
        self.accionador = accionador

    def setAccionador(self, accion: Accionador):
        self.accionador = accion

    #Bucle que se dedicara a observar el lugar ubcX-ubcY asegurandose que el color RGB(color123) este presente
    def Observar(self):
        print("Aprieta Ctrl+c para detener el observador")
        try:
            while True:
                if pyautogui.pixelMatchesColor(self.ubcX, self.ubcY, (self.cR, self.cG, self.cB)) == True:
                    print("Si todo bien")
                else:
                    self.accionador.Accionar()
                sleep(1)

        except KeyboardInterrupt:
            print("\nProgramaFinalizado")

    #Funcion para guardar los datos de este observador en archivo
    def GuardarPredeterminado(self):
        try:
            #El esquema de guardado esta en moldePredeterminado.txt
            #Abrir el archivo en modo lectura
            archivo = open( DIR_ARCHIVO, "r")
            #Crear una lista copia de todo el txt file
            lista = archivo.readlines()

            #Cambia solo la info necesaria justo en laubicacion respectiva del file
            lista[5] = str(self.ubcX) + "\n"
            lista[6] = str(self.ubcY) + "\n"
            lista[7] = str(self.cR) + "\n"
            lista[8] = str(self.cG) + "\n"
            lista[9] = str(self.cB) + "\n"

            #Lo vuelve abrir, pero esta vez en modo escritura
            archivo = open( DIR_ARCHIVO, "w")
            #Reemplaza toda la info con los datos alterados
            archivo.writelines( lista )

            print("----- Se guardaron los siguientes datos ")
            print( "Ubicacion:   " + str(self.ubcX) + "," + str(self.ubcY) )
            print( "Colores RGB: (" + str(self.cR) + ", " + str(self.cG) + ", " + str(self.cB) + ")" )

            archivo.close()

        except Exception as e:
            print("Hubo un error al guardar predeterminado en el Observador: ")
            print(" > " + str(e))

        

#Clase para poner COLORES en el cmd
# Template: print(f"{bcolors.RED}Warning{bcolors.RED}")
class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


#Muestra el Menu de Cambios
def MenuCambios():
    print("Lista de cambios guardados")
    
    print(f"|{bcolors.UNDERLINE} Nombre       {bcolors.END}", end="")
    print(f"{bcolors.UNDERLINE}| ColorInicial {bcolors.END}", end="")
    print(f"{bcolors.UNDERLINE}| ColorFinal   {bcolors.END}", end="")
    print(f"{bcolors.UNDERLINE}| Ubicacion    {bcolors.END}|")

    print("")
    print("")
    print("Opciones:")
    print("1. Crear      2. Editar     3. Eliminar")

#Muestra el Menu de Acciones
def MenuAcciones():
    print("Lista de Acciones guardadas")
    
    print(f"|{bcolors.UNDERLINE} Nombre       {bcolors.END}", end="")
    print(f"|{bcolors.UNDERLINE} Evento              _    {bcolors.END}|")

    print("")
    print("")
    print("Opciones:")
    print("1. Crear      2. Editar     3. Eliminar")

def pasosCrearObservador():
    #Desde aca se trabaja para el objeto Observador
    print("Deseeas ayuda para recopilar los datos?")
    print("a. Utilizar asistente de ubicacion")
    print("b. Ingresar datos manualmente")
    entrada = input()

    if entrada=="a":
        print("Observa un rato la pantalla y apunta tus datos")
        ubcX, ubcY, cR, cG, cB = pedirAyudita()
        #print("A ver si funciono ")
        #print(ubcX, ubcY, cR, cG, cB)

    elif entrada=="b":
        print("Primero ingresa a donde quieres que observe (separado el X e Y por un espacio)")
        ubcX, ubcY = input().split(" ")
        ubcX = int(ubcX)
        ubcY = int(ubcY)

        print("Que color debo esperar encontrar")
        cR,cG,cB = input().split()
        cR = int(cR)
        cG = int(cG)
        cB = int(cB)

    return Observador(ubcX, ubcY, cR, cG, cB)

def pasosCrearAccionador():
    print("Que tipo de accion deseas?")
    print("a. Mostrar mensaje en la pantalla")
    print("b. Abrir un link en el buscador")

    entrada = input()
    if entrada==("a"):
        print("Que mensaje quieres que se muestre?")
    elif entrada==("b"):
        print("Que link quieres que se abra?")

    palabra = input()

    #Se crea el objeto accionador con los datos ingresados
    return Accionador(entrada, palabra)



#Muestra el menu de inicio
def MenuInicio():
    print(f"{bcolors.CYAN}-_-_-_{bcolors.END}", end="")
    print(" DETECTOR DE CAMBIOS ", end="")
    print(f"{bcolors.CYAN}_-_-_-{bcolors.END}")

    print("    1. Inicio")
    print("    2. Inicio con Actuadores predeterminados")
    print("    3. Definir Observador predeterminado")
    print("    4. Definir Accionador predeterminado")
    print("    0. Salir")

    entrada = int(input())

    #En caso sea el inicio normal, ejecutar el programa de la forma mas basica
    if entrada==1:
        
        #Desde aca se trabaja para el objeto Observador
        print("Primero elige, deseeas ayuda para recopilar los datos?")
        print("a. Utilizar asistente de ubicacion")
        print("b. Ingresar datos manualmente")
        entrada = input()

        if entrada=="a":
            print("Observa un rato la pantalla y apunta tus datos")
            ubcX, ubcY, cR, cG, cB = pedirAyudita()
            #print("A ver si funciono ")
            #print(ubcX, ubcY, cR, cG, cB)

        elif entrada=="b":
            print("Primero ingresa a donde quieres que observe (separado el X e Y por un espacio)")
            ubcX, ubcY = input().split(" ")
            ubcX = int(ubcX)
            ubcY = int(ubcY)

            print("Que color debo esperar encontrar")
            cR,cG,cB = input().split()
            cR = int(cR)
            cG = int(cG)
            cB = int(cB)


        #Desde aqui se trabaja para el objeto Accionador
        print("Que tipo de accion deseas?")
        print("a. Mostrar mensaje en la pantalla")
        print("b. Abrir un link en el buscador")

        entrada = input()
        if entrada==("a"):
            print("Que mensaje quieres que se muestre?")
        elif entrada==("b"):
            print("Que link quieres que se abra?")

        palabra = input()


        #Se crea el objeto accionador con los datos ingresados
        accionador = Accionador(entrada, palabra)

        #Recien se puede crear al observador ya que necesita de un accionador
        observador = Observador(ubcX, ubcY, cR, cG, cB, accionador)

        observador.Observar()

    #Se ejecuta el programa con el observador y accionador que este en el archivo guardado
    elif entrada == 2:
        print("Ejecutando programa con los elementos predeterminados")
        
        #Abrir el archivo de texto y recopilar todos los datos en una lista
        archivo = open(DIR_ARCHIVO, "r")
        lista = archivo.readlines()

        #Alterar los datos de la lista para que no tengan el salto de linea al final
        for i in range( len(lista) ):
            lista[i] = lista[i].removesuffix("\n")


        #Crear los objetos necesarios con los datos de la lista
        #Cada creacion esta almacenada en un tryCatch para evitar posibles errores
        try:
            accionador = Accionador(tipoAccion = lista[1],
                                    msg = lista[2])
        except Exception as e:
            print("Hubo un error en la lectura de los datos para el Accionador: " + "\n " + str(e))    

        try:
            observador = Observador(ubcX = int(lista[5]),
                                    ubcY = int(lista[6]),
                                    color1 = int(lista[7]),
                                    color2 = int(lista[8]),
                                    color3 = int(lista[9]),
                                    accionador = accionador)
        except Exception as e:
            print("Hubo un error en la lectura de los datos para el Observador: " + "\n " + str(e))

        observador.Observar()

    #Caso se meta a la seccion de crear un Observador predeterminado
    elif entrada == 3:
        observer = pasosCrearObservador()
        observer.GuardarPredeterminado()

    #Caso se meta a la seccion de crear un Accionador predeterminado
    elif entrada == 4:
        accioner = pasosCrearAccionador()
        accioner.GuardarPredeterminado()

    elif entrada == 5:
        print("Este es un secretito para el futuro")


#La funcion main
if __name__ == "__main__" :
    MenuInicio()


'''
LISTADO DE COSAS QUE FALTAN:

    Hacer infalible el guardado de archivos
        Que se cree el file en caso ne exista

    ORDENAR EL CODIGO
        ELIMINAR FUNCIONES INNECESARIAS EXTRA
        MEJORAR PARTE DE MENU PRINCIPAL

    
    Se vienen cositas:
     > Cambiar las opciones de trabajo del Observador (que quiza pueda ESPERAR A VER un color)
     > Tener un menu completo con acciones y observaciones
'''