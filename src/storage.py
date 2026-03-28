import json
import os


class Storage:
    """Handles loading and saving score and settings data."""

    def __init__(
        self,
        score_file_path="data/highscore.json",
        settings_file_path="data/settings.json"
    ):
        self.score_file_path = score_file_path
        self.settings_file_path = settings_file_path

    def _ensure_parent_folder(self, file_path):
        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

    def _clean_scores(self, scores):
        cleaned = []

        for score in scores:
            try:
                score_value = int(score)
                if score_value > 0:
                    cleaned.append(score_value)
            except (TypeError, ValueError):
                continue

        cleaned.sort(reverse=True)
        return cleaned[:10]

    def load_top_scores(self):
        """Load the top 10 scores from JSON file."""
        if not os.path.exists(self.score_file_path):
            return []

        try:
            with open(self.score_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

        if isinstance(data, dict):
            if "top_scores" in data and isinstance(data["top_scores"], list):
                return self._clean_scores(data["top_scores"])

            if "high_score" in data:
                return self._clean_scores([data["high_score"]])

        if isinstance(data, list):
            return self._clean_scores(data)

        return []

    def save_top_scores(self, scores):
        """Save the top 10 scores to JSON file."""
        self._ensure_parent_folder(self.score_file_path)

        cleaned_scores = self._clean_scores(scores)
        data = {"top_scores": cleaned_scores}

        with open(self.score_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_score(self, score):
        """Add a score and keep only the top 10."""
        if score <= 0:
            return self.load_top_scores()

        scores = self.load_top_scores()
        scores.append(int(score))
        scores = self._clean_scores(scores)
        self.save_top_scores(scores)
        return scores

    def load_high_score(self):
        """Return the best score."""
        scores = self.load_top_scores()
        return scores[0] if scores else 0

    def get_default_settings(self):
        return {
            "smart_enemy": True,
            "show_hints": True,
            "starting_lives": 3,
        }

    def _clean_settings(self, settings):
        defaults = self.get_default_settings()

        if not isinstance(settings, dict):
            return defaults

        cleaned = {
            "smart_enemy": bool(settings.get("smart_enemy", defaults["smart_enemy"])),
            "show_hints": bool(settings.get("show_hints", defaults["show_hints"])),
            "starting_lives": defaults["starting_lives"],
        }

        try:
            lives = int(settings.get("starting_lives", defaults["starting_lives"]))
        except (TypeError, ValueError):
            lives = defaults["starting_lives"]

        if lives < 1:
            lives = 1
        if lives > 5:
            lives = 5

        cleaned["starting_lives"] = lives
        return cleaned

    def load_settings(self):
        """Load saved settings from JSON file."""
        defaults = self.get_default_settings()

        if not os.path.exists(self.settings_file_path):
            return defaults

        try:
            with open(self.settings_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return defaults

        return self._clean_settings(data)

    def save_settings(self, settings):
        """Save cleaned settings to JSON file."""
        self._ensure_parent_folder(self.settings_file_path)
        cleaned = self._clean_settings(settings)

        with open(self.settings_file_path, "w", encoding="utf-8") as file:
            json.dump(cleaned, file, indent=4)