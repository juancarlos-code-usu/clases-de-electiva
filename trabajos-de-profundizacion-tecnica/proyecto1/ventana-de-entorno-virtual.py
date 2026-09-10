import pygame
import sys

# 1. Inicializar Pygame
pygame.init() 

# 2. Configuraciones de la Ventana
ANCHO = 800
ALTO = 600
Dimensiones = (ANCHO, ALTO)

# Crear la ventana
pantalla = pygame.display.set_mode(Dimensiones)

# Título e Icono de la ventana
pygame.display.set_caption("Mi Ventana de Pygame")

# 3. Control de Rendimiento 
reloj = pygame.time.Clock()
FPS = 60 # Define a cuántos fotogramas por segundo correrá el juego

# Definición de colores RGB
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# 4. Bucle Principal del Juego
ejecutando = True
while ejecutando:
    
    # --- CONTROL DE EVENTOS ---
    for evento in pygame.event.get():
        # Si el usuario hace clic en la 'X' de la ventana, se cierra
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    # Limpiar la pantalla con un color de fondo 
    pantalla.fill(NEGRO)
    
    # Actualizar el contenido de la pantalla
    pygame.display.flip()
    
    # Engachar el bucle a los FPS configurados
    reloj.tick(FPS)

# 5. Salir del sistema
pygame.quit()
sys.exit()
