"""Jugador, enemigos, bombas, explosiones y mejoras."""

import random

import pygame

from config import (
    BOMB_CHAIN_DELAY,
    BOMB_TIMER,
    BOSS_HEALTH,
    BOSS_POINTS,
    BOSS_SIZE,
    BOSS_SPEED,
    COLORS,
    ENEMY_STATS,
    EXPLOSION_DURATION,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    PLAYER_INVULNERABLE_TIME,
    PLAYER_LIVES,
    PLAYER_MAX_LIVES,
    PLAYER_MAX_SPEED,
    PLAYER_SIZE,
    PLAYER_SPEED,
    POWERUP_COLORS,
    TILE_SIZE,
)
from utils import move_grid_step, tile_at_pixel


class Actor:
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.active = True
        self.grid_target = None

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    @property
    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.lives = PLAYER_LIVES
        self.max_bombs = 1
        self.bomb_range = 1
        self.speed = PLAYER_SPEED
        self.active_bombs = 0
        self.invulnerable = 0.0

    def update(self, dt, direction, tilemap, bombs=()):
        dx, dy = direction
        obstacles = [bomb.rect for bomb in bombs]
        if abs(dx) >= abs(dy):
            direction = (int(dx > 0) - int(dx < 0), 0)
        else:
            direction = (0, int(dy > 0) - int(dy < 0))
        move_grid_step(self, direction, self.speed, dt, tilemap, obstacles)
        self.invulnerable = max(0.0, self.invulnerable - dt)

    def damage(self):
        if self.invulnerable > 0 or not self.active:
            return False
        self.lives -= 1
        self.invulnerable = PLAYER_INVULNERABLE_TIME
        if self.lives <= 0:
            self.active = False
        return True

    def collect(self, kind):
        if kind == "bomb":
            self.max_bombs += 1
        elif kind == "range":
            self.bomb_range += 1
        elif kind == "speed":
            self.speed = min(self.speed + 50, PLAYER_MAX_SPEED)
        elif kind == "life":
            self.lives = min(self.lives + 1, PLAYER_MAX_LIVES)

    def reset_position(self, x, y):
        self.x, self.y = float(x), float(y)
        self.grid_target = None
        self.invulnerable = 0.0
        self.active_bombs = 0

    def render(self, screen):
        if self.invulnerable and int(self.invulnerable * 10) % 2 == 0:
            return
        pygame.draw.rect(screen, COLORS["player"], self.rect, border_radius=5)


class Enemy(Actor):
    def __init__(self, kind, x, y):
        size, speed, points = ENEMY_STATS[kind]
        super().__init__(x, y, size, size)
        self.kind = kind
        self.speed = speed
        self.points = points
        self.direction = random.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        self.turn_timer = random.uniform(0.2, 1.4)
        self.chase_timer = 0.0
        self.burst_timer = 0.0
        self.burst_cooldown = 2.0

    def update(self, dt, tilemap, player):
        if self.kind == "chaser":
            self.chase_timer -= dt
            if self.chase_timer <= 0:
                self.direction = self._chase_direction(tilemap, player)
                self.chase_timer = 0.4
        elif self.kind == "fast":
            self.burst_cooldown -= dt
            if self.burst_timer > 0:
                self.burst_timer -= dt
                self.speed = ENEMY_STATS["fast"][1] * 1.5
            else:
                self.speed = ENEMY_STATS["fast"][1]
                if self.burst_cooldown <= 0 and random.random() < 0.035:
                    self.burst_timer = 0.7
                    self.burst_cooldown = 2.5
        else:
            self.turn_timer -= dt
            if self.turn_timer <= 0:
                self._choose_open_direction(tilemap)
                self.turn_timer = random.uniform(0.7, 1.8)

        old_position = (self.x, self.y)
        move_grid_step(self, self.direction, self.speed, dt, tilemap)
        if self.direction != (0, 0) and self.grid_target is None and (self.x, self.y) == old_position:
            self._choose_open_direction(tilemap)

    def _choose_open_direction(self, tilemap):
        options = list(((1, 0), (-1, 0), (0, 1), (0, -1)))
        random.shuffle(options)
        for direction in options:
            rect = self.rect.move(direction[0] * TILE_SIZE, direction[1] * TILE_SIZE)
            if not tilemap.collides(rect):
                self.direction = direction
                return
        self.direction = (0, 0)

    def _chase_direction(self, tilemap, player):
        start = tile_at_pixel(*self.center)
        goal = tile_at_pixel(*player.center)
        queue = [(start, ())]
        visited = {start}
        while queue:
            (x, y), path = queue.pop(0)
            if (x, y) == goal:
                return path[0] if path else (0, 0)
            for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                point = x + direction[0], y + direction[1]
                if point not in visited and tilemap.walkable(*point):
                    visited.add(point)
                    queue.append((point, path + (direction,)))
        self._choose_open_direction(tilemap)
        return self.direction

    def render(self, screen):
        color = COLORS["enemy"] if self.kind == "basic" else COLORS[self.kind]
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.circle(screen, COLORS["text"], (self.rect.x + 9, self.rect.y + 10), 3)
        pygame.draw.circle(screen, COLORS["text"], (self.rect.right - 9, self.rect.y + 10), 3)


