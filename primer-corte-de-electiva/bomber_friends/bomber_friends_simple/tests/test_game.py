"""Pruebas de las reglas principales del juego reducido."""

import os
from collections import defaultdict
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from actors import Bomb, Enemy, Player
from game import Game
from level import Level, MAX_GENERATION_ATTEMPTS, PLAYER_START


class GameTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game(screen=pygame.Surface((800, 600)))

    def tearDown(self):
        pygame.quit()

    def start_game(self):
        self.game.start_new_game()
        self.game.level.enemies.clear()
        return self.game

    def test_generated_levels_have_safe_start_and_center_path(self):
        for number in range(1, 4):
            level = Level(number)
            self.assertTrue(level.tilemap.walkable(*PLAYER_START))
            self.assertTrue(level._has_path(level.tilemap, (9, 6)))
            self.assertLessEqual(MAX_GENERATION_ATTEMPTS, 10)

    def test_powerup_stays_hidden_until_its_block_is_destroyed(self):
        level = Level(1)
        (x, y), kind = next(iter(level.hidden_powerups.items()))

        self.assertTrue(level.tilemap.is_block(x, y))
        self.assertFalse(level.powerups)
        self.assertTrue(level.destroy_block(x, y))
        self.assertTrue(level.tilemap.walkable(x, y))
        self.assertEqual(level.powerups[0].kind, kind)
        self.assertTrue(level.powerups[0].revealed)

    def test_player_damage_has_invulnerability_and_upgrades_are_capped(self):
        player = Player(0, 0)
        self.assertTrue(player.damage())
        self.assertFalse(player.damage())
        self.assertEqual(player.lives, 3)
        player.collect("speed")
        player.collect("life")
        self.assertEqual(player.speed, 200)
        self.assertEqual(player.lives, 4)

    def test_explosion_triggers_neighboring_bomb(self):
        game = self.start_game()
        game.level.tilemap.grid[1][3] = 0
        first = Bomb(60, 80, 2, game.player)
        second = Bomb(140, 80, 1, game.player)
        first.timer = 0
        game.bombs = [first, second]
        game.player.active_bombs = 2

        game._detonate(first)

        self.assertIsNotNone(second.chain_timer)
        game._update_bombs(0.1)
        self.assertEqual(game.bombs, [])
        self.assertEqual(len(game.explosions), 2)
        self.assertEqual(game.player.active_bombs, 0)

    def test_next_level_preserves_lives_and_upgrades(self):
        game = self.start_game()
        game.player.lives = 3
        game.player.max_bombs = 2
        game.player.bomb_range = 4
        game.player.speed = 220

        game.next_level()

        self.assertEqual(game.level_number, 2)
        self.assertEqual(game.player.lives, 3)
        self.assertEqual(game.player.max_bombs, 2)
        self.assertEqual(game.player.bomb_range, 4)
        self.assertEqual(game.player.speed, 220)

    def test_boss_and_summoned_enemies_both_gate_level_completion(self):
        level = Level(3)
        level.enemies.clear()
        level.summon_near(level.boss.x, level.boss.y)
        for _ in range(10):
            level.boss.damage()

        self.assertFalse(level.completed)
        level.enemies.clear()
        self.assertTrue(level.completed)

    def test_menu_pause_and_resume_transitions(self):
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertEqual(self.game.state, Game.PLAYING)
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        self.assertEqual(self.game.state, Game.PAUSED)
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertEqual(self.game.state, Game.PLAYING)
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.assertEqual(self.game.state, Game.PLAYING)
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m))
        self.assertEqual(self.game.state, Game.MENU)

    def test_movement_is_normalized_and_uses_axis_collision(self):
        game = self.start_game()
        keys = defaultdict(bool)
        keys[pygame.K_RIGHT] = True
        keys[pygame.K_DOWN] = True
        old_position = (game.player.x, game.player.y)

        game.update(0.1, keys)

        dx = game.player.x - old_position[0]
        dy = game.player.y - old_position[1]
        self.assertGreater(dx, 0)
        self.assertEqual(dy, 0)

    def test_player_moves_one_grid_cell_at_a_time(self):
        game = self.start_game()
        keys = defaultdict(bool)
        keys[pygame.K_RIGHT] = True
        start_x, start_y = game.player.x, game.player.y

        game.update(1.0, keys)

        self.assertEqual(game.player.x - start_x, 40)
        self.assertEqual(game.player.y, start_y)
        self.assertIsNone(game.player.grid_target)

    def test_enemy_finishes_each_move_on_a_grid_cell(self):
        level = Level(1)
        enemy = Enemy("basic", 64, 84)
        enemy.direction = (1, 0)

        enemy.update(0.5, level.tilemap, Player(500, 400))

        self.assertEqual(enemy.x, 104)
        self.assertEqual(enemy.y, 84)
        self.assertIsNone(enemy.grid_target)

    def test_game_over_can_restart(self):
        game = self.start_game()
        game.player.lives = 1
        game.player.damage()
        game.update(1 / 60, defaultdict(bool))

        self.assertEqual(game.state, Game.GAME_OVER)
        game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertEqual(game.state, Game.PLAYING)
        self.assertEqual(game.level_number, 1)
        self.assertEqual(game.score, 0)

    def test_final_level_advances_to_victory(self):
        game = self.start_game()
        game.level_number = 3

        game.next_level()

        self.assertEqual(game.state, Game.VICTORY)


if __name__ == "__main__":
    unittest.main()