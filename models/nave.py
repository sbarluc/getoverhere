import pygame
import math
from models.objeto import Objeto

COLOR_NAVE = (220, 220, 255)

class Nave(Objeto):
    """Nave espacial controlable por el jugador"""
    
    def __init__(self, x=0, y=0):
        super().__init__(x, y, 100, 15, tipo="Nave")

        self.controles = {
            "avanzar": pygame.K_w, 
            "retroceder": pygame.K_s, 
            "girar_cw": pygame.K_d, 
            "girar_acw": pygame.K_a
        }

        self.angulo = 0
        self.velocidad_angular = 0

        self.empuje_lineal = 30
        self.velocidad_maxima = 180
        
        self.aceleracion_angular = 180
        self.velocidad_angular_maxima = 360
        self.amortiguamiento_angular = 1.0
        
        self.masa = 200  # Masa para efectos gravitatorios
        self.estela = []

    def cambiar_controles(self, controles):
        """Cambia las teclas de control de la nave"""
        self.controles = controles

    def actualizar(self, dt, teclas, pantalla):
        """Actualiza el estado de la nave basado en entrada del usuario"""
        self.angulo %= 360

        # Propulsión angular
        if teclas[self.controles["girar_acw"]]:
            self.velocidad_angular += self.aceleracion_angular * dt
        
        if teclas[self.controles["girar_cw"]]:
            self.velocidad_angular -= self.aceleracion_angular * dt
        
        # Amortiguamiento angular
        self.velocidad_angular *= self.amortiguamiento_angular
        
        # Límite de velocidad angular
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
        
        # Efecto de estela
        if esta_propulsando:
            self.estela.append((self.x, self.y))
            if len(self.estela) > 20:
                self.estela.pop(0)
        else:
            if self.estela: 
                self.estela.pop(0)

        self.actualizar_posicion(dt, pantalla)

    def dibujar_eje(self, pantalla):
        """Dibuja el eje W de la nave (para debug)"""
        longitud = 50
        
        radianes = math.radians(self.angulo)
        wx = math.cos(radianes)
        wy = -math.sin(radianes)
        
        p1x = self.x - wx * longitud
        p1y = self.y - wy * longitud
        p2x = self.x + wx * longitud
        p2y = self.y + wy * longitud
        
        pygame.draw.line(pantalla, (255, 255, 255), (p1x, p1y), (p2x, p2y), 2)
        
        # Dibujar la normal (perpendicular) para referencia
        nx = -wy
        ny = wx
        n1x = self.x - nx * 40
        n1y = self.y - ny * 40
        n2x = self.x + nx * 40
        n2y = self.y + ny * 40
        pygame.draw.line(pantalla, (100, 100, 100), (n1x, n1y), (n2x, n2y), 1)

    def dibujar_vector_hacia_objeto(self, pantalla, objeto, longitud=50):
        """Dibuja un vector desde la nave hacia un objeto (para debug)"""
        # Vector desde la nave hacia el objeto
        dx = objeto.x - self.x
        dy = objeto.y - self.y
        
        distancia = math.sqrt(dx**2 + dy**2)
        if distancia < 0.001:
            return
        
        # Vector unitario
        ux = dx / distancia
        uy = dy / distancia
        
        # Punto final del vector
        px = self.x + ux * longitud
        py = self.y + uy * longitud
        
        pygame.draw.line(pantalla, (255, 50, 0), (self.x, self.y), (px, py), 2)
        
        # Dibujar punta de flecha
        self._dibujar_punta_flecha(pantalla, self.x, self.y, px, py, (255, 50, 0))

    def _dibujar_punta_flecha(self, pantalla, x1, y1, x2, y2, color, tamaño=8):
        """Dibuja una punta de flecha en el punto (x2, y2)"""
        angulo = math.atan2(y2 - y1, x2 - x1)
        
        p1x = x2 - tamaño * math.cos(angulo - math.pi/6)
        p1y = y2 - tamaño * math.sin(angulo - math.pi/6)
        p2x = x2 - tamaño * math.cos(angulo + math.pi/6)
        p2y = y2 - tamaño * math.sin(angulo + math.pi/6)
        
        pygame.draw.polygon(pantalla, color, [(x2, y2), (p1x, p1y), (p2x, p2y)])

    def dibujar(self, pantalla):
        """Dibuja la nave con su estela y eje"""
        # Estela
        if len(self.estela) > 2:
            for i in range(len(self.estela) - 1):
                pygame.draw.circle(
                    pantalla,
                    (250, 50, 70),
                    (int(self.estela[i][0]), int(self.estela[i][1])),
                    1
                )
        
        # # Dibujar el eje W (opcional, comentar si no se quiere ver)
        # self.dibujar_eje(pantalla)
        
        # Triángulo de la nave
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
            COLOR_NAVE,
            [punta, izquierda, derecha],
        )