class Boss(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, BOSS_SIZE, BOSS_SIZE)
        self.health = BOSS_HEALTH
        self.summon_timer = 8.0
        self.points = BOSS_POINTS

    def update(self, dt, tilemap, player, level):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(1.0, (dx * dx + dy * dy) ** 0.5)
        speed = BOSS_SPEED * (1.2 if self.health <= 5 else 1.0)
        if abs(dx) >= abs(dy):
            direction = (int(dx > 0) - int(dx < 0), 0)
        else:
            direction = (0, int(dy > 0) - int(dy < 0))
        move_grid_step(self, direction, speed, dt, tilemap)
        self.summon_timer -= dt
        if self.summon_timer <= 0:
            self.summon_timer = 2.0 if self.health <= 2 else 8.0
            level.summon_near(self.x, self.y)

    def damage(self):
        if not self.active:
            return False
        self.health -= 1
        if self.health <= 0:
            self.active = False
        return True

    def render(self, screen):
        pygame.draw.rect(screen, COLORS["boss"], self.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS["highlight"], (self.rect.x + 14, self.rect.y + 18, 14, 14))
        pygame.draw.rect(screen, COLORS["highlight"], (self.rect.right - 28, self.rect.y + 18, 14, 14))


class Bomb(Actor):
    def __init__(self, x, y, blast_range, owner):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.blast_range = blast_range
        self.owner = owner
        self.timer = BOMB_TIMER
        self.chain_timer = None
        self.cell = tile_at_pixel(x, y)

    def trigger_chain(self):
        if self.chain_timer is None:
            self.chain_timer = BOMB_CHAIN_DELAY

    def update(self, dt):
        if self.chain_timer is not None:
            self.chain_timer -= dt
            return self.chain_timer <= 0
        self.timer -= dt
        return self.timer <= 0

    def render(self, screen):
        color = (255, 110, 20) if self.timer < 1 and int(self.timer * 8) % 2 else (45, 48, 50)
        pygame.draw.circle(screen, color, self.rect.center, self.width // 2 - 3)
        pygame.draw.circle(screen, COLORS["highlight"], self.rect.center, 4)


class Explosion:
    def __init__(self, cell, blast_range, tilemap):
        self.cells = {cell}
        self.timer = EXPLOSION_DURATION
        x, y = cell
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for distance in range(1, blast_range + 1):
                point = x + dx * distance, y + dy * distance
                if tilemap.is_wall(*point):
                    break
                self.cells.add(point)
                if tilemap.is_block(*point):
                    break

    def affects(self, actor):
        return tile_at_pixel(*actor.center) in self.cells

    def update(self, dt):
        self.timer -= dt
        return self.timer > 0

    def render(self, screen):
        alpha_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(alpha_surface, (*COLORS["explosion"], 190), alpha_surface.get_rect(), border_radius=8)
        for x, y in self.cells:
            screen.blit(alpha_surface, (MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE))


class PowerUp(Actor):
    def __init__(self, x, y, kind, revealed=False):
        super().__init__(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        self.kind = kind
        self.revealed = revealed

    def render(self, screen):
        if self.revealed:
            pygame.draw.rect(screen, POWERUP_COLORS[self.kind], self.rect, border_radius=7)
            pygame.draw.circle(screen, COLORS["text"], self.rect.center, 5)