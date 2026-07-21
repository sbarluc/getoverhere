import math
import random
import os
os.environ['SDL_VIDEODRIVER'] = 'x11'  # o 'wayland'

import pygame
from models.objeto import Objeto

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
# JUGADOR (modificado para tener masa)
# ==========================================================

class Nave(Objeto):
    
    def __init__(self, controles={"avanzar":pygame.K_w, "retroceder":pygame.K_s, "girar_cw":pygame.K_e, "girar_acw":pygame.K_q}):
        super().__init__(random.randint(0,ANCHO), random.randint(0,ALTO), 1000, 15, tipo="Nave")

        self.controles = controles

        self.angulo = 0
        self.velocidad_angular = 0

        self.empuje_lineal = 200
        self.velocidad_maxima = 500
        
        self.aceleracion_angular = 250
        self.velocidad_angular_maxima = 300
        self.amortiguamiento_angular = 1.0
        
        self.masa = -100000
        
        self.estela = []

    def cambiar_controles(self, controles):
        self.controles = controles

    def actualizar(self, dt, teclas):

        # Propulsión angular
        if teclas[self.controles["girar_acw"]]:
            self.velocidad_angular += self.aceleracion_angular * dt
        
        if teclas[self.controles["girar_cw"]]:
            self.velocidad_angular -= self.aceleracion_angular * dt
        
        self.velocidad_angular *= self.amortiguamiento_angular
        
        if self.velocidad_angular > self.velocidad_angular_maxima:
            self.velocidad_angular = self.velocidad_angular_maxima
        elif self.velocidad_angular < -self.velocidad_angular_maxima:
            self.velocidad_angular = -self.velocidad_angular_maxima
        
        self.angulo += self.velocidad_angular * dt
        
        # Propulsión lineal
        esta_propulsando = False
        
        if teclas[self.controles["avanzar"]]:
            radianes = math.radians(self.angulo)
            ax = math.cos(radianes) * self.empuje_lineal
            ay = -math.sin(radianes) * self.empuje_lineal
            self.vx += ax * dt
            self.vy += ay * dt
            esta_propulsando = True

        if teclas[self.controles["retroceder"]]:
            radianes = math.radians(self.angulo)
            ax = math.cos(radianes) * self.empuje_lineal
            ay = -math.sin(radianes) * self.empuje_lineal
            self.vx -= ax * dt
            self.vy -= ay * dt
            esta_propulsando = True
        
        # Límite de velocidad lineal
        rapidez = math.sqrt(self.vx**2 + self.vy**2)
        if rapidez > self.velocidad_maxima:
            self.vx = (self.vx / rapidez) * self.velocidad_maxima
            self.vy = (self.vy / rapidez) * self.velocidad_maxima
        
        # Movimiento
        self.x += self.vx * dt
        self.y += self.vy * dt
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

        # Bordes
        if self.x - self.radio < 0:
            self.x = self.radio
            self.vx = -self.vx * 0.8  # Pérdida de energía en el rebote
        elif self.x + self.radio > ANCHO:
            self.x = ANCHO - self.radio
            self.vx = -self.vx * 0.8
            
        if self.y - self.radio < 0:
            self.y = self.radio
            self.vy = -self.vy * 0.8
        elif self.y + self.radio > ALTO:
            self.y = ALTO - self.radio
            self.vy = -self.vy * 0.8
    
    def dibujar(self, pantalla):
        # Estela
        if len(self.estela) > 2:
            for i in range(len(self.estela) - 1):
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
        
        pygame.draw.polygon(
            pantalla,
            COLOR_JUGADOR,
            [punta, izquierda, derecha],
        )

class Asteroide(Objeto):

    def __init__(self, x, y, masa, radio):
        super().__init__(x, y, masa, radio, tipo="Asteroide")
    
    def dibujar(self, pantalla):
        pygame.draw.circle(
            pantalla,
            self.color,
            (int(self.x), int(self.y)),
            self.radio
        )

# ==========================================================
# ESTRELLAS
# ==========================================================

def generar_estrellas(cantidad):

    estrellas = []
    for _ in range(cantidad):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        radio = random.randint(1, 2)
        brillo = random.randint(33, 150)
        rand_1 = random.randint(0,255)
        color = (rand_1, max(0 ,rand_1 - 50), 0)
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
    pygame.display.set_caption("Get Over Here - Gravedad")
    reloj = pygame.time.Clock()
    
    estrellas = generar_estrellas(50)

    alpha_1 = Nave()
    beta_1 = Nave()

    beta_1.cambiar_controles({
        "avanzar": pygame.K_i,
        "retroceder": pygame.K_k,
        "girar_cw": pygame.K_o,
        "girar_acw": pygame.K_u
    })
    
    objetos = []
    for _ in range(20):
        x=random.randint(0, ANCHO)
        y=random.randint(0, ALTO)
        obj = Asteroide(x, y, 100, 4)
        obj.color = (
            random.randint(50, 155),
            random.randint(200, 250),
            random.randint(25, 155)
        )
        objetos.append(obj)
    
    ejecutando = True
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("Cerrando ventana...")
                ejecutando = False
            # Tecla R para reiniciar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    for obj in objetos:
                        obj.x = random.randint(0, ANCHO)
                        obj.y = random.randint(0, ALTO)
                        obj.vx = random.uniform(-30, 30)
                        obj.vy = random.uniform(-30, 30)
        
        teclas = pygame.key.get_pressed()
        
        alpha_1.actualizar(dt, teclas)
        beta_1.actualizar(dt, teclas)
        
        for obj in objetos:
            if not obj.tipo == "AgujeroNegro": 
                obj.aplicar_gravedad(dt, [alpha_1, beta_1]+objetos)
        
        pantalla.fill(COLOR_FONDO)
        dibujar_estrellas(pantalla, estrellas)
        
        for obj in objetos:
            obj.dibujar(pantalla)
        
        alpha_1.dibujar(pantalla)
        beta_1.dibujar(pantalla)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()