import pygame


class BonusItem:
    """Represents a collectible bonus item."""

    def __init__(self, x, y, size, color, score_value, time_bonus):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.score_value = score_value
        self.time_bonus = time_bonus
        self.collected = False

    def collect(self, player):
        """Collect bonus item if player touches it."""
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            return self.score_value, self.time_bonus
        return 0, 0

    def draw(self, screen):
        """Draw the bonus item if not collected."""
        if not self.collected:
            center = self.rect.center
            radius = self.rect.width // 2
            pygame.draw.circle(screen, self.color, center, radius)