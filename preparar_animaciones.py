
import sys
import io
import os
import pygame
import shutil
from PIL import Image, ImageOps

# Inicializar pygame (necesario para algunos elementos) Tony Mateo 23-eisn-2-044
pygame.init()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def crear_estructura_directorios():
    """Crea la estructura de directorios completa para el juego"""
    print("Creando estructura de directorios...")
    
    # Estructura básica Tony Mateo 23-eisn-2-044
    directorios = [
        "sprites",
        "sprites/jugador",
        "sprites/jugador/quieto",
        "sprites/jugador/moviendo",
        "sprites/jugador/disparando",
        "sprites/npc",
        "sprites/npc/quieto",
        "sprites/npc/moviendo",
        "sprites/npc/disparando"
    ]
    
    # Añadir subdirectorios para direcciones Tony Mateo 23-eisn-2-044
    entidades = ["jugador", "npc"]
    estados = ["quieto", "moviendo", "disparando"]
    direcciones = ["derecha", "izquierda", "arriba", "abajo"]
    
    for entidad in entidades:
        for estado in estados:
            for direccion in direcciones:
                directorios.append(f"sprites/{entidad}/{estado}/{direccion}")
    
    # Crear todos los directorios Tony Mateo 23-eisn-2-044
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
    
    print("✓ Estructura de directorios creada.")

def distribuir_frames_por_estado(entidad, frames_por_estado):
    """Distribuye los frames por estado para una entidad específica"""
    print(f"\nDistribuyendo frames de {entidad}...")
    
    # Verificar que se proporcionaron frames para al menos un estado Tony Mateo 23-eisn-2-044
    if not frames_por_estado:
        print(f"⚠ Error: No se proporcionaron frames para {entidad}")
        return False
        
    # Verificar que todos los archivos existen Tony Mateo 23-eisn-2-044
    for estado, frames in frames_por_estado.items():
        for frame in frames:
            if not os.path.exists(frame):
                print(f"⚠ Error: No se encontró el archivo {frame}")
                return False
    
    # Guardar una copia del primer frame como sprite base Tony Mateo 23-eisn-2-044
    primer_frame = frames_por_estado.get("quieto", [None])[0]
    if not primer_frame and "moviendo" in frames_por_estado and frames_por_estado["moviendo"]:
        primer_frame = frames_por_estado["moviendo"][0]
    if not primer_frame and "disparando" in frames_por_estado and frames_por_estado["disparando"]:
        primer_frame = frames_por_estado["disparando"][0]
        
    if primer_frame:
        shutil.copy(primer_frame, f"sprites/{entidad}.png")
        print(f"✓ Sprite base de {entidad} guardado: sprites/{entidad}.png")
    
    # Distribuir para cada estado y dirección Tony Mateo 23-eisn-2-044
    for estado, frames in frames_por_estado.items():
        if not frames:
            continue
            
        print(f"  Procesando estado: {estado}")
        
        # Para dirección derecha: usar frames originales Tony Mateo 23-eisn-2-044
        for i, frame_path in enumerate(frames):
            frame_num = i + 1
            destino = f"sprites/{entidad}/{estado}/derecha/frame{frame_num}.png"
            shutil.copy(frame_path, destino)
        
        # Para dirección izquierda: voltear horizontalmente Tony Mateo 23-eisn-2-044
        for i, frame_path in enumerate(frames):
            frame_num = i + 1
            imagen = Image.open(frame_path)
            imagen_volteada = ImageOps.mirror(imagen)
            destino = f"sprites/{entidad}/{estado}/izquierda/frame{frame_num}.png"
            imagen_volteada.save(destino)
        
        # Para dirección arriba y abajo: usar frames originales Tony Mateo 23-eisn-2-044
        for direccion in ["arriba", "abajo"]:
            for i, frame_path in enumerate(frames):
                frame_num = i + 1
                destino = f"sprites/{entidad}/{estado}/{direccion}/frame{frame_num}.png"
                shutil.copy(frame_path, destino)
    
    print(f"✓ Frames de {entidad} distribuidos correctamente.")
    return True

