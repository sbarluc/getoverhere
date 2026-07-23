import pygame
import math

ANCHO = 1280
ALTO = 720

FUERZA_ANTIWARP = 7000
GRAVEDAD = 2  # Constante gravitacional (ajustable)
DISTANCIA_MINIMA = 50  # Distancia mínima para evitar singularidades

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
        self.estela = []
        
    def actualizar_posicion(self, dt, pantalla):
        """Actualiza la posición del objeto y maneja colisiones con bordes"""
        ancho_pantalla, alto_pantalla = pantalla.get_size()

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Rebotes en bordes
        if self.x - self.radio < 0:
            self.x = self.radio
            self.vx *= -0.8
        elif self.x + self.radio > ancho_pantalla:
            self.x = ancho_pantalla - self.radio
            self.vx *= -0.8

        if self.y - self.radio < 0:
            self.y = self.radio
            self.vy *= -0.8
        elif self.y + self.radio > alto_pantalla:
            self.y = alto_pantalla - self.radio
            self.vy *= -0.8

    def aplicar_gravedad(self, dt, objetos):
        """Aplica gravedad normal entre objetos"""
        for obj in objetos:
            if obj is self:
                continue

            dx = self.x - obj.x
            dy = self.y - obj.y

            distancia = math.sqrt(dx**2 + dy**2)

            if distancia < DISTANCIA_MINIMA:
                distancia = DISTANCIA_MINIMA

            aceleracion = (GRAVEDAD * self.masa) / (distancia**2)

            ax = aceleracion * (dx / distancia)
            ay = aceleracion * (dy / distancia)

            obj.vx += ax * dt
            obj.vy += ay * dt


    def detectar_colision(self, otro):
        """Detecta si hay colisión entre dos objetos circulares"""
        dx = self.x - otro.x
        dy = self.y - otro.y
        distancia = math.sqrt(dx**2 + dy**2)
        return distancia < (self.radio + otro.radio)
    
    def resolver_colision(self, otro, dt):
        """Resuelve la colisión elástica entre dos objetos"""
        # Vector entre los centros
        dx = otro.x - self.x
        dy = otro.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        
        if distancia == 0:
            return
        
        # Vector normal
        nx = dx / distancia
        ny = dy / distancia
        
        # Separar los objetos para evitar solapamiento
        sobreposicion = (self.radio + otro.radio) - distancia
        if sobreposicion > 0:
            # Masa total
            masa_total = self.masa + otro.masa
            if masa_total == 0:
                return
            
            # Separar proporcionalmente a la masa
            self.x -= nx * sobreposicion * (otro.masa / masa_total)
            self.y -= ny * sobreposicion * (otro.masa / masa_total)
            otro.x += nx * sobreposicion * (self.masa / masa_total)
            otro.y += ny * sobreposicion * (self.masa / masa_total)
        
        # Velocidades relativas
        dvx = otro.vx - self.vx
        dvy = otro.vy - self.vy
        
        # Velocidad relativa en la dirección normal
        dvn = dvx * nx + dvy * ny
        
        # Solo si se están acercando
        if dvn > 0:
            return
        
        # Coeficiente de restitución (0 = perfectamente inelástico, 1 = perfectamente elástico)
        e = 0.8
        
        # Impulso (considerando masas)
        masa_total = self.masa + otro.masa
        if masa_total == 0:
            return
        
        impulso = -(1 + e) * dvn / masa_total
        
        # Aplicar impulso
        self.vx -= impulso * otro.masa * nx
        self.vy -= impulso * otro.masa * ny
        otro.vx += impulso * self.masa * nx
        otro.vy += impulso * self.masa * ny

    def colisionar_con_objeto(self, otro, dt):
        """Maneja la colisión con otro objeto"""
        if self.detectar_colision(otro):
            self.resolver_colision(otro, dt)
            return True
        return False


    def dibujar(self, pantalla):
        """Dibuja el objeto en pantalla"""
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)