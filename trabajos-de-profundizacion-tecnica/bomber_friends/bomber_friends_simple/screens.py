"""Dibujo de menu, HUD y pantallas de estado."""

import pygame

from config import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


class Screens:
    def __init__(self):
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 26)

    def _center(self, screen, text, y, color=None, font=None):
        image = (font or self.font).render(text, True, color or COLORS["text"])
        screen.blit(image, image.get_rect(center=(screen.get_width() // 2, y)))

    def menu(self, screen, instructions=False):
        screen.fill(COLORS["background"])
        self._center(screen, TITLE, 150, COLORS["highlight"], self.title_font)
        if instructions:
            lines = (
                "Flechas o WASD: mover",
                "Espacio: colocar bomba",
                "P: pausar    Escape: volver al menu",
                "Enter o I: volver",
            )
            for index, line in enumerate(lines):
                self._center(screen, line, 275 + index * 48, font=self.small_font)
            return
        self._center(screen, "Enter: jugar", 300)
        self._center(screen, "I: instrucciones", 355)
        self._center(screen, "Escape: salir", 410, font=self.small_font)

    def hud(self, screen, level, player, score):
        pygame.draw.rect(screen, (20, 23, 29), (0, 0, SCREEN_WIDTH, 38))
        values = (
            f"Nivel {level.number}/3",
            f"Vidas {player.lives}",
            f"Bombas {player.max_bombs}",
            f"Alcance {player.bomb_range}",
            f"Puntos {score}",
        )
        x_positions = (12, 155, 270, 420, 575)
        for text, x in zip(values, x_positions):
            image = self.small_font.render(text, True, COLORS["text"])
            screen.blit(image, (x, 9))

    def overlay(self, screen, state, score, level_number):
        screen.fill(COLORS["background"])
        titles = {
            "paused": ("PAUSA", "Enter/Escape: continuar    R: reiniciar    M: menu"),
            "level_complete": (f"NIVEL {level_number} COMPLETADO", "Enter: continuar"),
            "game_over": ("GAME OVER", f"Puntuacion: {score}    Enter: reintentar    Escape: menu"),
            "victory": ("VICTORIA", f"Puntuacion: {score}    Enter: jugar de nuevo    Escape: menu"),
        }
        title, message = titles[state]
        self._center(screen, title, SCREEN_HEIGHT // 2 - 45, COLORS["highlight"], self.title_font)
        self._center(screen, message, SCREEN_HEIGHT // 2 + 25, font=self.small_font)
