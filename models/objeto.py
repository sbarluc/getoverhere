import random
import math

ANCHO = 1280
ALTO = 720

GRAVEDAD = 200  # Constante gravitacional (ajustable)
DISTANCIA_MINIMA = 10  # Distancia mínima para evitar singularidades

class Objeto:
    
    def __init__(self, x, y, masa, radio, tipo=None):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.masa = masa
        self.radio = radio
        self.color = (200, 100, 50)
        self.tipo = tipo

        estela = []
        
    def aplicar_gravedad(self, dt, cuerpos):
        ax = 0
        ay = 0
        
        for cuerpo in cuerpos:
            dx = cuerpo.x - self.x
            dy = cuerpo.y - self.y
            distancia = math.sqrt(dx**2 + dy**2)
            
            if distancia < DISTANCIA_MINIMA:
                distancia = DISTANCIA_MINIMA
            
            fuerza = GRAVEDAD * cuerpo.masa / (distancia ** 2)
            
            # Componentes de la aceleración
            ax += fuerza * (dx / distancia)
            ay += fuerza * (dy / distancia)
        
        # Aplicamos la aceleración
        self.vx += ax * dt
        self.vy += ay * dt
        
        # Movimiento
        self.x += self.vx * dt
        self.y += self.vy * dt

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
        pass