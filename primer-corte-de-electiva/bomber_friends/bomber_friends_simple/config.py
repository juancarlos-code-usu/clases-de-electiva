"""Configuracion compacta de Bomber Friends."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "BOMBER FRIENDS"

TILE_SIZE = 40
MAP_WIDTH = 19
MAP_HEIGHT = 13
MAP_OFFSET_X = 20
MAP_OFFSET_Y = 40

PLAYER_SIZE = 32
PLAYER_SPEED = 150.0
PLAYER_LIVES = 4
PLAYER_MAX_LIVES = 7
PLAYER_INVULNERABLE_TIME = 2.0
PLAYER_MAX_SPEED = 300.0

BOMB_TIMER = 2.5
BOMB_CHAIN_DELAY = 0.1
EXPLOSION_DURATION = 0.5
POWERUP_DROP_CHANCE = 0.30

LEVELS = (
    {
        "name": "Una nueva exploracion",
        "blocks": 0.40,
        "enemies": {"basic": 4, "fast": 0, "chaser": 0},
        "powerups": ("bomb", "range"),
        "boss": False,
    },
    {
        "name": "Explosion mania",
        "blocks": 0.50,
        "enemies": {"basic": 1, "fast": 2, "chaser": 2},
        "powerups": ("speed", "bomb", "range"),
        "boss": False,
    },
    {
        "name": "El jefe final",
        "blocks": 0.30,
        "enemies": {"basic": 1, "fast": 0, "chaser": 0},
        "powerups": ("life", "bomb", "range", "speed"),
        "boss": True,
    },
)

ENEMY_STATS = {
    "basic": (32, 80.0, 100),
    "fast": (32, 120.0, 200),
    "chaser": (32, 100.0, 300),
}
BOSS_SIZE = 80
BOSS_SPEED = 60.0
BOSS_HEALTH = 10
BOSS_POINTS = 1000

POWERUP_COLORS = {
    "bomb": (50, 50, 50),
    "range": (255, 130, 0),
    "speed": (0, 100, 255),
    "life": (220, 40, 60),
}

COLORS = {
    "background": (15, 18, 25),
    "floor": (26, 31, 39),
    "wall": (105, 118, 128),
    "block": (130, 76, 45),
    "player": (40, 145, 230),
    "enemy": (205, 60, 65),
    "fast": (240, 135, 30),
    "chaser": (160, 70, 165),
    "boss": (120, 30, 38),
    "text": (242, 242, 235),
    "highlight": (255, 212, 75),
    "explosion": (255, 185, 35),
}