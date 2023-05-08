import pyautogui
import pymsgbox
import sys
import webbrowser
from time import sleep

#Literalmente una copia del codigo de pyautogui.displayMousePosition()
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
        ubcX = x - xOffset
        ubcY = y - yOffset
        rC, gC, bC = pixelColor
        return ubcX, ubcY, rC, gC, bC


class Accionador:
    def __init__(self, tipoAccion, msg):
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

class Observador:
    def __init__(self, ubcX, ubcY, color1, color2, color3, accion):
        self.ubcX = ubcX
        self.ubcY = ubcY
        self.cR = color1
        self.cG = color2
        self.cB = color3
        self.accionador = accion

    def Observar(self):
        print("Aprieta Ctrl+c para detener el observador")
        try:
            while True:
                if pyautogui.pixelMatchesColor(self.ubcX, self.ubcY, (cR, cG, cB)) == True: #Lol supuestamente no deberia ser cR sino self.cR ???
                    print("Si todo bien")
                else:
                    self.accionador.Accionar()
                sleep(1)

        except KeyboardInterrupt:
            print("\nProgramaFinalizado")


if __name__=="__main__":
    print("Bienvenido Detector de Cambios DEMO")
    print(" Este codigo se dedicara a observar un punto en tu pantalla\n")
    print(" y te avisara cuando vea un cambio en el color del mismo")

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
    observer = Observador(ubcX, ubcY, cR, cG, cB, accionador)


    observer.Observar()