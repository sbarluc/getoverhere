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

        self.x = random.random() * ANCHO
        self.y = random.random() * ALTO

        self.angulo = 0
        self.velocidad_angular = 0  # grados/segundo (velocidad actual)

        self.vx = 0
        self.vy = 0

        # Propulsión lineal
        self.empuje_lineal = 50           # píxeles/segundo²
        self.velocidad_maxima = 100        # límite de velocidad lineal
        
        # Propulsión angular
        self.aceleracion_angular = 200     # grados/segundo²
        self.velocidad_angular_maxima = 300  # grados/segundo (límite de velocidad angular)
        self.amortiguamiento_angular = 1.0   # sin fricción (1.0 = sin pérdida)

        self.radio = 15
        
        # Para el efecto de estela
        self.estela = []

    def actualizar(self, dt, teclas):

        # ------------------
        # Propulsión angular (rotación)
        # ------------------
        
        if teclas[pygame.K_q]:
            self.velocidad_angular += self.aceleracion_angular * dt
        
        if teclas[pygame.K_e]:
            self.velocidad_angular -= self.aceleracion_angular * dt
        
        self.velocidad_angular *= self.amortiguamiento_angular
        
        # Límite de velocidad angular
        if self.velocidad_angular > self.velocidad_angular_maxima:
            self.velocidad_angular = self.velocidad_angular_maxima
        elif self.velocidad_angular < -self.velocidad_angular_maxima:
            self.velocidad_angular = -self.velocidad_angular_maxima
        
        self.angulo += self.velocidad_angular * dt

        # ------------------
        # Propulsión lineal
        # ------------------
        
        esta_propulsando = False
        
        if teclas[pygame.K_w]:

            radianes = math.radians(self.angulo)

            ax = math.cos(radianes) * self.empuje_lineal
            ay = -math.sin(radianes) * self.empuje_lineal

            self.vx += ax * dt
            self.vy += ay * dt

            esta_propulsando = True

        # ------------------
        # Límite de velocidad lineal
        # ------------------
        
        rapidez = math.sqrt(self.vx**2 + self.vy**2)
        if rapidez > self.velocidad_maxima:
            self.vx = (self.vx / rapidez) * self.velocidad_maxima
            self.vy = (self.vy / rapidez) * self.velocidad_maxima

        # ------------------
        # Movimiento
        # ------------------

        self.x += self.vx * dt
        self.y += self.vy * dt
        # Bordes
        self.x = self.x % ANCHO
        self.y = self.y % ALTO

        # Efecto de estela
        if esta_propulsando:
            self.estela.append((self.x, self.y))
            if len(self.estela) > 20:
                self.estela.pop(0)
        else:
            if self.estela: 
                self.estela.pop(0)
        

    def dibujar(self, pantalla):

        # Estela
        if len(self.estela) > 2:
            for i in range(len(self.estela) - 1):
                # Dibujar círculos simples para la estela
                pygame.draw.circle(
                    pantalla,
                    (250, 50, 70),
                    (int(self.estela[i][0]), int(self.estela[i][1])),
                    1
                )

        radianes = math.radians(self.angulo)
        punta = (
            self.x + math.cos(radianes) * 10,
            self.y - math.sin(radianes) * 10
        )
        izquierda = (
            self.x + math.cos(radianes + 2.4) * 7.5,
            self.y - math.sin(radianes + 2.4) * 7.5
        )
        derecha = (
            self.x + math.cos(radianes - 2.4) * 7.5,
            self.y - math.sin(radianes - 2.4) * 7.5
        )

        # Efecto de llama
        if self.estela and len(self.estela) > 1:
            # Dibujar llama en la parte trasera de la nave
            efecto_llama = (
                self.x - math.cos(radianes) * (1 + random.randint(5, 60)),
                self.y + math.sin(radianes) * (1 + random.randint(5, 60))
            )
            pygame.draw.circle(
                pantalla,
                (250, 150, 70),
                (int(efecto_llama[0]), int(efecto_llama[1])),
                random.randint(0,5)
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

        radio = random.randint(1, 4)
        brillo = random.randint(33, 150)
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