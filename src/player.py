import pygame


class Player:
    """Represents the player controlled square."""

    def __init__(self, x, y, size, color, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = speed

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
        pygame.draw.rect(screen, self.color, self.rect)