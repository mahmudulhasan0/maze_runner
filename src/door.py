import pygame


class Door:
    """Represents the exit door."""

    def __init__(self, x, y, size, locked_color, unlocked_color):
        self.rect = pygame.Rect(x, y, size, size)
        self.locked_color = locked_color
        self.unlocked_color = unlocked_color

    def can_exit(self, player, has_key):
        """Return True if the player reaches the door with the key."""
        return has_key and self.rect.colliderect(player.rect)

    def draw(self, screen, unlocked):
        """Draw the door in locked or unlocked state."""
        color = self.unlocked_color if unlocked else self.locked_color
        pygame.draw.rect(screen, color, self.rect)