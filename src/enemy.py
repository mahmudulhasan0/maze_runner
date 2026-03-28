import math
import pygame


class Enemy:
    """Represents a moving enemy with patrol and smart chasing behavior."""

    def __init__(self, x, y, size, color, left_bound, right_bound, speed=2, image_path=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1
        self.image = self.load_image(image_path, size)
        self.detection_range = 220

    def load_image(self, image_path, size):
        """Load and scale enemy image if available."""
        if not image_path:
            return None

        try:
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (size, size))
        except (pygame.error, FileNotFoundError):
            return None

    def check_collision(self, player):
        """Return True if enemy touches the player."""
        return self.rect.colliderect(player.rect)

    def can_move_to(self, rect, maze):
        """Check if enemy can move to a given position."""
        if rect.x < self.left_bound or rect.x > self.right_bound:
            return False

        if maze is not None and maze.is_wall(rect):
            return False

        return True

    def try_move(self, dx, dy, maze):
        """Try to move enemy; return True if movement succeeded."""
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy

        if self.can_move_to(new_rect, maze):
            self.rect = new_rect
            return True

        return False

    def patrol_update(self, maze=None):
        """Move left and right between patrol bounds."""
        new_rect = self.rect.copy()
        new_rect.x += self.speed * self.direction

        if self.can_move_to(new_rect, maze):
            self.rect = new_rect
            return

        self.direction *= -1

        new_rect = self.rect.copy()
        new_rect.x += self.speed * self.direction

        if self.can_move_to(new_rect, maze):
            self.rect = new_rect

    def smart_chase_update(self, player, maze):
        """Move toward the player using a simple chasing behavior."""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        step_x = self.speed if dx > 0 else -self.speed if dx < 0 else 0
        step_y = self.speed if dy > 0 else -self.speed if dy < 0 else 0

        moved = False

        if abs(dx) >= abs(dy):
            if step_x != 0:
                moved = self.try_move(step_x, 0, maze)
            if not moved and step_y != 0:
                moved = self.try_move(0, step_y, maze)
        else:
            if step_y != 0:
                moved = self.try_move(0, step_y, maze)
            if not moved and step_x != 0:
                moved = self.try_move(step_x, 0, maze)

        if not moved:
            self.patrol_update(maze)

    def update(self, player=None, maze=None, smart_mode=False):
        """Update enemy movement."""
        if smart_mode and player is not None and maze is not None:
            distance = math.hypot(
                player.rect.centerx - self.rect.centerx,
                player.rect.centery - self.rect.centery
            )

            if distance <= self.detection_range:
                self.smart_chase_update(player, maze)
                return

        self.patrol_update(maze)

    def draw(self, screen):
        """Draw the enemy."""
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)