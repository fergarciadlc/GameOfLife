import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla.
width, height = 700, 700
# Creacion de la pantalla.
screen = pygame.display.set_mode((height, width))

# Numero de celdas.
nxC, nyC = 35, 35

# Dimensiones de la celda.
dimCW = int(width / nxC)
dimCH = int(height / nyC)

# Estado de las celdas.
gameState = np.zeros((nxC, nyC))

# Color del fondo.
bg = 25, 25, 25
# Pintar el fondo.
screen.fill(bg)

pauseExect = True

while True:
    newgameState = np.copy(gameState)
    screen.fill(bg)
    # Retraso en la actualizacion de la pantalla.
    time.sleep(0.01)

    # Registro de eventos de teclado y mouse.
    ev = pygame.event.get()
    for event in ev:
        mouseClic = pygame.mouse.get_pressed()
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        if sum(mouseClic) > 0:
            if mouseClic[1]:
                pauseExect = not pauseExect
            else:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                newgameState[celX, celY] = not gameState[celX, celY]

    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExect:
                # Calcular las celdas vecinas.
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[x % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, y % nyC] + \
                          gameState[(x + 1) % nxC, y % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[x % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Regla 1: Una celula muerta con 3 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newgameState[x, y] = 1
                # Regla 2: Una celula viva con menos de 2 o más de 3 vecinas vivas, "muere".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newgameState[x, y] = 0

            # Creacion del poligono de cada celda a dibujar.
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]
            # Dibujar la celda para cada par x e y.
            if newgameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    # Actualizacion del estado del juego.
    gameState = np.copy(newgameState)
    # Actualizacion de la pantalla.
    pygame.display.flip()
