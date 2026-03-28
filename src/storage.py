import json
import os


class Storage:
    """Handles loading and saving score data."""

    def __init__(self, file_path="data/highscore.json"):
        self.file_path = file_path

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
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
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
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        cleaned_scores = self._clean_scores(scores)
        data = {"top_scores": cleaned_scores}

        with open(self.file_path, "w", encoding="utf-8") as file:
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