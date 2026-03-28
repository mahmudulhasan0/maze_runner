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
)
from src.player import Player
from src.maze import Maze


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

        self.layout = [
            "####################",
            "#P.....#...........#",
            "#.###..#..#####.##.#",
            "#...#.....#...#....#",
            "#.#.#####.#.#.####.#",
            "#.#.....#.#.#......#",
            "#.#####.#.#.######.#",
            "#.....#...#........#",
            "###.#.#####.######.#",
            "#...#.....#......#.#",
            "#.#######.######.#.#",
            "#.......#........#.#",
            "#.#####.##########.#",
            "#..................#",
            "####################",
        ]

        self.maze = Maze(self.layout)

        start_x, start_y = self.maze.player_start
        self.player = Player(
            start_x,
            start_y,
            PLAYER_SIZE,
            PLAYER_COLOR,
            PLAYER_SPEED
        )

    def handle_events(self):
        """Handle close button and ESC key."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game logic and player movement."""
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

    def draw(self):
        """Draw maze, text, and player."""
        self.screen.fill(BACKGROUND_COLOR)

        self.maze.draw(self.screen)

        title_surface = self.title_font.render("Maze Runner", True, TEXT_COLOR)
        info_surface = self.info_font.render(
            "Walls are active | Move with Arrow Keys or WASD | ESC to quit",
            True,
            TEXT_COLOR
        )

        self.screen.blit(title_surface, (240, 10))
        self.screen.blit(info_surface, (80, 55))

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