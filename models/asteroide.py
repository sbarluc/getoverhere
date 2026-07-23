import pygame
import math
import random
from models.objeto import Objeto

class Asteroide(Objeto):
    """Asteroide con forma irregular"""
    
    def __init__(self, x, y, masa, radio):
        super().__init__(x, y, masa, radio, tipo="Asteroide")
        self.vertices = self._generar_vertices()
        self.rotacion = random.uniform(0, 2 * math.pi)
        self.velocidad_rotacion = random.uniform(-1, 1)
        self.color = (180, 140, 100)
        
    def _generar_vertices(self):
        """Genera vértices para dar forma irregular al asteroide"""
        vertices = []
        num_vertices = random.randint(self.radio, 10)
        for i in range(num_vertices):
            angulo = (2 * math.pi * i) / num_vertices + random.uniform(-0.3, 0.3)
            radio = self.radio * random.uniform(0.7, 1.3)
            vertices.append((math.cos(angulo) * radio, math.sin(angulo) * radio))
        return vertices
    
    def dibujar(self, pantalla):
        """Dibuja el asteroide con forma irregular"""
        self.rotacion += self.velocidad_rotacion * 0.01
        
        puntos = []
        for vx, vy in self.vertices:
            # Rotar el punto
            rx = vx * math.cos(self.rotacion) - vy * math.sin(self.rotacion)
            ry = vx * math.sin(self.rotacion) + vy * math.cos(self.rotacion)
            puntos.append((int(self.x + rx), int(self.y + ry)))
        
        pygame.draw.polygon(pantalla, self.color, puntos, 2)
        pygame.draw.polygon(pantalla, self.color, puntos, 0)