import pygame


class Player:
    """Represents the player controlled square."""

    def __init__(self, x, y, size, color, speed, image_path=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = speed
        self.image = self.load_image(image_path, size)

    def load_image(self, image_path, size):
        """Load and scale player image if available."""
        if not image_path:
            return None

        try:
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (size, size))
        except (pygame.error, FileNotFoundError):
            return None

    def reset_position(self, x, y):
        """Move player back to a specific position."""
        self.rect.x = x
        self.rect.y = y

    def move(self, dx, dy, maze, screen_width, screen_height):
        """Move the player and block movement through walls."""
        if dx != 0:
            new_rect = self.rect.copy()
            new_rect.x += dx * self.speed

            if new_rect.left >= 0 and new_rect.right <= screen_width:
                if not maze.is_wall(new_rect):
                    self.rect = new_rect

        if dy != 0:
            new_rect = self.rect.copy()
            new_rect.y += dy * self.speed

            if new_rect.top >= 0 and new_rect.bottom <= screen_height:
                if not maze.is_wall(new_rect):
                    self.rect = new_rect

    def draw(self, screen):
        """Draw the player on the screen."""
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)