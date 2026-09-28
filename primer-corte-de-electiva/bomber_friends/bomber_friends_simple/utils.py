"""Utilidades pequeñas compartidas por el juego."""

from math import hypot

import pygame

from config import TILE_SIZE


def movement_from_keys(keys):
    """Devuelve una direccion normalizada a partir de las teclas pulsadas."""
    x = float(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - float(
        keys[pygame.K_LEFT] or keys[pygame.K_a]
    )
    y = float(keys[pygame.K_DOWN] or keys[pygame.K_s]) - float(
        keys[pygame.K_UP] or keys[pygame.K_w]
    )
    length = hypot(x, y)
    return (x / length, y / length) if length else (0.0, 0.0)


def move_with_collision(actor, dx, dy, tilemap, obstacles=()):
    """Mueve por ejes para permitir deslizarse junto a las paredes."""
    original = actor.rect.copy()
    for axis, amount in (("x", dx), ("y", dy)):
        if not amount:
            continue
        setattr(actor, axis, getattr(actor, axis) + amount)
        if tilemap.collides(actor.rect):
            setattr(actor, axis, getattr(actor, axis) - amount)
        else:
            for obstacle in obstacles:
                if actor.rect.colliderect(obstacle) and not original.colliderect(obstacle):
                    setattr(actor, axis, getattr(actor, axis) - amount)
                    break


def move_grid_step(actor, direction, speed, dt, tilemap, obstacles=()):
    """Avanza entre casillas, completando cada tramo antes de girar."""
    target = getattr(actor, "grid_target", None)
    if target is None:
        dx, dy = direction
        if not (dx or dy):
            return
        target = (actor.x + dx * TILE_SIZE, actor.y + dy * TILE_SIZE)
        destination = actor.rect.move(dx * TILE_SIZE, dy * TILE_SIZE)
        if tilemap.collides(destination) or any(destination.colliderect(obstacle) for obstacle in obstacles):
            return
        actor.grid_target = target

    target_x, target_y = target
    remaining_x = target_x - actor.x
    remaining_y = target_y - actor.y
    distance = abs(remaining_x) + abs(remaining_y)
    travel = min(speed * dt, distance)
    if remaining_x:
        actor.x += (1 if remaining_x > 0 else -1) * travel
    else:
        actor.y += (1 if remaining_y > 0 else -1) * travel
    if travel >= distance:
        actor.x, actor.y = target
        actor.grid_target = None


def tile_at_pixel(x, y):
    from config import MAP_OFFSET_X, MAP_OFFSET_Y, TILE_SIZE

    return (
        int((x - MAP_OFFSET_X) // TILE_SIZE),
        int((y - MAP_OFFSET_Y) // TILE_SIZE),
    )
