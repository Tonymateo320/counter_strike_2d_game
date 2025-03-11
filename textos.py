import pygame
# Esta clase es para que cuando se el jugador le de un tiro al NPC, para que se pueda 
# visualizar la cantodad de vida que le quita.  (Tony Mateo 23-eisn-2-044)
class DamegeText:  
    def __init__(self, x, y, valor, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.valor = valor
        self.vida = 30 
        self.color = color
        self.velocidad_y = -1  
        self.fuente = pygame.font.SysFont(None, 24)
        self.texto = self.fuente.render(str(valor), True, self.color)
    
    # Es para ir actualizandonse la vida o se cada ves que le peque un tiro le va restando vida
    def actualizar(self):
        self.vida -= 1
        self.y += self.velocidad_y
        return self.vida > 0
    
    def dibujar(self, pantalla):
        # Hacer que el texto desaparezca gradualmente (Tony Mateo 23-eisn-2-044)
        alpha = int(255 * (self.vida / 30))
        texto_con_alpha = self.texto.copy()
        texto_con_alpha.set_alpha(alpha)
        pantalla.blit(texto_con_alpha, (self.x, self.y))
        