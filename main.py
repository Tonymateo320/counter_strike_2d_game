## Libreria Tony Mateo 23-eisn-2-044

import os
import pygame
import sys
import time
import random
from config import *
from game_objects import Jugador, NPC, Bala, Obstaculo, Moneda, Pocion
from utils import Boton, generar_obstaculos
from sprite_manager import SpriteManager
from textos import DamegeText

# Inicialización de Pygame Tony Mateo 23-eisn-2-044
pygame.init()

# Configuración de la pantalla Tony Mateo 23-eisn-2-044
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Counter Strike 2D")
reloj = pygame.time.Clock()

font=pygame.font.SysFont("./copy/font/TruType (.ttf)/Linerama-Regular.fff", 30)
print(font)

# def dibujar_texto(txto, fuente, color, x,y):
#     img=fuente.render(txto, True, color) 
#     ventana.blit(img, (x, y))
# Verificar y crear estructura de sprites si es necesario Tony Mateo 23-eisn-2-044
def verificar_estructura_sprites():
    """Verifica si la estructura de directorios para sprites existe, si no, la crea"""
    if not os.path.exists("sprites"):
        print("Directorio 'sprites' no encontrado. Ejecutando preparar_animaciones.py...")
        try:
            import preparar_animaciones
            preparar_animaciones.main()
            print("Estructura de sprites creada correctamente.")
            return True
        except ImportError:
            print("No se pudo importar preparar_animaciones.py")
            return False
    return True

# Inicializar gestor de sprites Tony Mateo 23-eisn-2-044
sprite_manager = SpriteManager()

# Cargar sprites y animaciones Tony Mateo 23-eisn-2-044
def cargar_recursos():
    """Carga todos los sprites y animaciones necesarios para el juego"""
    print("Inicializando recursos gráficos...")
    
    # Verificar y crear estructura si es necesario Tony Mateo 23-eisn-2-044
    if not verificar_estructura_sprites():
        print("¡ADVERTENCIA! No se pudo verificar la estructura de sprites.")
    
    # Cargar sprites individuales
    print("Cargando sprites individuales...")
    if os.path.exists("sprites"):
        sprite_manager.load_all_sprites_from_directory('sprites')
    
    # Cargar todas las animaciones Tony Mateo 23-eisn-2-044
    print("Cargando animaciones...")
    sprite_manager.load_all_animations()
    
    print("Recursos gráficos inicializados correctamente.")

# Cargar recursos al inicio Tony Mateo 23-eisn-2-044
cargar_recursos()

# Variables globales Tony Mateo 23-eisn-2-044
jugador = None
npcs = []
balas = []
obstaculos = []
monedas = []
pociones = []
textos_dano = []
nivel_actual = 0
max_niveles = 10
estado_juego = "menu"  

