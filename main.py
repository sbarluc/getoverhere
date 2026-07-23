import math
import random

import pygame
from models.nave import Nave
from models.asteroide import Asteroide

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO = 1200
ALTO = 700
FPS = 60

COLOR_FONDO = (5, 5, 15)
COLOR_NAVE = (220, 220, 255)

# ==========================================================
# ESTRELLAS
# ==========================================================

def generar_estrellas(cantidad):
    """Genera un fondo de estrellas aleatorio"""
    estrellas = []
    for _ in range(cantidad):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        radio = random.randint(1, 2)
        brillo = random.randint(33, 150)
        rand_1 = random.randint(0, 255)
        color = (rand_1, max(0, rand_1 - 50), 0)
        estrellas.append((x, y, radio, brillo, color))
    return estrellas

def dibujar_estrellas(pantalla, estrellas):
    """Dibuja el fondo de estrellas"""
    for x, y, radio, brillo, color in estrellas:
        pygame.draw.circle(
            pantalla,
            (min(255, brillo + color[0]), min(255, brillo + color[1]), min(255, brillo + color[2])),
            (x, y),
            radio,
        )

# ==========================================================
# FUNCIONES DE DEBUG
# ==========================================================

def dibujar_info(pantalla, nave):
    """Dibuja información de debug en pantalla"""
    radianes_1 = math.radians(nave.angulo)
    fuente = pygame.font.SysFont("Mono", 20)
    
    # Información de la nave
    info_texto = [
        f"Ángulo: {math.trunc(nave.angulo)}°",
        f"Eje W: ({-math.sin(radianes_1):.2f}, {math.cos(radianes_1):.2f})",
        f"Velocidad: ({nave.vx:.1f}, {nave.vy:.1f})",
        f"Rapidez: {math.sqrt(nave.vx**2 + nave.vy**2):.1f}",
        f"Masa: {nave.masa}"
    ]
    
    for i, texto in enumerate(info_texto):
        superficie_texto = fuente.render(texto, True, (0, 255, 0))
        pantalla.blit(superficie_texto, (10, 10 + i * 25))


# ==========================================================
# COLISIONES
# ==========================================================

def manejar_colisiones(objetos, dt):
    """Maneja todas las colisiones entre objetos"""
    # Primero, detectar y resolver colisiones entre todos los objetos
    for i in range(len(objetos)):
        for j in range(i + 1, len(objetos)):
            obj1 = objetos[i]
            obj2 = objetos[j]
            obj1.colisionar_con_objeto(obj2, dt)


# ==========================================================
# PRINCIPAL
# ==========================================================

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Anti-Warp - Nave con campo vectorial")
    reloj = pygame.time.Clock()
    
    # Generar fondo de estrellas
    estrellas = generar_estrellas(50)

    # Crear nave principal
    nave_1 = Nave(x=ANCHO * (3/4), y=ALTO * (3/4))
    nave_1.masa += 50000

    # Crear segunda nave (opcional)
    nave_2 = Nave(x=ANCHO * (2/3), y=ALTO * (2/3))
    nave_2.cambiar_controles({
        "avanzar": pygame.K_i,
        "retroceder": pygame.K_k,
        "girar_cw": pygame.K_l,
        "girar_acw": pygame.K_j
    })
    nave_2.masa += 50000
    
    # Lista de objetos
    objetos = []
    objetos.append(nave_1)
    objetos.append(nave_2)


    # Generar asteroides
    random_vel = [
            (random.random()-0.5, random.random()-0.5),  
            (random.random()-0.5, random.random()-0.5),  
            (random.random()-0.5, random.random()-0.5),  
            (random.random()-0.5, random.random()-0.5),  
            (random.random()-0.5, random.random()-0.5),                
    ]
    for i in range(0):
        r_cumulo = 0.01
        extra_brillo = random.randint(0,50)
        if i < 35:
            spawn_x, spawn_y = 0.2, 0.2
            color_particula = (150+extra_brillo,150+extra_brillo,205+extra_brillo)
            masa = 4000
        elif i < 60:
            spawn_x, spawn_y = 0.9, 0.2
            color_particula = (0+extra_brillo,0+extra_brillo,205+extra_brillo)
            masa = 8000
        elif i < 70:
            spawn_x, spawn_y = 0.2, 0.9
            color_particula = (0+extra_brillo,75+extra_brillo,205+extra_brillo)
            masa = 100000
        elif i < 85:
            spawn_x, spawn_y = 0.9, 0.9
            color_particula = (100+extra_brillo,100+extra_brillo,20+extra_brillo)
            masa = 200000
        else:
            spawn_x, spawn_y = 0.5, 0.5
            color_particula = (200+extra_brillo,100+extra_brillo,0+extra_brillo)
            masa = 60000

        radianes = math.radians(random.randint(-180, 180))
        obj = Asteroide(
            spawn_x * ANCHO + r_cumulo * i * math.cos(radianes),
            spawn_y * ALTO + r_cumulo * i * math.sin(radianes),
            masa,
            3
        )
        obj.color = (color_particula)

        obj.vx += int(i/20)*10*random_vel[int(i/20)-1][0]
        obj.vy += int(i/20)*10*random_vel[int(i/20)-1][1]
        
        objetos.append(obj)
    
    ejecutando = True
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000
        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("Cerrando ventana...")
                ejecutando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Reiniciar
                    for obj in objetos:
                        obj.x = random.randint(0, ANCHO)
                        obj.y = random.randint(0, ALTO)
                        obj.vx = random.uniform(-30, 30)
                        obj.vy = random.uniform(-30, 30)
        
        teclas = pygame.key.get_pressed()
        
        # Actualizar nave
        nave_1.actualizar(dt, teclas, pantalla)
        nave_2.actualizar(dt, teclas, pantalla)
        
        # Aplicar efectos a los objetos
        for obj in objetos:
            obj.aplicar_gravedad(dt, objetos)
        
        # Actualizar posiciones
        for obj in objetos:
            obj.actualizar_posicion(dt, pantalla)
        
        manejar_colisiones(objetos, dt)

        # Dibujar
        pantalla.fill(COLOR_FONDO)
        dibujar_estrellas(pantalla, estrellas)
        
        # Dibujar todos los objetos
        for obj in objetos:
            obj.dibujar(pantalla)
        
        # Dibujar información de debug
        dibujar_info(pantalla, nave_1)
        
        # Dibujar vector hacia un objeto cercano (ejemplo)
        # if len(objetos) > 1:
        #     # Buscar el objeto más cercano para dibujar el vector
        #     objeto_cercano = None
        #     distancia_minima = float('inf')
        #     for obj in objetos:
        #         if obj is nave_1:
        #             continue
        #         dx = obj.x - nave_1.x
        #         dy = obj.y - nave_1.y
        #         distancia = math.sqrt(dx**2 + dy**2)
        #         if distancia < distancia_minima:
        #             distancia_minima = distancia
        #             objeto_cercano = obj
            
        #     if objeto_cercano:
        #         nave_1.dibujar_vector_hacia_objeto(pantalla, objeto_cercano)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()