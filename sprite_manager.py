
import pygame
import os
import glob

#esta clase es para manejar los sprite (Tony Mateo 23-eisn-2-044)
class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.animations = {}
        self.current_animations = {}
        self.placeholder_sprites = self._create_placeholder_sprites()
        
  

    
    def _create_placeholder_sprites(self):
        """Crea sprites de marcador de posición hasta que se carguen las imágenes reales (Tony Mateo 23-eisn-2-044)"""
        placeholders = {}
        
        # Jugador rectángulo azul (Tony Mateo 23-eisn-2-044)
        jugador_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        jugador_surf.fill((0, 0, 255))
        placeholders['jugador'] = jugador_surf
        
        # NPC rectángulo rojo (Tony Mateo 23-eisn-2-044)
        npc_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        npc_surf.fill((255, 0, 0))
        placeholders['npc'] = npc_surf
        
        # Obstáculo rectángulo marrón (Tony Mateo 23-eisn-2-044)
        obstaculo_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        obstaculo_surf.fill((139, 69, 19))
        placeholders['obstaculo'] = obstaculo_surf
        
        # Bala del jugador círculo blanco (Tony Mateo 23-eisn-2-044)
        bala_jugador_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(bala_jugador_surf, (255, 255, 255), (5, 5), 5)
        placeholders['bala_jugador'] = bala_jugador_surf
        
        # Bala del NPC círculo blanco con borde rojo (Tony Mateo 23-eisn-2-044)
        bala_npc_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(bala_npc_surf, (255, 255, 255), (5, 5), 5)
        pygame.draw.circle(bala_npc_surf, (255, 0, 0), (5, 5), 5, 1)
        placeholders['bala_npc'] = bala_npc_surf
        
        # Moneda círculo amarillo (Tony Mateo 23-eisn-2-044)
        moneda_surf = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(moneda_surf, (255, 215, 0), (7, 7), 7)  # Color oro
        # Añadir un poco de brillo para que parezca más una moneda  (Tony Mateo 23-eisn-2-044)
        pygame.draw.circle(moneda_surf, (255, 255, 200), (4, 4), 2)  # Brillo
        placeholders['moneda'] = moneda_surf
        
        # Poción (frasco rojo) (Tony Mateo 23-eisn-2-044)
        pocion_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Cuerpo del frasco (Tony Mateo 23-eisn-2-044)
        pygame.draw.rect(pocion_surf, (255, 0, 0), pygame.Rect(4, 8, 12, 12))
        # Cuello del frasco (Tony Mateo 23-eisn-2-044)
        pygame.draw.rect(pocion_surf, (200, 200, 200), pygame.Rect(7, 3, 6, 5))
        # Tapa (Tony Mateo 23-eisn-2-044)
        pygame.draw.rect(pocion_surf, (100, 100, 100), pygame.Rect(6, 0, 8, 3))
        # Borde (Tony Mateo 23-eisn-2-044)
        pygame.draw.rect(pocion_surf, (255, 255, 255), pygame.Rect(4, 8, 12, 12), 1)
        placeholders['pocion'] = pocion_surf
        
        return placeholders
    
    def load_sprite(self, name, path):
        """Carga un sprite desde un archivo (Tony Mateo 23-eisn-2-044)"""
        try:
            sprite = pygame.image.load(path).convert_alpha()
            self.sprites[name] = sprite
            return True
        except (pygame.error, FileNotFoundError):
            print(f"Error al cargar el sprite '{name}' desde '{path}'")
            return False
    
    def load_animation(self, name, paths, frame_duration=100):
        """Carga una animación desde múltiples archivos (Tony Mateo 23-eisn-2-044)"""
        frames = []
        for path in paths:
            try:
                frame = pygame.image.load(path).convert_alpha()
                frames.append(frame)
            except (pygame.error, FileNotFoundError):
                print(f"Error al cargar el frame para animación '{name}' desde '{path}'")
                return False
        
        if frames:
            self.animations[name] = {
                'frames': frames,
                'frame_duration': frame_duration,
                'total_frames': len(frames)
            }
            return True
        return False
    
    def play_animation(self, name, entity_id):
        """Inicia la reproducción de una animación para una entidad (Tony Mateo 23-eisn-2-044)"""
        if name in self.animations:
            self.current_animations[entity_id] = {
                'name': name,
                'current_frame': 0,
                'last_update': pygame.time.get_ticks()
            }
            return True
        return False
    
    def update_animations(self):
        """Actualiza todas las animaciones activas (Tony Mateo 23-eisn-2-044)"""
        current_time = pygame.time.get_ticks()
        for entity_id, anim_data in list(self.current_animations.items()):
            anim_name = anim_data['name']
            anim = self.animations.get(anim_name)
            
            if anim and current_time - anim_data['last_update'] > anim['frame_duration']:
                anim_data['current_frame'] = (anim_data['current_frame'] + 1) % anim['total_frames']
                anim_data['last_update'] = current_time
                self.current_animations[entity_id] = anim_data
    
    def get_animation_frame(self, entity_id):
        """Obtiene el frame actual de la animación de una entidad (Tony Mateo 23-eisn-2-044)"""
        if entity_id in self.current_animations:
            anim_data = self.current_animations[entity_id]
            anim_name = anim_data['name']
            anim = self.animations.get(anim_name)
            
            if anim:
                frame_index = anim_data['current_frame']
                return anim['frames'][frame_index]
        return None
    
    def get_sprite(self, name):
        """Obtiene un sprite por su nombre, si no existe devuelve un marcador de posición (Tony Mateo 23-eisn-2-044)"""
        if name in self.sprites:
            return self.sprites[name]
        return self.placeholder_sprites.get(name)
    
    def load_all_sprites_from_directory(self, directory):
        """Carga todos los sprites desde un directorio y sus subdirectorios (Tony Mateo 23-eisn-2-044)"""
        if not os.path.exists(directory):
            print(f"El directorio de sprites '{directory}' no existe.")
            return False
        
        # Cargar sprites individuales (archivos en la raíz) (Tony Mateo 23-eisn-2-044)
        loaded = 0
        for filename in os.listdir(directory):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                path = os.path.join(directory, filename)
                if os.path.isfile(path):
                    name = os.path.splitext(filename)[0]
                    if self.load_sprite(name, path):
                        loaded += 1
                        print(f"Sprite cargado: {name}")
        
        return loaded
    
    def load_all_animations(self):
        """Carga todas las animaciones desde la estructura de directorios preparada (Tony Mateo 23-eisn-2-044)"""
        if not os.path.exists('sprites'):
            print("El directorio 'sprites' no existe.")
            return False
            
        # Definir entidades, estados y direcciones
        entidades = ['jugador', 'npc']
        estados = ['quieto', 'moviendo', 'disparando']
        direcciones = ['derecha', 'izquierda', 'arriba', 'abajo']
        
        animations_loaded = 0
        
        # Recorrer la estructura y cargar las animaciones (Tony Mateo 23-eisn-2-044)
        for entidad in entidades:
            for estado in estados:
                for direccion in direcciones:
                    # Ruta al directorio de la animación (Tony Mateo 23-eisn-2-044)
                    anim_dir = f"sprites/{entidad}/{estado}/{direccion}"
                    
                    if not os.path.exists(anim_dir):
                        continue
                        
                    # Buscar frames por orden numérico (Tony Mateo 23-eisn-2-044)
                    frames = sorted(glob.glob(os.path.join(anim_dir, "frame*.png")))
                    
                    if not frames:
                        continue
                        
                    # Determinar duración según el estado (Tony Mateo 23-eisn-2-044)
                    if estado == "quieto":
                        duracion = 300  
                    elif estado == "disparando":
                        duracion = 100  
                    else:
                        duracion = 150  # Velocidad estándar para movimiento (Tony Mateo 23-eisn-2-044)
                    
                    # Nombre de la animación: entidad_estado_direccion (Tony Mateo 23-eisn-2-044)
                    anim_name = f"{entidad}_{estado}_{direccion}"
                    
                    # Cargar la animación (Tony Mateo 23-eisn-2-044)
                    if self.load_animation(anim_name, frames, duracion):
                        animations_loaded += 1
                        print(f"Animación cargada: {anim_name}")
        
        print(f"Total de animaciones cargadas: {animations_loaded}")
        
        # Si no se cargaron animaciones, crear algunas de respaldo con los sprites básicos (Tony Mateo 23-eisn-2-044)
        if animations_loaded == 0:
            print("No se encontraron animaciones, creando respaldos...")
            self.create_fallback_animations()
            
        return animations_loaded > 0
    
    def create_fallback_animations(self):
        """Crea animaciones de respaldo si no se encuentran en la estructura de directorios (Tony Mateo 23-eisn-2-044)"""
        # Verificar si existen sprites para jugador y NPC (Tony Mateo 23-eisn-2-044)
        entidades = ['jugador', 'npc']
        estados = ['quieto', 'moviendo', 'disparando']
        direcciones = ['derecha', 'izquierda', 'arriba', 'abajo']
        
        for entidad in entidades:
            sprite = self.get_sprite(entidad)
            if sprite:
                # Crear frames simples para la animación (Tony Mateo 23-eisn-2-044)
                frames = []
                temp_paths = []
                
                # Crear 4 versiones ligeramente diferentes para simular animación (Tony Mateo 23-eisn-2-044)
                for i in range(4):
                    frame = sprite.copy()
                    # Escalar ligeramente diferente para simular movimiento (Tony Mateo 23-eisn-2-044)
                    escala = 0.95 + (i * 0.02)
                    nuevo_ancho = int(frame.get_width() * escala)
                    nuevo_alto = int(frame.get_height() * escala)
                    
                    # Evitar que se haga muy pequeño (Tony Mateo 23-eisn-2-044)
                    if nuevo_ancho < 10:
                        nuevo_ancho = 10
                    if nuevo_alto < 10:
                        nuevo_alto = 10
                    
                    frame = pygame.transform.scale(frame, (nuevo_ancho, nuevo_alto))
                    temp_path = f"temp_{entidad}_frame_{i}.png"
                    pygame.image.save(frame, temp_path)
                    frames.append(frame)
                    temp_paths.append(temp_path)
                
                # Crear animaciones para cada estado y dirección (Tony Mateo 23-eisn-2-044)
                for estado in estados:
                    duracion = 300 if estado == "quieto" else 150
                    for direccion in direcciones:
                        anim_name = f"{entidad}_{estado}_{direccion}"
                        self.animations[anim_name] = {
                            'frames': frames,
                            'frame_duration': duracion,
                            'total_frames': len(frames)
                        }
                
                # Limpiar archivos temporales
                for path in temp_paths:
                    if os.path.exists(path):
                        os.remove(path)
        
        print("Animaciones de respaldo creadas correctamente.")