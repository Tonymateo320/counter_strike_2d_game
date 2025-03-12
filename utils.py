
import pygame
import random
from config import *

class Boton:
    """Clase para crear botones interactivos (Tony Mateo 23-eisn-2-044)"""
    def __init__(self, x, y, ancho, alto, texto, color, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.fuente = pygame.font.SysFont(None, 32)
        
    def dibujar(self, pantalla):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(pantalla, self.color_hover, self.rect)
        else:
            pygame.draw.rect(pantalla, self.color, self.rect)
        texto_renderizado = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        pantalla.blit(texto_renderizado, texto_rect)
        
    def es_clic(self, pos):
        return self.rect.collidepoint(pos)

def generar_obstaculos(nivel, sprite_manager, num_obstaculos=10):
    """Genera obstáculos aleatorios para el nivel con verificación estricta de superposición (Tony Mateo 23-eisn-2-044)"""
    import pygame 
    import random
    from config import ANCHO, ALTO, DEBUG_MODE
    # Importación local para evitar referencia circular
    from game_objects import Obstaculo
    
    obstaculos = []
    
    #  Crear obstáculos en los bordes (barreras) (Tony Mateo 23-eisn-2-044)
    grosor_pared = 20
    
    # Pared superior
    obstaculos.append(Obstaculo(0, 0, ANCHO, grosor_pared, sprite_manager))
    
    # Pared inferior
    obstaculos.append(Obstaculo(0, ALTO-grosor_pared, ANCHO, grosor_pared, sprite_manager))
    
    # Pared izquierda
    obstaculos.append(Obstaculo(0, 0, grosor_pared, ALTO, sprite_manager))
    
    # Pared derecha
    obstaculos.append(Obstaculo(ANCHO-grosor_pared, 0, grosor_pared, ALTO, sprite_manager))
    
    #  Preparar dimensiones de obstáculos internos (Tony Mateo 23-eisn-2-044)
    # Obtener dimensiones del sprite de obstáculo
    sprite = sprite_manager.get_sprite('obstaculo')
    if sprite:
        ancho_obstaculo = sprite.get_width()
        alto_obstaculo = sprite.get_height()
    else:
        ancho_obstaculo = 48  # Valor por defecto
        alto_obstaculo = 48
    
    #  Definir área de jugador (zona segura) (Tony Mateo 23-eisn-2-044)
    area_jugador = pygame.Rect(ANCHO//2 - 150, ALTO//2 - 150, 300, 300)
    
    #  Generar obstáculos aleatorios con verificación estricta (Tony Mateo 23-eisn-2-044)
    obstaculos_generados = 0
    num_obstaculos_objetivo = num_obstaculos + nivel * 2  # Más obstáculos según nivel
    max_intentos = 1000  # Límite de intentos
    
    for _ in range(max_intentos):
        if obstaculos_generados >= num_obstaculos_objetivo:
            break
            
        # Generar posición candidata - ajustada a una cuadrícula
        unidad_x = ancho_obstaculo
        unidad_y = alto_obstaculo
        
        # Posiciones en cuadrícula
        pos_x = grosor_pared + random.randint(0, (ANCHO - 2*grosor_pared - ancho_obstaculo) // unidad_x) * unidad_x
        pos_y = grosor_pared + random.randint(0, (ALTO - 2*grosor_pared - alto_obstaculo) // unidad_y) * unidad_y
        
        # Convertir a enteros
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        
        # Crear rectángulo para verificar colisiones
        rect_candidato = pygame.Rect(pos_x, pos_y, ancho_obstaculo, alto_obstaculo)
        
        # 1. Verificar que no esté en el área del jugador
        if rect_candidato.colliderect(area_jugador):
            continue
            
        # 2. Verificar que no colisione con otros obstáculos (con margen)
        colision = False
        for obs in obstaculos:
            # Añadir margen de separación
            margen = 5  # 5 píxeles de separación mínima
            rect_expandido = obs.rect.inflate(margen*2, margen*2)
            if rect_candidato.colliderect(rect_expandido):
                colision = True
                break
                
        if colision:
            continue
            
        # Si pasó todas las verificaciones, crear el obstáculo (Tony Mateo 23-eisn-2-044)
        nuevo_obstaculo = Obstaculo(pos_x, pos_y, ancho_obstaculo, alto_obstaculo, sprite_manager)
        obstaculos.append(nuevo_obstaculo)
        obstaculos_generados += 1
        
        if DEBUG_MODE:
            print(f"Obstáculo #{obstaculos_generados} creado en ({pos_x}, {pos_y})")
            
    if DEBUG_MODE:
        print(f"Total de obstáculos generados: {obstaculos_generados} (objetivo: {num_obstaculos_objetivo})")
        
    return obstaculos

def dibujar_texto(pantalla, texto, pos, tamaño=32, color=BLANCO):
    """Dibuja texto en la pantalla (Tony Mateo 23-eisn-2-044)"""
    fuente = pygame.font.SysFont(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=pos)
    pantalla.blit(superficie, rect)

def calcular_angulo(origen, destino):
    """Calcula el ángulo en radianes entre dos puntos (Tony Mateo 23-eisn-2-044)"""
    import math
    dx = destino[0] - origen[0]
    dy = destino[1] - origen[1]
    return math.atan2(dy, dx)

def distancia(p1, p2):
    """Calcula la distancia entre dos puntos (Tony Mateo 23-eisn-2-044)"""
    import math
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def hay_linea_vision(origen, destino, obstaculos, pasos=20):
    """Verifica si hay línea de visión directa entre dos puntos (Tony Mateo 23-eisn-2-044)"""
    import math
    dx = destino[0] - origen[0]
    dy = destino[1] - origen[1]
    dist = math.hypot(dx, dy)
    
    if dist > 0:
        dx, dy = dx/dist, dy/dist
        # Comprobar varios puntos en la línea entre origen y destino (Tony Mateo 23-eisn-2-044)
        paso_dist = dist / pasos
        for i in range(1, pasos):
            punto_x = origen[0] + dx * i * paso_dist
            punto_y = origen[1] + dy * i * paso_dist
            punto = pygame.Rect(punto_x - 1, punto_y - 1, 2, 2)
            for obstaculo in obstaculos:
                if obstaculo.rect.colliderect(punto):
                    return False
        return True
    return False

def cargar_nivel(num_nivel):
    """Carga la configuración de un nivel específico (Tony Mateo 23-eisn-2-044)"""
    configuracion = {
        'num_npcs': 3 + num_nivel * 2,
        'velocidad_npcs': min(2 + num_nivel * 0.2, 4.0),  # Aumenta hasta un máximo de 4 (Tony Mateo 23-eisn-2-044)
        'vida_npcs': 50 + num_nivel * 10,  # Más vida en niveles superiores (Tony Mateo 23-eisn-2-044)
        'num_obstaculos': 8 + num_nivel * 2,
        'tiempo_maximo': 180 - num_nivel * 5  # Menos tiempo en niveles superiores (Tony Mateo 23-eisn-2-044)
    }
    return configuracion

# Función para verificar colisiones de forma más precisa (Tony Mateo 23-eisn-2-044)
def verificar_colision(rect1, rect2, expandir=0):
    """
    Verifica colisión entre dos rectángulos de manera precisa.
    Opcionalmente puede expandir el primer rectángulo para detección más permisiva. (Tony Mateo 23-eisn-2-044)
    """
    # Crear copias para no modificar los originales (Tony Mateo 23-eisn-2-044)
    r1 = pygame.Rect(rect1.x, rect1.y, rect1.width, rect1.height)
    r2 = pygame.Rect(rect2.x, rect2.y, rect2.width, rect2.height)
    
    # Expandir el primer rectángulo si se solicita (Tony Mateo 23-eisn-2-044)
    if expandir != 0:
        r1.inflate_ip(expandir, expandir)
    
    # Verificar colisión (Tony Mateo 23-eisn-2-044)
    return r1.colliderect(r2)

def posicion_segura(x, y, ancho, alto, obstaculos, area_prohibida=None):
    """
    Determina si una posición es segura (no colisiona con obstáculos ni está en área prohibida).
    (Tony Mateo 23-eisn-2-044)
    Parámetros:
    - x, y: Coordenadas a verificar
    - ancho, alto: Dimensiones del objeto
    - obstaculos: Lista de obstáculos a verificar
    - area_prohibida: Rect opcional para verificar
    
    Retorna:
    - True si la posición es segura, False si colisiona
    """
    # Crear rectángulo para la posición a verificar (Tony Mateo 23-eisn-2-044)
    rect = pygame.Rect(int(x), int(y), int(ancho), int(alto))
    
    # Verificar colisión con cada obstáculo (Tony Mateo 23-eisn-2-044)
    for obs in obstaculos:
        if verificar_colision(rect, obs.rect):
            return False
    
    # Verificar si está en área prohibida (Tony Mateo 23-eisn-2-044)
    if area_prohibida and rect.colliderect(area_prohibida):
        return False
    
    # Si no hay colisión, la posición es segura (Tony Mateo 23-eisn-2-044)
    return True
