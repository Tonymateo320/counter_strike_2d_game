    
import pygame
import math
import random
import heapq
from config import *
from behavior_tree import Selector, Secuencia, Hoja

class Obstaculo:
    def __init__(self, x, y, ancho, alto, sprite_manager):
        # Asegurar que las coordenadas sean enteros para evitar problemas de precisión
        self.x = int(x)
        self.y = int(y)
        self.ancho = int(ancho)
        self.alto = int(alto)
        # Crear el rectángulo de colisión con valores exactos
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.sprite_manager = sprite_manager
        
    def dibujar(self, pantalla):
        # Obtener el sprite del obstáculo
        sprite = self.sprite_manager.get_sprite('obstaculo')
        if sprite:
            # Escalar el sprite para que coincida EXACTAMENTE con el rectángulo de colisión
            sprite_escalado = pygame.transform.scale(sprite, (self.ancho, self.alto))
            # Dibujar el sprite en la posición exacta del rectángulo
            pantalla.blit(sprite_escalado, self.rect.topleft)
            # Dibujar el borde del rectángulo para visualizar el área de colisión (si DEBUG_MODE está activo)
            if DEBUG_MODE:
                pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 1)
        else:
            # Si no hay sprite, dibujar un rectángulo sólido
            pygame.draw.rect(pantalla, MARRON, self.rect)
            # Dibujar borde de colisión si DEBUG_MODE está activo
            if DEBUG_MODE:
                pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 1)

class Jugador:
    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.ancho = JUGADOR_ANCHO
        self.alto = JUGADOR_ALTO
        self.velocidad = JUGADOR_VELOCIDAD
        self.vida = JUGADOR_VIDA
        self.puntuacion = 0
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.ultimo_disparo = 0
        self.sprite_manager = sprite_manager
        self.direccion = "derecha"  # derecha, izquierda, arriba, abajo
        self.estado = "quieto"  # quieto, moviendo, disparando
        self.id = "jugador_1"  # ID único para el sprite_manager
        # Iniciar animación por defecto
        self.sprite_manager.play_animation(f"jugador_quieto_{self.direccion}", self.id)
        
    def mover(self, dx, dy, obstaculos):
        # Manejar la animación según el movimiento
        if dx == 0 and dy == 0:
            if self.estado != "disparando":
                self.estado = "quieto"
                self.sprite_manager.play_animation(f"jugador_quieto_{self.direccion}", self.id)
            return
            
        # Actualizar estado y dirección
        self.estado = "moviendo"
        if abs(dx) > abs(dy):
            self.direccion = "derecha" if dx > 0 else "izquierda"
        else:
            self.direccion = "abajo" if dy > 0 else "arriba"
            
        # Actualizar animación
        self.sprite_manager.play_animation(f"jugador_{self.estado}_{self.direccion}", self.id)
        
        # IMPORTANTE: Mover en X y en Y por separado para mejor detección de colisiones
        
        # 1. Mover en X
        nueva_x = self.x + dx
        
        # Verificar límites de pantalla
        if nueva_x < 0:
            nueva_x = 0
        elif nueva_x > ANCHO - self.ancho:
            nueva_x = ANCHO - self.ancho
            
        # Crear un rect temporal para probar el movimiento en X
        temp_rect_x = pygame.Rect(nueva_x, self.y, self.ancho, self.alto)
        
        # Verificar colisiones en X
        colision_x = False
        for obstaculo in obstaculos:
            if temp_rect_x.colliderect(obstaculo.rect):
                colision_x = True
                # Ajustar posición para que quede justo al borde del obstáculo
                if dx > 0:  # Moviendo a la derecha
                    nueva_x = obstaculo.rect.left - self.ancho
                else:  # Moviendo a la izquierda
                    nueva_x = obstaculo.rect.right
                break
                
        # Actualizar posición en X si no hay colisión o después de ajustar
        self.x = nueva_x
        
        # 2. Mover en Y
        nueva_y = self.y + dy
        
        # Verificar límites de pantalla
        if nueva_y < 0:
            nueva_y = 0
        elif nueva_y > ALTO - self.alto:
            nueva_y = ALTO - self.alto
            
        # Crear un rect temporal para probar el movimiento en Y
        temp_rect_y = pygame.Rect(self.x, nueva_y, self.ancho, self.alto)
        
        # Verificar colisiones en Y
        colision_y = False
        for obstaculo in obstaculos:
            if temp_rect_y.colliderect(obstaculo.rect):
                colision_y = True
                # Ajustar posición para que quede justo al borde del obstáculo
                if dy > 0:  # Moviendo hacia abajo
                    nueva_y = obstaculo.rect.top - self.alto
                else:  # Moviendo hacia arriba
                    nueva_y = obstaculo.rect.bottom
                break
                
        # Actualizar posición en Y si no hay colisión o después de ajustar
        self.y = nueva_y
        
        # Actualizar el rectángulo completo con la nueva posición
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def dibujar(self, pantalla):
        # Obtener el frame actual de la animación, o usar sprite estático
        frame = self.sprite_manager.get_animation_frame(self.id)
        if frame:
            pantalla.blit(frame, self.rect)
        else:
            # Si no hay animación, usar sprite normal
            sprite = self.sprite_manager.get_sprite('jugador')
            if sprite:
                pantalla.blit(sprite, self.rect)
            else:
                pygame.draw.rect(pantalla, AZUL, self.rect)
                
    def disparar(self, posicion_mouse):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > COOLDOWN_DISPARO:
            self.ultimo_disparo = ahora
            x_centro = self.x + self.ancho // 2
            y_centro = self.y + self.alto // 2
            
            # Cambiar estado a disparando brevemente
            self.estado = "disparando"
            nombre_anim = f"jugador_{self.estado}_{self.direccion}"
            self.sprite_manager.play_animation(nombre_anim, self.id)
            # Después de 200ms, volver al estado quieto
            pygame.time.set_timer(pygame.USEREVENT + 1, 200)
            
            # Calcular dirección
            dx = posicion_mouse[0] - x_centro
            dy = posicion_mouse[1] - y_centro
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx, dy = dx/dist, dy/dist
            
            return Bala(x_centro, y_centro, dx, dy, True, self.sprite_manager)
        return None

