import pygame


class Trap:
    """Represents a static trap tile."""

    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color

    def check_collision(self, player):
        """Return True if player touches the trap."""
        return self.rect.colliderect(player.rect)

    def draw(self, screen):
        """Draw the trap."""
        pygame.draw.rect(screen, self.color, self.rect)
