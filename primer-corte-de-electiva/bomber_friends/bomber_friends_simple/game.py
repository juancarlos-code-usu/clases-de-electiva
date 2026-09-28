"""Bucle principal y transiciones unicas del juego."""

import pygame

from actors import Bomb, Explosion, Player
from config import FPS, MAP_OFFSET_X, MAP_OFFSET_Y, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, TITLE
from level import Level
from screens import Screens
from utils import movement_from_keys, tile_at_pixel


class Game:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    VICTORY = "victory"

    def __init__(self, screen=None):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = screen or pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.screens = Screens()
        self.state = self.MENU
        self.instructions = False
        self.level_number = 1
        self.level = None
        self.player = None
        self.score = 0
        self.bombs = []
        self.explosions = []
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.1)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.render()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self.state == self.MENU:
            if self.instructions:
                if key in (pygame.K_RETURN, pygame.K_i, pygame.K_ESCAPE):
                    self.instructions = False
            elif key == pygame.K_RETURN:
                self.start_new_game()
            elif key == pygame.K_i:
                self.instructions = True
            elif key == pygame.K_ESCAPE:
                self.running = False
        elif self.state == self.PLAYING:
            if key == pygame.K_p:
                self.state = self.PAUSED
            elif key == pygame.K_ESCAPE:
                self.state = self.MENU
            elif key == pygame.K_SPACE:
                self.place_bomb()
        elif self.state == self.PAUSED:
            if key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = self.PLAYING
            elif key == pygame.K_r:
                self.restart_level()
            elif key == pygame.K_m:
                self.state = self.MENU
        elif self.state == self.LEVEL_COMPLETE and key == pygame.K_RETURN:
            self.next_level()
        elif self.state in (self.GAME_OVER, self.VICTORY):
            if key == pygame.K_RETURN:
                self.start_new_game()
            elif key == pygame.K_ESCAPE:
                self.state = self.MENU

    def start_new_game(self):
        self.level_number = 1
        self.score = 0
        self.player = None
        self.bombs.clear()
        self.explosions.clear()
        self._start_level(preserve_player=False)

    def _start_level(self, preserve_player):
        self.level = Level(self.level_number)
        x, y = Level.start_position()
        if self.player is None or not preserve_player:
            self.player = Player(x, y)
        else:
            self.player.reset_position(x, y)
        self.bombs.clear()
        self.explosions.clear()
        self.state = self.PLAYING

    def restart_level(self):
        self.player = Player(*Level.start_position())
        self._start_level(preserve_player=True)

    def next_level(self):
        if self.level_number >= 3:
            self.state = self.VICTORY
            return
        self.level_number += 1
        self._start_level(preserve_player=True)

    def place_bomb(self):
        if self.level is None or self.player.active_bombs >= self.player.max_bombs:
            return False
        cell = tile_at_pixel(*self.player.center)
        if not self.level.tilemap.walkable(*cell) or any(bomb.cell == cell for bomb in self.bombs):
            return False
        x = MAP_OFFSET_X + cell[0] * TILE_SIZE
        y = MAP_OFFSET_Y + cell[1] * TILE_SIZE
        self.bombs.append(Bomb(x, y, self.player.bomb_range, self.player))
        self.player.active_bombs += 1
        return True

    def update(self, dt, keys=None):
        if self.state != self.PLAYING:
            return
        keys = pygame.key.get_pressed() if keys is None else keys
        self.player.update(dt, movement_from_keys(keys), self.level.tilemap, self.bombs)
        self.level.update(dt, self.player)
        self.score += self.level.take_score()
        self._update_bombs(dt)
        self.explosions = [explosion for explosion in self.explosions if explosion.update(dt)]
        if not self.player.active:
            self.state = self.GAME_OVER
        elif self.level.completed:
            self.state = self.LEVEL_COMPLETE

    def _update_bombs(self, dt):
        for bomb in self.bombs[:]:
            if bomb.update(dt):
                self._detonate(bomb)

    def _detonate(self, bomb):
        if bomb not in self.bombs:
            return
        explosion = Explosion(bomb.cell, bomb.blast_range, self.level.tilemap)
        self.bombs.remove(bomb)
        bomb.owner.active_bombs = max(0, bomb.owner.active_bombs - 1)
        self.explosions.append(explosion)
        for x, y in explosion.cells:
            if self.level.destroy_block(x, y):
                self.score += self.level.take_score()
        for other in self.bombs:
            if other.cell in explosion.cells:
                other.trigger_chain()
        if explosion.affects(self.player):
            self.player.damage()
        for enemy in self.level.enemies:
            if enemy.active and explosion.affects(enemy):
                enemy.active = False
                self.score += enemy.points
        boss = self.level.boss
        if boss and boss.active and explosion.affects(boss) and boss.damage() and not boss.active:
            self.score += boss.points
        self.level.enemies = [enemy for enemy in self.level.enemies if enemy.active]

    def render(self):
        if self.state == self.MENU:
            self.screens.menu(self.screen, self.instructions)
        elif self.state == self.PLAYING:
            self.screen.fill((15, 18, 25))
            self.level.render(self.screen, self.player)
            for bomb in self.bombs:
                bomb.render(self.screen)
            for explosion in self.explosions:
                explosion.render(self.screen)
            self.screens.hud(self.screen, self.level, self.player, self.score)
        else:
            self.screens.overlay(self.screen, self.state, self.score, self.level_number)
        if pygame.display.get_surface() is self.screen:
            pygame.display.flip()