import math
import random
import os
os.environ['SDL_VIDEODRIVER'] = 'x11'  # o 'wayland'

import pygame

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO = 1280
ALTO = 720
FPS = 60

COLOR_FONDO = (5, 5, 15)

COLOR_JUGADOR = (220, 220, 255)
COLOR_ESTELA = (100, 100, 255)


# ==========================================================
# JUGADOR
# ==========================================================

class Jugador:

    def __init__(self):

        self.x = ANCHO / 2
        self.y = ALTO / 2

        self.angulo = 0
        self.velocidad_angular = 0  # grados/segundo (velocidad actual)

        self.vx = 0
        self.vy = 0

        # Propulsión lineal
        self.empuje_lineal = 350           # píxeles/segundo²
        self.velocidad_maxima = 500        # límite de velocidad lineal
        
        # Propulsión angular
        self.aceleracion_angular = 360     # grados/segundo²
        self.velocidad_angular_maxima = 540  # grados/segundo (límite de velocidad angular)
        self.amortiguamiento_angular = 1.0   # sin fricción (1.0 = sin pérdida)

        self.radio = 15
        
        # Para el efecto de estela
        self.estela = []

    def actualizar(self, dt, teclas):

        # ------------------
        # Propulsión lineal
        # ------------------
        
        if teclas[pygame.K_w]:

            radianes = math.radians(self.angulo)

            ax = math.cos(radianes) * self.empuje_lineal
            ay = -math.sin(radianes) * self.empuje_lineal

            self.vx += ax * dt
            self.vy += ay * dt

        # ------------------
        # Movimiento
        # ------------------

        self.x += self.vx * dt
        self.y += self.vy * dt
        # Bordes
        self.x = self.x % ANCHO
        self.y = self.y % ALTO

        # ------------------
        # Límite de velocidad lineal
        # ------------------
        
        rapidez = math.sqrt(self.vx**2 + self.vy**2)
        if rapidez > self.velocidad_maxima:
            self.vx = (self.vx / rapidez) * self.velocidad_maxima
            self.vy = (self.vy / rapidez) * self.velocidad_maxima

        

    def dibujar(self, pantalla):

        radianes = math.radians(self.angulo)
        punta = (
            self.x + math.cos(radianes) * 20,
            self.y - math.sin(radianes) * 20
        )
        izquierda = (
            self.x + math.cos(radianes + 2.4) * 15,
            self.y - math.sin(radianes + 2.4) * 15
        )
        derecha = (
            self.x + math.cos(radianes - 2.4) * 15,
            self.y - math.sin(radianes - 2.4) * 15
        )

        pygame.draw.polygon(
            pantalla,
            COLOR_JUGADOR,
            [punta, izquierda, derecha],
        )


# ==========================================================
# ESTRELLAS
# ==========================================================

def generar_estrellas(cantidad):

    estrellas = []

    for _ in range(cantidad):

        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)

        radio = random.randint(3, 5)
        brillo = random.randint(33, 255)
        rand_1 = random.randint(0,255)
        color = (rand_1, random.randint(0,100), 255-rand_1 )

        estrellas.append((x, y, radio, brillo, color))

    return estrellas


def dibujar_estrellas(pantalla, estrellas):

    for x, y, radio, brillo, color in estrellas:

        pygame.draw.circle(
            pantalla,
            (min(255, brillo + color[0]), min(255, brillo + color[1]), min(255, brillo + color[2])),
            (x, y),
            radio,
        )


# ==========================================================
# PRINCIPAL
# ==========================================================

def main():

    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Get Over Here")
    reloj = pygame.time.Clock()
    jugador = Jugador()
    estrellas = generar_estrellas(50)
    ejecutando = True

    while ejecutando:
        dt = reloj.tick(FPS) / 1000

        # ------------------
        # Eventos
        # ------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("Cerrando ventana...")
                ejecutando = False

        teclas = pygame.key.get_pressed()

        # ------------------
        # Actualizar
        # ------------------

        jugador.actualizar(dt, teclas)

        # ------------------
        # Dibujar
        # ------------------

        pantalla.fill(COLOR_FONDO)
        dibujar_estrellas(pantalla, estrellas)
        jugador.dibujar(pantalla)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()