import pygame

from src.settings import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOR,
    TEXT_COLOR,
    PLAYER_COLOR,
    PLAYER_SIZE,
    PLAYER_SPEED,
    KEY_COLOR,
    DOOR_LOCKED_COLOR,
    DOOR_UNLOCKED_COLOR,
    ITEM_SIZE,
    ENEMY_COLOR,
    TRAP_COLOR,
    ENEMY_SIZE,
    TRAP_SIZE,
    TIME_LIMIT,
    KEY_SCORE,
    WIN_SCORE,
    TIME_BONUS_MULTIPLIER,
    PLAYER_IMAGE_PATH,
    ENEMY_IMAGE_PATH,
    INITIAL_LIVES,
    RESPAWN_INVULNERABLE_MS,
)
from src.player import Player
from src.maze import Maze
from src.key_item import KeyItem
from src.door import Door
from src.enemy import Enemy
from src.trap import Trap
from src.storage import Storage
from src.level_manager import LevelManager


class GameEngine:
    """Main controller for the Maze Runner game."""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.title_font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 28)
        self.message_font = pygame.font.Font(None, 40)
        self.hud_font = pygame.font.Font(None, 30)
        self.menu_font = pygame.font.Font(None, 72)
        self.menu_option_font = pygame.font.Font(None, 38)

        self.storage = Storage()
        self.top_scores = self.storage.load_top_scores()
        self.high_score = self.top_scores[0] if self.top_scores else 0

        self.score = 0
        self.time_left = TIME_LIMIT
        self.level_start_ticks = 0

        self.level_manager = LevelManager()
        self.state = "menu"

        self.game_over_reason = ""
        self.current_time_limit = TIME_LIMIT
        self.score_saved = False

        self.lives = INITIAL_LIVES
        self.last_hit_ticks = 0
        self.last_hit_reason = ""

        self.maze = None
        self.player = None
        self.key = None
        self.door = None
        self.enemy = None
        self.traps = []
        self.start_position = (0, 0)

    def refresh_scores(self):
        """Reload scores from storage."""
        self.top_scores = self.storage.load_top_scores()
        self.high_score = self.top_scores[0] if self.top_scores else 0

    def save_current_score_once(self):
        """Save score only one time per run."""
        if self.score_saved:
            return

        self.top_scores = self.storage.add_score(self.score)
        self.high_score = self.top_scores[0] if self.top_scores else 0
        self.score_saved = True

    def start_new_game(self):
        """Start the game from level 1."""
        self.level_manager.reset()
        self.score = 0
        self.lives = INITIAL_LIVES
        self.score_saved = False
        self.last_hit_ticks = 0
        self.last_hit_reason = ""
        self.load_current_level()
        self.state = "playing"

    def load_current_level(self):
        """Load the current level from LevelManager."""
        level_data = self.level_manager.get_current_level_data()

        self.current_time_limit = level_data["time_limit"]
        self.time_left = self.current_time_limit
        self.level_start_ticks = pygame.time.get_ticks()
        self.game_over_reason = ""
        self.last_hit_reason = ""
        self.last_hit_ticks = 0

        self.maze = Maze(level_data["layout"])

        start_x, start_y = self.maze.player_start
        self.start_position = (start_x, start_y)

        key_x, key_y = self.maze.key_position
        door_x, door_y = self.maze.door_position

        self.player = Player(
            start_x,
            start_y,
            PLAYER_SIZE,
            PLAYER_COLOR,
            PLAYER_SPEED,
            PLAYER_IMAGE_PATH
        )

        self.key = KeyItem(
            key_x,
            key_y,
            ITEM_SIZE,
            KEY_COLOR
        )

        self.door = Door(
            door_x,
            door_y,
            ITEM_SIZE,
            DOOR_LOCKED_COLOR,
            DOOR_UNLOCKED_COLOR
        )

        enemy_x, enemy_y = self.maze.enemy_position
        left_bound, right_bound = level_data["enemy_bounds"]

        self.enemy = Enemy(
            enemy_x,
            enemy_y,
            ENEMY_SIZE,
            ENEMY_COLOR,
            left_bound=left_bound,
            right_bound=right_bound,
            speed=level_data["enemy_speed"],
            image_path=ENEMY_IMAGE_PATH
        )

        self.traps = []
        for trap_x, trap_y in self.maze.trap_positions:
            self.traps.append(
                Trap(trap_x, trap_y, TRAP_SIZE, TRAP_COLOR)
            )

    def is_invulnerable(self):
        """Return True for a short time after taking damage."""
        if self.last_hit_ticks == 0:
            return False

        elapsed = pygame.time.get_ticks() - self.last_hit_ticks
        return elapsed < RESPAWN_INVULNERABLE_MS

    def damage_player(self, reason):
        """Reduce life, respawn player, or end the game."""
        if self.is_invulnerable():
            return

        self.lives -= 1
        self.last_hit_ticks = pygame.time.get_ticks()
        self.last_hit_reason = reason
        self.player.reset_position(self.start_position[0], self.start_position[1])

        if self.lives <= 0:
            self.game_over_reason = reason
            self.state = "game_over"
            self.save_current_score_once()

    def handle_final_win(self):
        """Finish the game after the last level."""
        self.state = "final_win"
        self.save_current_score_once()

    def handle_events(self):
        """Handle keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.state == "menu":
                    if event.key == pygame.K_s:
                        self.start_new_game()
                    elif event.key == pygame.K_h:
                        self.refresh_scores()
                        self.state = "high_score"
                    elif event.key == pygame.K_q:
                        self.running = False

                elif self.state == "high_score":
                    if event.key == pygame.K_b:
                        self.state = "menu"

                elif self.state == "level_complete":
                    if event.key == pygame.K_n:
                        if self.level_manager.go_to_next_level():
                            self.load_current_level()
                            self.state = "playing"
                    elif event.key == pygame.K_r:
                        self.start_new_game()
                    elif event.key == pygame.K_m:
                        self.state = "menu"

                elif self.state in ("game_over", "final_win"):
                    if event.key == pygame.K_r:
                        self.start_new_game()
                    elif event.key == pygame.K_m:
                        self.state = "menu"

    def update(self):
        """Update movement, timer, and game logic."""
        if self.state != "playing":
            return

        elapsed_ms = pygame.time.get_ticks() - self.level_start_ticks
        self.time_left = self.current_time_limit - (elapsed_ms / 1000)

        if self.time_left <= 0:
            self.time_left = 0
            self.game_over_reason = "Time is up!"
            self.state = "game_over"
            self.save_current_score_once()
            return

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        self.player.move(dx, dy, self.maze, WIDTH, HEIGHT)

        self.enemy.update()

        if self.enemy.check_collision(self.player):
            self.damage_player("Enemy touched you!")
            return

        for trap in self.traps:
            if trap.check_collision(self.player):
                self.damage_player("You stepped on a trap!")
                return

        if self.key.collect(self.player):
            self.score += KEY_SCORE

        if self.door.can_exit(self.player, self.key.collected):
            time_bonus = int(self.time_left) * TIME_BONUS_MULTIPLIER
            self.score += WIN_SCORE + time_bonus

            if self.level_manager.has_next_level():
                self.state = "level_complete"
            else:
                self.handle_final_win()

    def draw_top_text(self):
        """Draw title and objective text."""
        title_surface = self.title_font.render("Maze Runner", True, TEXT_COLOR)

        if self.state == "game_over":
            info_text = f"{self.game_over_reason} | Press R to restart | M for menu"
        elif self.state == "level_complete":
            info_text = "Level complete! Press N for next level | R restart | M menu"
        elif self.state == "final_win":
            info_text = "All levels complete! Press R to play again | M for menu"
        elif self.is_invulnerable() and self.lives > 0:
            info_text = f"{self.last_hit_reason}  Lives left: {self.lives}"
        elif not self.key.collected:
            info_text = "Collect the key, avoid enemy/traps, then go to the door"
        else:
            info_text = "Key collected! Go to the door | Avoid enemy/traps"

        info_surface = self.info_font.render(info_text, True, TEXT_COLOR)

        self.screen.blit(title_surface, (240, 10))
        self.screen.blit(info_surface, (60, 55))

    def draw_hud(self):
        """Draw timer, score, high score, level, and lives."""
        shown_time = max(0, int(self.time_left + 0.99))

        time_surface = self.hud_font.render(f"Time: {shown_time}", True, TEXT_COLOR)
        score_surface = self.hud_font.render(f"Score: {self.score}", True, TEXT_COLOR)
        high_score_surface = self.hud_font.render(
            f"High Score: {self.high_score}",
            True,
            TEXT_COLOR
        )
        level_surface = self.hud_font.render(
            f"Level: {self.level_manager.get_level_number()}/{self.level_manager.get_total_levels()}",
            True,
            TEXT_COLOR
        )
        lives_surface = self.hud_font.render(
            f"Lives: {self.lives}",
            True,
            TEXT_COLOR
        )

        self.screen.blit(time_surface, (20, 90))
        self.screen.blit(score_surface, (150, 90))
        self.screen.blit(high_score_surface, (300, 90))
        self.screen.blit(level_surface, (520, 90))
        self.screen.blit(lives_surface, (680, 90))

    def draw_menu(self):
        """Draw the start menu."""
        self.screen.fill(BACKGROUND_COLOR)

        title_surface = self.menu_font.render("Maze Runner", True, TEXT_COLOR)
        start_surface = self.menu_option_font.render("Press S - Start Game", True, TEXT_COLOR)
        high_surface = self.menu_option_font.render("Press H - View Top 10 Scores", True, TEXT_COLOR)
        quit_surface = self.menu_option_font.render("Press Q - Quit", True, TEXT_COLOR)

        self.screen.blit(title_surface, (220, 120))
        self.screen.blit(start_surface, (250, 260))
        self.screen.blit(high_surface, (190, 320))
        self.screen.blit(quit_surface, (290, 380))

    def draw_high_score_screen(self):
        """Draw the top 10 score screen."""
        self.screen.fill(BACKGROUND_COLOR)

        title_surface = self.menu_font.render("Top 10 Scores", True, TEXT_COLOR)
        back_surface = self.menu_option_font.render(
            "Press B - Back to Menu",
            True,
            TEXT_COLOR
        )

        self.screen.blit(title_surface, (180, 70))
        self.screen.blit(back_surface, (240, 500))

        if not self.top_scores:
            empty_surface = self.menu_option_font.render(
                "No scores yet",
                True,
                TEXT_COLOR
            )
            self.screen.blit(empty_surface, (300, 260))
            return

        start_y = 180
        line_gap = 28

        for index, score in enumerate(self.top_scores, start=1):
            score_surface = self.menu_option_font.render(
                f"{index}. {score}",
                True,
                TEXT_COLOR
            )
            self.screen.blit(score_surface, (320, start_y + (index - 1) * line_gap))

    def draw_level_complete_message(self):
        """Draw message between levels."""
        if self.state == "level_complete":
            message_surface = self.message_font.render(
                "Level Complete! Press N for next level",
                True,
                TEXT_COLOR
            )
            self.screen.blit(message_surface, (110, 560))

    def draw_final_win_message(self):
        """Draw message when all levels are done."""
        if self.state == "final_win":
            message_surface = self.message_font.render(
                "You beat all levels! Press R to restart",
                True,
                TEXT_COLOR
            )
            self.screen.blit(message_surface, (120, 560))

    def draw_game_over_message(self):
        """Draw the game over message."""
        if self.state == "game_over":
            lose_surface = self.message_font.render(
                "Game Over! Press R to restart or M for menu",
                True,
                TEXT_COLOR
            )
            self.screen.blit(lose_surface, (80, 560))

    def draw_gameplay(self):
        """Draw the gameplay scene."""
        self.screen.fill(BACKGROUND_COLOR)

        self.maze.draw(self.screen)
        self.key.draw(self.screen)
        self.door.draw(self.screen, self.key.collected)

        for trap in self.traps:
            trap.draw(self.screen)

        self.enemy.draw(self.screen)

        self.draw_top_text()
        self.draw_hud()
        self.draw_level_complete_message()
        self.draw_final_win_message()
        self.draw_game_over_message()

        if self.is_invulnerable():
            blink = (pygame.time.get_ticks() // 120) % 2 == 0
            if blink:
                self.player.draw(self.screen)
        else:
            self.player.draw(self.screen)

    def draw(self):
        """Draw the current screen."""
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "high_score":
            self.draw_high_score_screen()
        else:
            self.draw_gameplay()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()