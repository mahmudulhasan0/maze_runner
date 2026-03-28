import pygame


class KeyItem:
    """Represents the collectible key."""

    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.collected = False

    def collect(self, player):
        """Mark the key as collected if the player touches it."""
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            return True
        return False

    def draw(self, screen):
        """Draw the key if it has not been collected yet."""
        if not self.collected:
            pygame.draw.rect(screen, self.color, self.rect)