def crear_sprites_adicionales():
    """Crea sprites adicionales para las balas y obstáculos"""
    print("\nCreando sprites adicionales...")
    
    # Crear sprite para bala del jugador Tony Mateo 23-eisn-2-044
    bala_jugador = pygame.Surface((8, 8), pygame.SRCALPHA)
    pygame.draw.circle(bala_jugador, (30, 144, 255), (4, 4), 4)  # Azul
    pygame.image.save(bala_jugador, "sprites/bala_jugador.png")
    print("✓ Sprite de bala del jugador creado: sprites/bala_jugador.png")
    
    # Crear sprite para bala del NPC Tony Mateo 23-eisn-2-044
    bala_npc = pygame.Surface((8, 8), pygame.SRCALPHA)
    pygame.draw.circle(bala_npc, (255, 0, 0), (4, 4), 4)  
    pygame.image.save(bala_npc, "sprites/bala_npc.png")
    print("✓ Sprite de bala del NPC creado: sprites/bala_npc.png")
    
    # Crear sprite para obstáculo Tony Mateo 23-eisn-2-044
    obstaculo = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.rect(obstaculo, (139, 69, 19), (0, 0, 48, 48), border_radius=5)  
    pygame.draw.rect(obstaculo, (101, 67, 33), (2, 2, 44, 44), 2, border_radius=5)
    # Añadir textura Tony Mateo 23-eisn-2-044
    for i in range(5, 45, 8):
        for j in range(5, 45, 8):
            pygame.draw.rect(obstaculo, (101, 67, 33), (i, j, 4, 4))
    pygame.image.save(obstaculo, "sprites/obstaculo.png")
    print("✓ Sprite de obstáculo creado: sprites/obstaculo.png")
    
    print("✓ Sprites adicionales creados correctamente.")
    return True

def obtener_rutas_frames(entidad, estado):
    """Solicita al usuario las rutas de los frames para un estado específico"""
    print(f"\nIntroduce las rutas a los frames de {entidad} para el estado '{estado}' (separadas por comas, o deja vacío si no hay):")
    frames_input = input("> ")
    
    if not frames_input.strip():
        return []
        
    return [ruta.strip() for ruta in frames_input.split(",")]

def main():
    """Función principal que ejecuta todo el proceso"""
    print("=== DISTRIBUCIÓN DE SPRITES Y ANIMACIONES ===")
    
    # 1. Crear estructura de directorios Tony Mateo 23-eisn-2-044
    crear_estructura_directorios()
    
    # 2. Solicitar rutas de archivos al usuario para cada estado Tony Mateo 23-eisn-2-044
    frames_jugador = {}
    frames_npc = {}
    
    for estado in ["quieto", "moviendo", "disparando"]:
        frames_jugador[estado] = obtener_rutas_frames("jugador", estado)
        frames_npc[estado] = obtener_rutas_frames("npc", estado)
    
    # 3. Distribuir frames Tony Mateo 23-eisn-2-044
    jugador_ok = distribuir_frames_por_estado("jugador", frames_jugador)
    npc_ok = distribuir_frames_por_estado("npc", frames_npc)
    
    # 4. Crear sprites adicionales Tony Mateo 23-eisn-2-044
    adicionales_ok = crear_sprites_adicionales()
    
    # 5. Resumen Tony Mateo 23-eisn-2-044
    print("\n=== RESUMEN ===")
    if jugador_ok:
        print("✓ Frames del jugador distribuidos correctamente")
    else:
        print("⚠ Error al distribuir frames del jugador")
    
    if npc_ok:
        print("✓ Frames del NPC distribuidos correctamente")
    else:
        print("⚠ Error al distribuir frames del NPC")
    
    if adicionales_ok:
        print("✓ Sprites adicionales creados correctamente")
    else:
        print("⚠ Error al crear sprites adicionales")
    
    print("\n¡Proceso completado!")
    print("Ya puedes ejecutar tu juego con las animaciones.")
    
    # Cerrar pygame Tony Mateo 23-eisn-2-044
    pygame.quit()

if __name__ == "__main__":
    main()