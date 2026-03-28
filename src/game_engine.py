import pygame

from src.settings import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOR,
    GRID_COLOR,
    TEXT_COLOR,
    PLAYER_COLOR,
    TILE_SIZE,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_SIZE,
)


class GameEngine:
    """Main controller for the Maze Runner game."""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.title_font = pygame.font.Font(None, 64)
        self.info_font = pygame.font.Font(None, 30)

        self.player_rect = pygame.Rect(
            PLAYER_START_X,
            PLAYER_START_Y,
            PLAYER_SIZE,
            PLAYER_SIZE
        )

    def handle_events(self):
        """Handle window close and keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game logic."""
        pass

    def draw_grid(self):
        """Draw a simple background grid."""
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (x, 0),
                (x, HEIGHT)
            )

        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, y),
                (WIDTH, y)
            )

    def draw(self):
        """Draw everything on the screen."""
        self.screen.fill(BACKGROUND_COLOR)

        self.draw_grid()

        title_surface = self.title_font.render("Maze Runner", True, TEXT_COLOR)
        info_surface = self.info_font.render(
            "First game window is working - Press ESC to quit",
            True,
            TEXT_COLOR
        )

        self.screen.blit(title_surface, (220, 30))
        self.screen.blit(info_surface, (150, 100))

        pygame.draw.rect(self.screen, PLAYER_COLOR, self.player_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()