class NPC:
    def __init__(self, objetivo, obstaculos, sprite_manager):
        self.sprite_manager = sprite_manager
        self.posicion_valida = False
        # Dimensiones del NPC
        self.ancho = NPC_ANCHO
        self.alto = NPC_ALTO
        self.velocidad = NPC_VELOCIDAD
        self.vida = NPC_VIDA
        self.objetivo = objetivo
        self.tiempo_recalculo = 0
        self.camino = []
        self.tiempo_disparo = 0
        self.ultimo_calculo = 0
        self.direccion = "derecha"
        self.estado = "quieto"
        self.id = f"npc_{id(self)}"  # ID único usando la dirección en memoria
        
        # SOLUCIÓN CRÍTICA: Mejorar la ubicación inicial de NPCs
        # Intentar hasta 100 veces encontrar una posición válida que NO colisione
        max_intentos = 100
        for intento in range(max_intentos):
            # 1. Generar posición aleatoria
            self.x = random.randint(50, ANCHO - self.ancho - 50)
            self.y = random.randint(50, ALTO - self.alto - 50)
            
            # 2. Crear rectángulo de colisión para verificación
            self.rect = pygame.Rect(int(self.x), int(self.y), self.ancho, self.alto)
            
            # 3. Verificar QUE NO COLISIONE con obstáculos
            # IMPORTANTE: Lista completa de todos los obstáculos
            colision = False
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo.rect):
                    colision = True
                    if DEBUG_MODE:
                        print(f"NPC: Colisión con obstáculo en intento {intento}. Reintentando...")
                    break
                    
            if colision:
                continue  # Si hay colisión, intentar con otra posición
                
            # 4. Verificar que esté lejos del jugador (objetivo)
            distancia_al_jugador = math.sqrt((self.x - objetivo.x)**2 + (self.y - objetivo.y)**2)
            if distancia_al_jugador < 150:  # Mínimo 150 píxeles de distancia
                if DEBUG_MODE:
                    print(f"NPC: Muy cerca del jugador en intento {intento}. Reintentando...")
                continue  # Muy cerca del jugador, intentar otra posición
                
            # Si llegamos aquí, la posición es válida
            self.posicion_valida = True
            if DEBUG_MODE:
                print(f"NPC: Creado exitosamente en ({self.x}, {self.y}) después de {intento+1} intentos")
            break
            
        # Solo construir el árbol de comportamiento si la posición es válida
        if self.posicion_valida:
            # Iniciar animación por defecto
            self.sprite_manager.play_animation(f"npc_quieto_{self.direccion}", self.id)
            self.construir_arbol_comportamiento()
        else:
            if DEBUG_MODE:
                print(f"NPC: No se pudo encontrar posición válida después de {max_intentos} intentos")
                
    def construir_arbol_comportamiento(self):
        # Construimos el árbol de comportamiento
        def esta_cerca():
            dist = math.hypot(self.objetivo.x - self.x, self.objetivo.y - self.y)
            return dist < NPC_DISTANCIA_VISION
            
        def ver_objetivo(obstaculos):
            # Comprobar si hay línea de visión directa al jugador
            if esta_cerca():
                # Verificar si hay obstáculos entre el NPC y el jugador
                dx = self.objetivo.x + self.objetivo.ancho//2 - (self.x + self.ancho//2)
                dy = self.objetivo.y + self.objetivo.alto//2 - (self.y + self.alto//2)
                dist = math.hypot(dx, dy)
                
                if dist > 0:
                    dx, dy = dx/dist, dy/dist
                    # Comprobar varios puntos en la línea entre NPC y jugador
                    pasos = int(dist / 20)  # Comprobar cada 20 píxeles
                    for i in range(1, pasos):
                        punto_x = self.x + self.ancho//2 + dx * i * 20
                        punto_y = self.y + self.alto//2 + dy * i * 20
                        punto = pygame.Rect(punto_x - 1, punto_y - 1, 2, 2)
                        
                        for obstaculo in obstaculos:
                            if obstaculo.rect.colliderect(punto):
                                return False
                    return True
            return False
            
        def perseguir(obstaculos):
            self.seguir_camino(obstaculos)
            return True
            
        def vagar(obstaculos):
            # Si no tenemos un camino o hace tiempo que no recalculamos, generamos un punto aleatorio
            ahora = pygame.time.get_ticks()
            if not self.camino or ahora - self.ultimo_calculo > NPC_TIEMPO_VAGAR:
                self.ultimo_calculo = ahora
                destino_x = random.randint(0, ANCHO - self.ancho)
                destino_y = random.randint(0, ALTO - self.alto)
                
                # Convertir a coordenadas de celda
                destino = (int(destino_x // TAMANO_CELDA), int(destino_y // TAMANO_CELDA))
                inicio = (int(self.x // TAMANO_CELDA), int(self.y // TAMANO_CELDA))
                
                # Calcular camino
                self.calcular_camino_a_punto(inicio, destino, obstaculos)
                
            self.seguir_camino(obstaculos)
            return True
            
        # Construir el árbol con una estructura más simple y robusta
        self.raiz = Selector([
            Secuencia([
                Hoja(lambda obs=None: esta_cerca()),
                Hoja(ver_objetivo),
                Hoja(perseguir)
            ]),
            Hoja(vagar)
        ])
        
    def es_celda_valida(self, x, y, obstaculos):
        # Comprobar límites del mapa
        if not (0 <= x < ANCHO // TAMANO_CELDA and 0 <= y < ALTO // TAMANO_CELDA):
            return False
            
        # Comprobar colisiones con obstáculos
        celda_rect = pygame.Rect(
            x * TAMANO_CELDA, 
            y * TAMANO_CELDA, 
            TAMANO_CELDA, 
            TAMANO_CELDA
        )
        
        for obstaculo in obstaculos:
            if celda_rect.colliderect(obstaculo.rect):
                return False
                
        return True
        
    def calcular_camino_a_punto(self, inicio, fin, obstaculos):
        # Implementación básica de A*
        abiertos = []
        abiertos_set = set([inicio])  # Para búsqueda más eficiente
        cerrados = set()
        g_score = {inicio: 0}
        f_score = {inicio: self.heuristica(inicio, fin)}
        heapq.heappush(abiertos, (f_score[inicio], inicio))
        came_from = {}
        
        while abiertos:
            _, actual = heapq.heappop(abiertos)
            abiertos_set.remove(actual)
            
            if actual == fin:
                # Reconstruir camino
                camino = []
                while actual in came_from:
                    camino.append((actual[0] * TAMANO_CELDA + TAMANO_CELDA // 2, 
                                   actual[1] * TAMANO_CELDA + TAMANO_CELDA // 2))
                    actual = came_from[actual]
                self.camino = camino[::-1]  # Invertir para tener desde inicio a fin
                return
                
            cerrados.add(actual)
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                vecino = (actual[0] + dx, actual[1] + dy)
                
                if not self.es_celda_valida(vecino[0], vecino[1], obstaculos):
                    continue
                    
                if vecino in cerrados:
                    continue
                    
                # Calcular coste adicional para movimientos diagonales
                coste_mov = 1.4 if dx != 0 and dy != 0 else 1.0
                tentative_g = g_score[actual] + coste_mov
                
                if vecino not in abiertos_set or tentative_g < g_score.get(vecino, float('inf')):
                    came_from[vecino] = actual
                    g_score[vecino] = tentative_g
                    f_score[vecino] = tentative_g + self.heuristica(vecino, fin)
                    
                    if vecino not in abiertos_set:
                        heapq.heappush(abiertos, (f_score[vecino], vecino))
                        abiertos_set.add(vecino)
                        
    def calcular_camino(self, obstaculos):
        # Convertir posiciones a coordenadas de celda
        inicio = (int(self.x // TAMANO_CELDA), int(self.y // TAMANO_CELDA))
        fin = (int(self.objetivo.x // TAMANO_CELDA), int(self.objetivo.y // TAMANO_CELDA))
        self.calcular_camino_a_punto(inicio, fin, obstaculos)
        
    def heuristica(self, a, b):
        # Distancia diagonal (permite movimientos en 8 direcciones)
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy) + 0.4 * min(dx, dy)
        
    def seguir_camino(self, obstaculos):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_recalculo > NPC_RECALCULO_CAMINO:
            self.tiempo_recalculo = ahora
            self.calcular_camino(obstaculos)
            
        if self.camino:
            siguiente = self.camino[0]
            dx = siguiente[0] - (self.x + self.ancho // 2)
            dy = siguiente[1] - (self.y + self.alto // 2)
            dist = math.hypot(dx, dy)
            
            if dist < self.velocidad:
                self.camino.pop(0)
                if not self.camino:
                    self.estado = "quieto"
                    nombre_anim = f"npc_{self.estado}_{self.direccion}"
                    self.sprite_manager.play_animation(nombre_anim, self.id)
                    return
                    
            self.estado = "moviendo"
            
            # Actualizar dirección basado en el movimiento
            if abs(dx) > abs(dy):
                self.direccion = "derecha" if dx > 0 else "izquierda"
            else:
                self.direccion = "arriba" if dy < 0 else "abajo"
                
            # Actualizar la animación
            nombre_anim = f"npc_{self.estado}_{self.direccion}"
            self.sprite_manager.play_animation(nombre_anim, self.id)
            
            if dist > 0:
                dx, dy = dx/dist * self.velocidad, dy/dist * self.velocidad
                
            # MOVIMIENTO CRÍTICO: Similar al del jugador, verificación completa
            
            # Intentar mover en X
            nueva_x = int(self.x + dx)
            
            # Crear un rect EXACTO para colisión en X (sin margen)
            temp_rect_x = pygame.Rect(
                nueva_x, 
                self.y, 
                self.ancho, 
                self.alto
            )
            
            # Verificar colisión con cada obstáculo
            colision_x = False
            for obstaculo in obstaculos:
                if temp_rect_x.colliderect(obstaculo.rect):
                    colision_x = True
                    # Ajustar posición para que quede justo al borde del obstáculo
                    if dx > 0:  # Moviendo a la derecha
                        nueva_x = obstaculo.rect.left - self.ancho
                    else:  # Moviendo a la izquierda
                        nueva_x = obstaculo.rect.right
                    break
                    
            # Solo actualizar si NO hay colisión o después de ajustar
            self.x = nueva_x
            
            # Intentar mover en Y
            nueva_y = int(self.y + dy)
            
            # Crear un rect EXACTO para colisión en Y
            temp_rect_y = pygame.Rect(
                self.x, 
                nueva_y, 
                self.ancho, 
                self.alto
            )
            
            # Verificar colisión con cada obstáculo
            colision_y = False
            for obstaculo in obstaculos:
                if temp_rect_y.colliderect(obstaculo.rect):
                    colision_y = True
                    # Ajustar posición para que quede justo al borde del obstáculo
                    if dy > 0:  # Moviendo hacia abajo
                        nueva_y = obstaculo.rect.top - self.alto
                    else:  # Moviendo hacia arriba
                        nueva_y = obstaculo.rect.bottom
                    break
                    
            # Solo actualizar si NO hay colisión o después de ajustar
            self.y = nueva_y
            
            # Si hay colisión en ambos ejes, recalcular el camino
            if colision_x and colision_y:
                self.camino = []
                
            # CRÍTICO: Actualizar el rect completo al final para asegurar consistencia
            self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
            
    def ver_objetivo(self, obstaculos):
        # Comprobar si hay línea de visión directa al jugador
        # Verificar si hay obstáculos entre el NPC y el jugador
        dx = self.objetivo.x + self.objetivo.ancho//2 - (self.x + self.ancho//2)
        dy = self.objetivo.y + self.objetivo.alto//2 - (self.y + self.alto//2)
        dist = math.hypot(dx, dy)
        
        if dist > 0 and dist < NPC_DISTANCIA_VISION:
            dx, dy = dx/dist, dy/dist
            # Comprobar varios puntos en la línea entre NPC y jugador
            pasos = int(dist / 20)  # Comprobar cada 20 píxeles
            for i in range(1, pasos):
                punto_x = self.x + self.ancho//2 + dx * i * 20
                punto_y = self.y + self.alto//2 + dy * i * 20
                punto = pygame.Rect(punto_x - 1, punto_y - 1, 2, 2)
                
                for obstaculo in obstaculos:
                    if obstaculo.rect.colliderect(punto):
                        return False
            return True
        return False
        
    def disparar(self, obstaculos):
        """Intenta disparar al objetivo si hay línea de visión despejada"""
        if self.ver_objetivo(obstaculos):  # Verificar línea de visión con los obstáculos
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_disparo > NPC_COOLDOWN_DISPARO:  # Disparar cada segundo
                self.tiempo_disparo = ahora
                
                # Cambiar estado a disparando
                self.estado = "disparando"
                nombre_anim = f"npc_{self.estado}_{self.direccion}"
                self.sprite_manager.play_animation(nombre_anim, self.id)
                
                dx = self.objetivo.x - self.x
                dy = self.objetivo.y - self.y
                dist = math.hypot(dx, dy)
                
                # Actualizar dirección basada en el objetivo
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.direccion = "derecha"
                    else:
                        self.direccion = "izquierda"
                else:
                    if dy > 0:
                        self.direccion = "abajo"
                    else:
                        self.direccion = "arriba"
                        
                if dist > 0:
                    dx, dy = dx/dist, dy/dist
                return Bala(self.x + self.ancho//2, self.y + self.alto//2, dx, dy, False, self.sprite_manager)
        return None
        
    def actualizar(self, obstaculos):
        # Ejecutar el árbol de comportamiento pasando los obstáculos
        self.raiz.ejecutar(obstaculos)
        
    def dibujar(self, pantalla):
        # Obtener el frame actual de la animación, o usar sprite estático
        frame = self.sprite_manager.get_animation_frame(self.id)
        if frame:
            pantalla.blit(frame, self.rect)
        else:
            # Si no hay animación, usar sprite normal
            sprite = self.sprite_manager.get_sprite('npc')
            if sprite:
                pantalla.blit(sprite, self.rect)
            else:
                pygame.draw.rect(pantalla, ROJO, self.rect)

class Bala:
    def __init__(self, x, y, dx, dy, es_jugador=True, sprite_manager=None):
        self.x = x
        self.y = y
        self.dx = dx * BALA_VELOCIDAD
        self.dy = dy * BALA_VELOCIDAD
        self.radio = BALA_RADIO
        self.es_jugador = es_jugador
        self.rect = pygame.Rect(x - self.radio, y - self.radio, self.radio * 2, self.radio * 2)
        self.sprite_manager = sprite_manager
        
    def actualizar(self, obstaculos):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x - self.radio
        self.rect.y = self.y - self.radio
        
        # Verificar si la bala está fuera de pantalla
        if self.x < 0 or self.x > ANCHO or self.y < 0 or self.y > ALTO:
            return False
            
        # Verificar colisión con obstáculos
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo.rect):
                return False
                
        return True
        
    def dibujar(self, pantalla):
        # Si hay un sprite disponible, usarlo; si no, dibujar un círculo
        sprite_key = 'bala_jugador' if self.es_jugador else 'bala_npc'
        sprite = self.sprite_manager.get_sprite(sprite_key)
        if sprite:
            pantalla.blit(sprite, self.rect)
        else:
            pygame.draw.circle(pantalla, BLANCO, (int(self.x), int(self.y)), self.radio)

class Moneda:
    def __init__(self, x, y, valor, sprite_manager):
        self.x = x
        self.y = y
        self.valor = valor
        self.ancho = 15
        self.alto = 15
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.sprite_manager = sprite_manager
        self.id = f"moneda_{id(self)}"
        # Intentar iniciar animación si existe
        self.sprite_manager.play_animation("moneda_girando", self.id)
        
    def dibujar(self, pantalla):
        # Obtener frame de la animación o usar sprite estático
        frame = self.sprite_manager.get_animation_frame(self.id)
        if frame:
            pantalla.blit(frame, self.rect)
        else:
            # Si no hay animación, usar sprite normal o dibujar un círculo amarillo
            sprite = self.sprite_manager.get_sprite('moneda')
            if sprite:
                pantalla.blit(sprite, self.rect)
            else:
                # Dibujar un círculo amarillo como fallback
                pygame.draw.circle(
                    pantalla, 
                    (255, 215, 0),  # Color oro
                    (self.x + self.ancho // 2, self.y + self.alto // 2), 
                    self.ancho // 2
                )
                # Añadir brillo para que parezca más una moneda
                pygame.draw.circle(
                    pantalla, 
                    (255, 255, 200),  # Color amarillo claro para el brillo
                    (self.x + self.ancho // 4, self.y + self.alto // 4), 
                    self.ancho // 6
                )

class Pocion:
    def __init__(self, x, y, valor_curacion, sprite_manager):
        self.x = x
        self.y = y
        self.valor_curacion = valor_curacion
        self.ancho = 20
        self.alto = 20
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.sprite_manager = sprite_manager
        self.id = f"pocion_{id(self)}"
        # Intentar iniciar animación si existe
        self.sprite_manager.play_animation("pocion_brillando", self.id)
        
    def dibujar(self, pantalla):
        # Obtener frame de la animación o usar sprite estático
        frame = self.sprite_manager.get_animation_frame(self.id)
        if frame:
            pantalla.blit(frame, self.rect)
        else:
            # Si no hay animación, usar sprite normal o dibujar una poción simple
            sprite = self.sprite_manager.get_sprite('pocion')
            if sprite:
                pantalla.blit(sprite, self.rect)
            else:
                # Dibujar un frasco rojo como fallback
                # Cuerpo del frasco
                pygame.draw.rect(
                    pantalla, 
                    (255, 0, 0),  # Rojo
                    pygame.Rect(self.x + 4, self.y + 8, self.ancho - 8, self.alto - 8)
                )
                # Cuello del frasco
                pygame.draw.rect(
                    pantalla, 
                    (200, 200, 200),  # Gris claro
                    pygame.Rect(self.x + 7, self.y + 3, 6, 5)
                )
                # Tapa
                pygame.draw.rect(
                    pantalla, 
                    (100, 100, 100),  # Gris oscuro
                    pygame.Rect(self.x + 6, self.y, 8, 3)
                )
                # Borde para el frasco
                pygame.draw.rect(
                    pantalla, 
                    (255, 255, 255),  # Blanco
                    pygame.Rect(self.x + 4, self.y + 8, self.ancho - 8, self.alto - 8),
                    1
                )