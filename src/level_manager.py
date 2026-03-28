class LevelManager:
    """Handles level data and level progression."""

    def __init__(self):
        self.current_level = 0

        self.levels = [
            {
                "time_limit": 45,
                "enemy_speed": 2,
                "enemy_bounds": (447, 727),
                "layout": [
                    "####################",
                    "#P.....#...........#",
                    "#.###..#..#####.##.#",
                    "#...#.....#...#....#",
                    "#.#.#####.#.#.####.#",
                    "#.#.....#.#.#......#",
                    "#.#####.#.#.######.#",
                    "#.....#...#...E.K..#",
                    "###.#.#####.######.#",
                    "#...#.....#..T...#.#",
                    "#.#######.######.#.#",
                    "#.......#....T...#.#",
                    "#.#####.##########.#",
                    "#................D.#",
                    "####################",
                ],
            },
            {
                "time_limit": 38,
                "enemy_speed": 3,
                "enemy_bounds": (447, 727),
                "layout": [
                    "####################",
                    "#P....#...........D#",
                    "#.##..#.#####.###..#",
                    "#....##.....#......#",
                    "####.#####..#.####.#",
                    "#......#....#....#.#",
                    "#.####.#.######.#..#",
                    "#.#....#...E....#..#",
                    "#.#.######.######..#",
                    "#...#....T.....##..#",
                    "###.#.########..#..#",
                    "#...#......#....#..#",
                    "#.######.#.#.####..#",
                    "#......K.#....T....#",
                    "####################",
                ],
            },
             {
                "time_limit": 32,
                "enemy_speed": 10,
                "enemy_bounds": (390, 687),
                "layout": [
                    "####################",
                    "#P......#.........D#",
                    "#.####..#.#####.##.#",
                    "#....#..#.....#....#",
                    "####.#.###...#.###.#",
                    "#....#.....#.#...#.#",
                    "#.#####..#...###.#.#",
                    "#........#.#.....#.#",
                    "#######.#.#.#####..#",
                    "#.....#.#.#...E....#",
                    "#.###.#.#.#######..#",
                    "#.#...#.#.......#..#",
                    "#.#.###.#######.#..#",
                    "#...#....K..T......#",
                    "####################",
                ],
                 },
        ]

    def reset(self):
        """Reset to the first level."""
        self.current_level = 0

    def get_current_level_data(self):
        """Return the current level dictionary."""
        return self.levels[self.current_level]

    def has_next_level(self):
        """Return True if another level exists."""
        return self.current_level < len(self.levels) - 1

    def go_to_next_level(self):
        """Move to the next level if possible."""
        if self.has_next_level():
            self.current_level += 1
            return True
        return False

    def get_level_number(self):
        """Return current level number starting from 1."""
        return self.current_level + 1

    def get_total_levels(self):
        """Return total number of levels."""
        return len(self.levels)
