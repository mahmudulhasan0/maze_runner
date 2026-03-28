import pygame

from src.settings import TILE_SIZE, WALL_COLOR, PATH_COLOR, ITEM_SIZE


class Maze:
    """Represents the maze layout and wall collision logic."""

    def __init__(self, layout):
        self.layout = layout
        self.walls = []
        self.player_start = (0, 0)
        self.key_position = (0, 0)
        self.door_position = (0, 0)

       
        self.enemy_position = (0, 0)
        self.trap_positions = []
      

        self._build_maze()

    def _build_maze(self):
        """Create wall rectangles and find important object positions."""
        self.walls.clear()

      
        self.trap_positions.clear()


        offset = (TILE_SIZE - ITEM_SIZE) // 2

        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == "#":
                    wall_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.walls.append(wall_rect)

                elif cell == "P":
                    self.player_start = (x + 5, y + 5)

                elif cell == "K":
                    self.key_position = (x + offset, y + offset)

                elif cell == "D":
                    self.door_position = (x + offset, y + offset)

                elif cell == "E":
                    self.enemy_position = (x + 7, y + 7)

                elif cell == "T":
                    self.trap_positions.append((x + offset, y + offset))

    def is_wall(self, rect):
        """Return True if the given rectangle touches any wall."""
        for wall in self.walls:
            if wall.colliderect(rect):
                return True
        return False

    def draw(self, screen):
        """Draw the maze floor and walls."""
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                floor_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, PATH_COLOR, floor_rect)

                if cell == "#":
                    pygame.draw.rect(screen, WALL_COLOR, floor_rect)