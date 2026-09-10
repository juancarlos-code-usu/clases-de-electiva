import pygame
import sys

# 1. Inicializar Pygame
pygame.init() 

# 2. Configuraciones de la Ventana
ANCHO = 800
ALTO = 600
Dimensiones = (ANCHO, ALTO)

# Crear la ventana (superficie principal)
pantalla = pygame.display.set_mode(Dimensiones)

# Título e Icono de la ventana
pygame.display.set_caption("Mi Ventana de Pygame")
# Nota: Para el icono, necesitas una imagen pequeña (ej. 32x32 píxeles)
# icono = pygame.image.load("tu_icono.png")
# pygame.display.set_icon(icono)

# 3. Control de Rendimiento (FPS)
reloj = pygame.time.Clock()
FPS = 60 # Define a cuántos fotogramas por segundo correrá el juego

# Definición de colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# 4. Bucle Principal del Juego (Game Loop)
ejecutando = True
while ejecutando:
    
    # --- CONTROL DE EVENTOS ---
    for evento in pygame.event.get():
        # Si el usuario hace clic en la 'X' de la ventana, se cierra
        if evento.type == pygame.QUIT:
            ejecutando = False
            
    # --- LÓGICA DEL JUEGO ---
    # Aquí puedes actualizar las posiciones de tus personajes o variables
    
    # --- RENDERIZADO / DIBUJO ---
    # Limpiar la pantalla con un color de fondo (evita el efecto "fantasma")
    pantalla.fill(NEGRO)
    
    # (Aquí puedes dibujar tus figuras, imágenes o texto)
    
    # Actualizar el contenido de la pantalla
    pygame.display.flip()
    
    # Engachar el bucle a los FPS configurados
    reloj.tick(FPS)

# 5. Salir del sistema de forma limpia
pygame.quit()
sys.exit()