# Botones para el menú Tony Mateo 23-eisn-2-044
boton_iniciar = Boton(ANCHO//2 - 100, ALTO//2 - 50, 200, 50, "Iniciar Juego", VERDE, (0, 200, 0))
boton_salir = Boton(ANCHO//2 - 100, ALTO//2 + 50, 200, 50, "Salir", ROJO, (200, 0, 0))

# Función para generar monedas Tony Mateo 23-eisn-2-044
def generar_monedas(cantidad, obstaculos):
    """Genera monedas distribuidas aleatoriamente en el nivel"""
    global monedas
    monedas = []
    for _ in range(cantidad):
        intentos = 100
        for _ in range(intentos):
            x = random.randint(50, ANCHO - 50)
            y = random.randint(50, ALTO - 50)
            
            rect_moneda = pygame.Rect(x, y, 15, 15)
            
            # Verificar que no colisiona con obstáculos Tony Mateo 23-eisn-2-044
            colision = False
            for obs in obstaculos:
                if rect_moneda.colliderect(obs.rect):
                    colision = True
                    break
            
            if not colision:
                monedas.append(Moneda(x, y, 10, sprite_manager))  
                break
    
    if DEBUG_MODE:
        print(f"Generadas {len(monedas)} monedas")

# Función para generar pociones  Tony Mateo 23-eisn-2-044
def generar_pociones(cantidad, obstaculos):
    """Genera pociones distribuidas aleatoriamente en el nivel"""
    global pociones
    pociones = []
    for _ in range(cantidad):
        intentos = 100
        for _ in range(intentos):
            x = random.randint(50, ANCHO - 50)
            y = random.randint(50, ALTO - 50)
            
            rect_pocion = pygame.Rect(x, y, 20, 20)
            
            # Verificar que no colisiona con obstáculos u otras pociones Tony Mateo 23-eisn-2-044
            colision = False
            for obs in obstaculos:
                if rect_pocion.colliderect(obs.rect):
                    colision = True
                    break
            
            for moneda in monedas:
                if rect_pocion.colliderect(moneda.rect):
                    colision = True
                    break
            
            if not colision:
                pociones.append(Pocion(x, y, 25, sprite_manager))  # Recupera 25 de vida Tony Mateo 23-eisn-2-044
                break
    
    if DEBUG_MODE:
        print(f"Generadas {len(pociones)} pociones")

def iniciar_nivel(nivel):
    global jugador, npcs, balas, obstaculos, monedas, pociones, textos_dano
    
    if DEBUG_MODE:
        print(f"Iniciando nivel {nivel + 1}")
    
    jugador = Jugador(ANCHO // 2, ALTO // 2, sprite_manager)
    npcs = []
    balas = []
    textos_dano = []
    
    # Generar obstáculos Tony Mateo 23-eisn-2-044
    obstaculos = generar_obstaculos(nivel, sprite_manager)
    
    # Configurar NPCs según el nivel Tony Mateo 23-eisn-2-044
    num_npcs = 3 + nivel * 2
    for _ in range(num_npcs):
        npc = NPC(jugador, obstaculos, sprite_manager)
        if npc.posicion_valida:
            npcs.append(npc)
    
    # Generar monedas (5 + nivel monedas por nivel) Tony Mateo 23-eisn-2-044
    generar_monedas(5 + nivel, obstaculos)
    
    # Generar pociones (2 pociones por nivel) Tony Mateo 23-eisn-2-044
    generar_pociones(2, obstaculos)
    
    if DEBUG_MODE:
        print(f"Nivel {nivel + 1} iniciado con {len(npcs)} NPCs, {len(monedas)} monedas y {len(pociones)} pociones")

# Al inicio del archivo, después de las importaciones Tony Mateo 23-eisn-2-044
DEBUG_MODE = False

def dibujar_debug_info(pantalla, jugador, obstaculos):
    if not DEBUG_MODE:
        return
        
    # Dibujar información de posición del jugador Tony Mateo 23-eisn-2-044
    fuente = pygame.font.SysFont(None, 24)
    info_jugador = fuente.render(f"Jugador: ({int(jugador.x)}, {int(jugador.y)})", True, (255, 255, 0))
    pantalla.blit(info_jugador, (ANCHO - 220, 10))
    
    # Dibujar rectángulo del jugador Tony Mateo 23-eisn-2-044
    pygame.draw.rect(pantalla, (0, 255, 255), jugador.rect, 2)
    
    # Dibujar información de obstáculos
    for i, obs in enumerate(obstaculos):
        # Solo mostrar información de obstáculos cercanos al jugador Tony Mateo 23-eisn-2-044
        distancia = ((jugador.x - obs.rect.x)**2 + (jugador.y - obs.rect.y)**2)**0.5
        if distancia < 200:  # Mostrar solo obstáculos cercanos Tony Mateo 23-eisn-2-044
            texto = fuente.render(f"#{i}: ({obs.rect.x}, {obs.rect.y})", True, (255, 255, 0))
            pantalla.blit(texto, (obs.rect.x, obs.rect.y - 20))

def dibujar_menu():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 64)
    titulo = fuente.render("Counter Strike 2D", True, BLANCO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//4))
    
    boton_iniciar.dibujar(pantalla)
    boton_salir.dibujar(pantalla)

def dibujar_juego():
    # Dibujar fondo Tony Mateo 23-eisn-2-044
    pantalla.fill(GRIS)
    
    # Dibujar obstáculos Tony Mateo 23-eisn-2-044
    for obstaculo in obstaculos:
        obstaculo.dibujar(pantalla)
    
    # Dibujar monedas Tony Mateo 23-eisn-2-044
    for moneda in monedas:
        moneda.dibujar(pantalla)
        
    # Dibujar pociones Tony Mateo 23-eisn-2-044
    for pocion in pociones:
        pocion.dibujar(pantalla)
    
    # Dibujar jugador y NPCs Tony Mateo 23-eisn-2-044
    jugador.dibujar(pantalla)
    for npc in npcs:
        npc.dibujar(pantalla)
    
    # Dibujar balas Tony Mateo 23-eisn-2-044
    for bala in balas:
        bala.dibujar(pantalla)
    
    # Dibujar textos de daño Tony Mateo 23-eisn-2-044
    for texto in textos_dano:
        texto.dibujar(pantalla)
    
    # Mostrar vida y puntuación Tony Mateo 23-eisn-2-044
    fuente = pygame.font.SysFont(None, 32)
    vida_texto = fuente.render(f"Vida: {jugador.vida}", True, BLANCO)
    puntuacion_texto = fuente.render(f"Puntuación: {jugador.puntuacion}", True, BLANCO)
    nivel_texto = fuente.render(f"Nivel: {nivel_actual + 1}/{max_niveles}", True, BLANCO)
    
    pantalla.blit(vida_texto, (10, 10))
    pantalla.blit(puntuacion_texto, (10, 50))
    pantalla.blit(nivel_texto, (10, 90))
    
    # Mostrar información de depuración si está activado Tony Mateo 23-eisn-2-044
    if DEBUG_MODE:
        dibujar_debug_info(pantalla, jugador, obstaculos)

def toggle_debug_mode():
    """Alterna el modo de depuración cuando se presiona F1"""
    global DEBUG_MODE
    DEBUG_MODE = not DEBUG_MODE
    print(f"Modo depuración: {'ACTIVADO' if DEBUG_MODE else 'DESACTIVADO'}")

def mostrar_debug(pantalla, jugador, npcs, obstaculos):
    """Muestra información detallada de depuración"""
    if not DEBUG_MODE:
        return
    
    # Fuente pequeña para texto de depuración Tony Mateo 23-eisn-2-044
    fuente_debug = pygame.font.SysFont(None, 16)
    
    # Información del jugador Tony Mateo 23-eisn-2-044
    pos_jugador = f"Jugador: ({int(jugador.x)}, {int(jugador.y)})"
    txt_jugador = fuente_debug.render(pos_jugador, True, (255, 255, 0))
    pantalla.blit(txt_jugador, (10, 130))
    
    # Dibujar rectángulo del jugador Tony Mateo 23-eisn-2-044
    pygame.draw.rect(pantalla, (0, 255, 0), jugador.rect, 1)
    
    # Mostrar información de NPCs Tony Mateo 23-eisn-2-044
    for i, npc in enumerate(npcs):
        if npc.posicion_valida:
            info_npc = f"NPC #{i}: ({int(npc.x)}, {int(npc.y)})"
            txt_npc = fuente_debug.render(info_npc, True, (255, 200, 0))
            pantalla.blit(txt_npc, (10, 150 + i*15))
            
            # Mostrar rectángulo del NPC Tony Mateo 23-eisn-2-044
            pygame.draw.rect(pantalla, (255, 0, 0), npc.rect, 1)
    
    # Mostrar información de obstáculos cercanos Tony Mateo 23-eisn-2-044
    obstaculos_mostrados = 0
    for i, obs in enumerate(obstaculos):
        # Calcular distancia al jugador Tony Mateo 23-eisn-2-044
        dist_jugador = ((jugador.x - obs.x)**2 + (jugador.y - obs.y)**2)**0.5
        if dist_jugador < 200:  # Solo mostrar obstáculos cercanos
            info_obs = f"Obs #{i}: ({int(obs.x)}, {int(obs.y)})"
            txt_obs = fuente_debug.render(info_obs, True, (0, 255, 255))
            pantalla.blit(txt_obs, (ANCHO - 150, 10 + obstaculos_mostrados*15))
            obstaculos_mostrados += 1
            
            # Destacar rectángulo de obstáculo Tony Mateo 23-eisn-2-044
            pygame.draw.rect(pantalla, (255, 0, 255), obs.rect, 1)

def dibujar_game_over():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 64)
    texto = fuente.render("¡GAME OVER!", True, ROJO)
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
    
    fuente_pequena = pygame.font.SysFont(None, 32)
    puntuacion_texto = fuente_pequena.render(f"Puntuación final: {jugador.puntuacion}", True, BLANCO)
    pantalla.blit(puntuacion_texto, (ANCHO//2 - puntuacion_texto.get_width()//2, ALTO//2 + 50))
    
    mensaje = fuente_pequena.render("Presiona ESPACIO para volver al menú", True, BLANCO)
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 + 100))

def dibujar_victoria():
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 64)
    texto = fuente.render("¡VICTORIA!", True, VERDE)
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
    
    fuente_pequena = pygame.font.SysFont(None, 32)
    puntuacion_texto = fuente_pequena.render(f"Puntuación final: {jugador.puntuacion}", True, BLANCO)
    pantalla.blit(puntuacion_texto, (ANCHO//2 - puntuacion_texto.get_width()//2, ALTO//2 + 50))
    
    mensaje = fuente_pequena.render("Presiona ESPACIO para volver al menú", True, BLANCO)
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 + 100))

# Registrar eventos personalizados Tony Mateo 23-eisn-2-044
EVENTO_FIN_DISPARO_JUGADOR = pygame.USEREVENT + 1
EVENTO_FIN_DISPARO_NPC = pygame.USEREVENT + 2

# Bucle principal del juego Tony Mateo 23-eisn-2-044
def ejecutar_juego():
    global estado_juego, nivel_actual, DEBUG_MODE
    
    ejecutando = True
    ultimo_tiempo = time.time()
    
    while ejecutando:
        # Calcular tiempo delta para animaciones suaves Tony Mateo 23-eisn-2-044
        tiempo_actual = time.time()
        delta_tiempo = tiempo_actual - ultimo_tiempo
        ultimo_tiempo = tiempo_actual
        
        # Actualizar todas las animaciones Tony Mateo 23-eisn-2-044
        sprite_manager.update_animations()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and estado_juego == "menu":
                pos = pygame.mouse.get_pos()
                if boton_iniciar.es_clic(pos):
                    estado_juego = "jugando"
                    nivel_actual = 0
                    try:
                        sonido_fondo = pygame.mixer.music.load("./sound/fondo.mp3")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.5)
                    except:
                        print("No se pudo cargar el sonido de fondo")
                    iniciar_nivel(nivel_actual)
                elif boton_salir.es_clic(pos):
                    ejecutando = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"
                
                elif evento.key == pygame.K_F1:  
                    DEBUG_MODE = not DEBUG_MODE
                    print(f"Modo depuración: {'ACTIVADO' if DEBUG_MODE else 'DESACTIVADO'}")
                
                elif estado_juego in ["game_over", "victoria"] and evento.key == pygame.K_SPACE:
                    estado_juego = "menu"
            
            # Eventos para animaciones de disparo Tony Mateo 23-eisn-2-044
            elif evento.type == EVENTO_FIN_DISPARO_JUGADOR and jugador:
                jugador.estado = "quieto"
                sprite_manager.play_animation(f"jugador_quieto_{jugador.direccion}", jugador.id)
            
            elif evento.type == EVENTO_FIN_DISPARO_NPC:
                # Encontrar el NPC que disparó por su ID Tony Mateo 23-eisn-2-044
                for npc in npcs:
                    if evento.entity_id == id(npc):
                        npc.estado = "quieto"
                        sprite_manager.play_animation(f"npc_quieto_{npc.direccion}", npc.id)
                        break
        
        if estado_juego == "menu":
            dibujar_menu()
        
        elif estado_juego == "jugando":
            # Movimiento del jugador Tony Mateo 23-eisn-2-044
            teclas = pygame.key.get_pressed()
            dx, dy = 0, 0
            if teclas[pygame.K_a]: dx -= jugador.velocidad
            if teclas[pygame.K_d]: dx += jugador.velocidad
            if teclas[pygame.K_w]: dy -= jugador.velocidad
            if teclas[pygame.K_s]: dy += jugador.velocidad
            jugador.mover(dx, dy, obstaculos)
            
            
            # Disparo del jugador Tony Mateo 23-eisn-2-044
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                bala = jugador.disparar((mx, my))
                if bala and jugador.estado == "disparando":
                    balas.append(bala)
                    try:
                        sonido_disparo = pygame.mixer.Sound("./sound/disparo.mp3")
                        sonido_disparo.play()
                        
                    except:
                        pass
                    # Programar evento para volver al estado quieto Tony Mateo 23-eisn-2-044
                    pygame.time.set_timer(EVENTO_FIN_DISPARO_JUGADOR, 200, False)
            
            # Actualizar NPCs Tony Mateo 23-eisn-2-044
            for npc in npcs:
                npc.actualizar(obstaculos)
                npc_bala = npc.disparar(obstaculos)
                if npc_bala and npc.estado == "disparando":
                    balas.append(npc_bala)
                    ## sonido de los disparos Tony Mateo 23-eisn-2-044
                    try:
                        sonido_disparo = pygame.mixer.Sound("./sound/disparo.mp3")
                        sonido_disparo.play()

                    except:
                        pass
                    # Programar evento para volver al estado quieto Tony Mateo 23-eisn-2-044
                    evento = pygame.event.Event(EVENTO_FIN_DISPARO_NPC, {'entity_id': id(npc)})
                    pygame.event.post(evento)
            
            # Actualizar balas y verificar colisiones Tony Mateo 23-eisn-2-044
            balas_para_eliminar = []
            for i, bala in enumerate(balas):
                if not bala.actualizar(obstaculos):
                    balas_para_eliminar.append(i)
                    continue
                
                # Colisión con NPCs Tony Mateo 23-eisn-2-044
                if bala.es_jugador:
                    for j, npc in enumerate(npcs):
                        if bala.rect.colliderect(npc.rect):
                            dano = 25  
                            npc.vida -= dano
                            
                            # Crear texto de daño Tony Mateo 23-eisn-2-044
                            texto_dano = DamegeText(
                                npc.x + npc.ancho // 2,  # Centrado en el NPC
                                npc.y - 10,  # Justo arriba del NPC
                                dano
                            )
                            textos_dano.append(texto_dano)
                            
                            balas_para_eliminar.append(i)
                            if npc.vida <= 0:
                                npcs.pop(j)
                                jugador.puntuacion += 100
                            break
                # Colisión con jugador Tony Mateo 23-eisn-2-044
                elif bala.rect.colliderect(jugador.rect):
                    jugador.vida -= 10
                    balas_para_eliminar.append(i)
                    if jugador.vida <= 0:
                        estado_juego = "game_over"
            
            # Eliminar balas Tony Mateo 23-eisn-2-044
            for i in sorted(balas_para_eliminar, reverse=True):
                if i < len(balas):
                    balas.pop(i)
            
            # Actualizar textos de daño Tony Mateo 23-eisn-2-044
            textos_dano_para_eliminar = []
            for i, texto in enumerate(textos_dano):
                if not texto.actualizar():
                    textos_dano_para_eliminar.append(i)
            
            # Eliminar textos que ya terminaron Tony Mateo 23-eisn-2-044
            for i in sorted(textos_dano_para_eliminar, reverse=True):
                if i < len(textos_dano):
                    textos_dano.pop(i)
            
            # Colisión con monedas Tony Mateo 23-eisn-2-044
            monedas_para_eliminar = []
            for i, moneda in enumerate(monedas):
                if moneda.rect.colliderect(jugador.rect):
                    jugador.puntuacion += moneda.valor
                    monedas_para_eliminar.append(i)
                    
                    try:
                        sonido_moneda = pygame.mixer.Sound("./sound/moneda.mp3")
                        sonido_moneda.play()
                    except:
                        pass
            
            # Eliminar monedas recogidas Tony Mateo 23-eisn-2-044
            for i in sorted(monedas_para_eliminar, reverse=True):
                if i < len(monedas):
                    monedas.pop(i)
            
            # Colisión con pociones
            pociones_para_eliminar = []
            for i, pocion in enumerate(pociones):
                if pocion.rect.colliderect(jugador.rect):
                    # Recuperar vida, pero sin exceder el máximo Tony Mateo 23-eisn-2-044
                    jugador.vida = min(jugador.vida + pocion.valor_curacion, JUGADOR_VIDA)
                    pociones_para_eliminar.append(i)
                    
                    try:
                        sonido_pocion = pygame.mixer.Sound("./sound/posion.mp3")
                        sonido_pocion.play()
                    except:
                        pass
            
            # Eliminar pociones usadas Tony Mateo 23-eisn-2-044
            for i in sorted(pociones_para_eliminar, reverse=True):
                if i < len(pociones):
                    pociones.pop(i)
            
            # Verificar si se han eliminado todos los NPCs Tony Mateo 23-eisn-2-044
            if not npcs:
                nivel_actual += 1
                if nivel_actual >= max_niveles:
                    estado_juego = "victoria"
                else:
                    iniciar_nivel(nivel_actual)
            
            dibujar_juego()
        
        elif estado_juego == "game_over":
            try:
                sonido_fondo = pygame.mixer.music.load("./sound/fondo.mp3")
                # print("tony: ",sonido_fondo)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            except:
                pass
            dibujar_game_over()
        
        elif estado_juego == "victoria":
            dibujar_victoria()
        
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    ejecutar_juego()