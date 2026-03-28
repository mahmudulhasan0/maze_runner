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
)
from src.player import Player
from src.maze import Maze
from src.key_item import KeyItem
from src.door import Door


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

        self.layout = [
            "####################",
            "#P.....#...........#",
            "#.###..#..#####.##.#",
            "#...#.....#...#....#",
            "#.#.#####.#.#.####.#",
            "#.#.....#.#.#......#",
            "#.#####.#.#.######.#",
            "#.....#...#.....K..#",
            "###.#.#####.######.#",
            "#...#.....#......#.#",
            "#.#######.######.#.#",
            "#.......#........#.#",
            "#.#####.##########.#",
            "#................D.#",
            "####################",
        ]

        self.game_won = False
        self.setup_level()

    def setup_level(self):
        """Create maze, player, key, and door."""
        self.maze = Maze(self.layout)

        start_x, start_y = self.maze.player_start
        key_x, key_y = self.maze.key_position
        door_x, door_y = self.maze.door_position

        self.player = Player(
            start_x,
            start_y,
            PLAYER_SIZE,
            PLAYER_COLOR,
            PLAYER_SPEED
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

        self.game_won = False

    def handle_events(self):
        """Handle close button, ESC, and restart."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_r and self.game_won:
                    self.setup_level()

    def update(self):
        """Update movement, key collection, and win condition."""
        if self.game_won:
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

        if self.key.collect(self.player):
            pass

        if self.door.can_exit(self.player, self.key.collected):
            self.game_won = True

    def draw_top_text(self):
        """Draw the title and current objective text."""
        title_surface = self.title_font.render("Maze Runner", True, TEXT_COLOR)

        if not self.key.collected:
            info_text = "Collect the key, then go to the door | Move: Arrows/WASD"
        else:
            info_text = "Key collected! Go to the door | Press ESC to quit"

        info_surface = self.info_font.render(info_text, True, TEXT_COLOR)

        self.screen.blit(title_surface, (240, 10))
        self.screen.blit(info_surface, (70, 55))

    def draw_win_message(self):
        """Draw the win message."""
        if self.game_won:
            win_surface = self.message_font.render(
                "You Win! Press R to restart or ESC to quit",
                True,
                TEXT_COLOR
            )
            self.screen.blit(win_surface, (120, 560))

    def draw(self):
        """Draw maze, key, door, text, and player."""
        self.screen.fill(BACKGROUND_COLOR)

        self.maze.draw(self.screen)
        self.key.draw(self.screen)
        self.door.draw(self.screen, self.key.collected)

        self.draw_top_text()
        self.draw_win_message()

        self.player.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()