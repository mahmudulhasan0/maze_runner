import pygame


class Enemy:
    """Represents a moving enemy that patrols left and right."""

    def __init__(self, x, y, size, color, left_bound, right_bound, speed=2, image_path=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1
        self.image = self.load_image(image_path, size)

    def load_image(self, image_path, size):
        """Load and scale enemy image if available."""
        if not image_path:
            return None

        try:
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (size, size))
        except (pygame.error, FileNotFoundError):
            return None

    def update(self):
        """Move the enemy left and right between bounds."""
        self.rect.x += self.speed * self.direction

        if self.rect.x <= self.left_bound:
            self.rect.x = self.left_bound
            self.direction = 1

        if self.rect.x >= self.right_bound:
            self.rect.x = self.right_bound
            self.direction = -1

    def check_collision(self, player):
        """Return True if enemy touches the player."""
        return self.rect.colliderect(player.rect)

    def draw(self, screen):
        """Draw the enemy."""
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)