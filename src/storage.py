import json
import os


class Storage:
    """Handles loading and saving high score data."""

    def __init__(self, file_path="data/highscore.json"):
        self.file_path = file_path

    def load_high_score(self):
        """Load high score from JSON file."""
        if not os.path.exists(self.file_path):
            return 0

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("high_score", 0)
        except (json.JSONDecodeError, OSError):
            return 0

    def save_high_score(self, score):
        """Save high score to JSON file."""
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        data = {"high_score": score}

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
