"""Mapa, generacion y estado de un nivel."""

from collections import deque
import random

import pygame

from actors import Boss, Enemy, PowerUp
from config import (
    COLORS,
    LEVELS,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    POWERUP_DROP_CHANCE,
    TILE_SIZE,
)

EMPTY = 0
WALL = 1
BLOCK = 2
MAX_GENERATION_ATTEMPTS = 10
PLAYER_START = (1, 1)


class TileMap:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    def is_wall(self, x, y):
        return not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT) or self.grid[y][x] == WALL

    def is_block(self, x, y):
        return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and self.grid[y][x] == BLOCK

    def walkable(self, x, y):
        return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and self.grid[y][x] == EMPTY

    def collides(self, rect):
        left = (rect.left - MAP_OFFSET_X) // TILE_SIZE
        right = (rect.right - 1 - MAP_OFFSET_X) // TILE_SIZE
        top = (rect.top - MAP_OFFSET_Y) // TILE_SIZE
        bottom = (rect.bottom - 1 - MAP_OFFSET_Y) // TILE_SIZE
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if self.is_wall(x, y) or self.is_block(x, y):
                    tile = pygame.Rect(
                        MAP_OFFSET_X + x * TILE_SIZE,
                        MAP_OFFSET_Y + y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE,
                    )
                    if rect.colliderect(tile):
                        return True
        return False

    def destroy_block(self, x, y):
        if not self.is_block(x, y):
            return False
        self.grid[y][x] = EMPTY
        return True

    def render(self, screen):
        for y, row in enumerate(self.grid):
            for x, kind in enumerate(row):
                rect = pygame.Rect(
                    MAP_OFFSET_X + x * TILE_SIZE,
                    MAP_OFFSET_Y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                color = COLORS["wall"] if kind == WALL else COLORS["block"] if kind == BLOCK else COLORS["floor"]
                pygame.draw.rect(screen, color, rect)
                if kind != EMPTY:
                    pygame.draw.rect(screen, (35, 38, 43), rect, 2)


class Level:
    def __init__(self, number):
        if not 1 <= number <= len(LEVELS):
            raise ValueError(f"Nivel invalido: {number}")
        self.number = number
        self.settings = LEVELS[number - 1]
        self.tilemap = self._generate_map()
        self.enemies = []
        self.boss = None
        self.powerups = []
        self.hidden_powerups = {}
        self._score = 0
        self._place_powerups()
        self._place_boss()
        self._place_enemies()

    @staticmethod
    def start_position():
        return (
            MAP_OFFSET_X + PLAYER_START[0] * TILE_SIZE + 4,
            MAP_OFFSET_Y + PLAYER_START[1] * TILE_SIZE + 4,
        )

    def _generate_map(self):
        for _ in range(MAX_GENERATION_ATTEMPTS):
            tilemap = self._make_map(self.settings["blocks"])
            if self._has_path(tilemap, (MAP_WIDTH // 2, MAP_HEIGHT // 2)):
                return tilemap

        tilemap = self._make_map(0.0)
        for x in range(PLAYER_START[0], MAP_WIDTH // 2 + 1):
            tilemap.grid[PLAYER_START[1]][x] = EMPTY
        for y in range(PLAYER_START[1], MAP_HEIGHT // 2 + 1):
            tilemap.grid[y][MAP_WIDTH // 2] = EMPTY
        return tilemap

    def _make_map(self, block_chance):
        tilemap = TileMap()
        for x in range(MAP_WIDTH):
            tilemap.grid[0][x] = WALL
            tilemap.grid[-1][x] = WALL
        for y in range(MAP_HEIGHT):
            tilemap.grid[y][0] = WALL
            tilemap.grid[y][-1] = WALL
        for y in range(2, MAP_HEIGHT - 2, 2):
            for x in range(2, MAP_WIDTH - 2, 2):
                tilemap.grid[y][x] = BLOCK
        for y in range(1, MAP_HEIGHT - 1):
            for x in range(1, MAP_WIDTH - 1):
                if tilemap.grid[y][x] == EMPTY and random.random() < block_chance:
                    tilemap.grid[y][x] = BLOCK
        for x, y in (PLAYER_START, (2, 1), (1, 2)):
            tilemap.grid[y][x] = EMPTY
        if self.settings["boss"]:
            self._clear_boss_area(tilemap)
        return tilemap

    @staticmethod
    def _clear_boss_area(tilemap):
        center_x, center_y = MAP_WIDTH // 2, MAP_HEIGHT // 2
        for y in range(center_y - 1, center_y + 2):
            for x in range(center_x - 1, center_x + 2):
                if tilemap.grid[y][x] != WALL:
                    tilemap.grid[y][x] = EMPTY

    @staticmethod
    def _has_path(tilemap, goal):
        queue = deque([PLAYER_START])
        visited = {PLAYER_START}
        while queue:
            point = queue.popleft()
            if point == goal:
                return True
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                neighbor = point[0] + dx, point[1] + dy
                if neighbor not in visited and tilemap.walkable(*neighbor):
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

    def _place_powerups(self):
        blocks = [
            (x, y)
            for y in range(1, MAP_HEIGHT - 1)
            for x in range(1, MAP_WIDTH - 1)
            if self.tilemap.is_block(x, y)
        ]
        random.shuffle(blocks)
        for kind in self.settings["powerups"]:
            if not blocks:
                break
            self.hidden_powerups[blocks.pop()] = kind
        for point in blocks:
            if random.random() < POWERUP_DROP_CHANCE:
                self.hidden_powerups[point] = random.choice(("bomb", "range", "speed", "life"))

    def _place_boss(self):
        if not self.settings["boss"]:
            return
        center_x, center_y = MAP_WIDTH // 2, MAP_HEIGHT // 2
        self._clear_boss_area(self.tilemap)
        x = MAP_OFFSET_X + center_x * TILE_SIZE - 20
        y = MAP_OFFSET_Y + center_y * TILE_SIZE - 20
        self.boss = Boss(x, y)

    def _place_enemies(self):
        candidates = [
            (x, y)
            for y in range(2, MAP_HEIGHT - 2)
            for x in range(2, MAP_WIDTH - 2)
            if self.tilemap.walkable(x, y) and (x > 3 or y > 3)
        ]
        random.shuffle(candidates)
        for kind, amount in self.settings["enemies"].items():
            for _ in range(amount):
                if not candidates:
                    return
                x, y = candidates.pop()
                self.enemies.append(
                    Enemy(kind, MAP_OFFSET_X + x * TILE_SIZE + 4, MAP_OFFSET_Y + y * TILE_SIZE + 4)
                )

    def destroy_block(self, x, y):
        if not self.tilemap.destroy_block(x, y):
            return False
        kind = self.hidden_powerups.pop((x, y), None)
        if kind:
            self.powerups.append(
                PowerUp(MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE, kind, True)
            )
        self._score += 10
        return True

    def take_score(self):
        score, self._score = self._score, 0
        return score

    def summon_near(self, x, y):
        center = (int((x - MAP_OFFSET_X) // TILE_SIZE), int((y - MAP_OFFSET_Y) // TILE_SIZE))
        candidates = [
            (cx, cy)
            for cy in range(1, MAP_HEIGHT - 1)
            for cx in range(1, MAP_WIDTH - 1)
            if self.tilemap.walkable(cx, cy)
            and abs(cx - center[0]) + abs(cy - center[1]) <= 4
        ]
        if candidates:
            cx, cy = random.choice(candidates)
            self.enemies.append(
                Enemy("basic", MAP_OFFSET_X + cx * TILE_SIZE + 4, MAP_OFFSET_Y + cy * TILE_SIZE + 4)
            )

    def update(self, dt, player):
        for enemy in self.enemies:
            if enemy.active:
                enemy.update(dt, self.tilemap, player)
                if enemy.rect.colliderect(player.rect):
                    player.damage()
        if self.boss and self.boss.active:
            self.boss.update(dt, self.tilemap, player, self)
            if self.boss.rect.colliderect(player.rect):
                player.damage()
        for powerup in self.powerups:
            if powerup.active and powerup.revealed and player.rect.colliderect(powerup.rect):
                player.collect(powerup.kind)
                powerup.active = False
                self._score += 50
        self.enemies = [enemy for enemy in self.enemies if enemy.active]

    @property
    def completed(self):
        return not self.enemies and (self.boss is None or not self.boss.active)

    def render(self, screen, player):
        self.tilemap.render(screen)
        for powerup in self.powerups:
            if powerup.active:
                powerup.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)
        if self.boss and self.boss.active:
            self.boss.render(screen)
        player.render(screen)