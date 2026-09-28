# Bomber Friends Simple

Version independiente y reducida de Bomber Friends. Mantiene tres niveles, mapas generados, cuatro tipos de enemigos, bombas, mejoras ocultas, jefe final y puntuacion. El juego dibuja sus elementos con Pygame; no requiere archivos graficos ni de audio.

## Requisitos y ejecucion

Python 3.8 o posterior y Pygame 2.x.

```bash
python -m pip install -r requirements.txt
python main.py
```

## Controles

| Tecla | Accion |
|---|---|
| Flechas o WASD | Mover |
| Espacio | Colocar bomba |
| P | Pausar |
| Enter | Confirmar o continuar |
| R (en pausa) | Reiniciar nivel |
| Escape | Reanudar desde pausa; volver al menu durante la partida; salir desde el menu |
| M (en pausa) | Volver al menu |

Las explosiones pueden activar otras bombas. Los power-ups aparecen al destruir el bloque que los oculta. Las vidas y mejoras se conservan al avanzar entre niveles.

## Pruebas

Desde esta carpeta:

```bash
python -m unittest discover tests
```

La aplicacion se organiza en siete modulos Python: entrada, juego, configuracion, actores, nivel, pantallas y utilidades. Las pruebas estan separadas en `tests/`.