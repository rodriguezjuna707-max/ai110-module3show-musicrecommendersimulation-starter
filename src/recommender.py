from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# Point values awarded per feature.
# Genre and mood use binary (exact) matching.
# Numeric features use proximity: points × (1 − |song_value − user_value|).
# Maximum possible score = 1.0 + 1.0 + 2.0 + 0.6 + 0.25 + 0.15 = 5.0
POINTS = {
    "genre":        1.00,   # strongest signal — hard stylistic boundary
    "mood":         1.00,   # emotional intent — slightly less rigid than genre
    "energy":       2.00,   # widest spread in catalog (0.28–0.97), most discriminating
    "valence":      0.60,   # secondary emotional coloring
    "danceability": 0.25,   # minor refinement
    "acousticness": 0.15,   # minor refinement
}
MAX_SCORE = sum(POINTS.values())  # 5.0


def load_songs(csv_path: str) -> List[Dict]:
    """Parse songs.csv and return a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (max 5.0) and return (score, reasons list)."""
    reasons: List[str] = []

    # --- Categorical features (binary match) ---
    genre_pts = POINTS["genre"] if song["genre"] == user_prefs.get("genre") else 0.0
    if genre_pts:
        reasons.append(f"genre match (+{genre_pts:.1f})")

    mood_pts = POINTS["mood"] if song["mood"] == user_prefs.get("mood") else 0.0
    if mood_pts:
        reasons.append(f"mood match (+{mood_pts:.1f})")

    # --- Numeric features (proximity scoring) ---
    energy_pts       = POINTS["energy"]       * (1.0 - abs(song["energy"]       - user_prefs.get("energy",       0.5)))
    valence_pts      = POINTS["valence"]      * (1.0 - abs(song["valence"]      - user_prefs.get("valence",      0.5)))
    danceability_pts = POINTS["danceability"] * (1.0 - abs(song["danceability"] - user_prefs.get("danceability", 0.5)))
    acousticness_pts = POINTS["acousticness"] * (1.0 - abs(song["acousticness"] - user_prefs.get("acousticness", 0.5)))

    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs.get('energy', 0.5):.2f} (+{energy_pts:.2f})")
    reasons.append(f"valence {song['valence']:.2f} vs target {user_prefs.get('valence', 0.5):.2f} (+{valence_pts:.2f})")
    reasons.append(f"danceability {song['danceability']:.2f} vs target {user_prefs.get('danceability', 0.5):.2f} (+{danceability_pts:.2f})")
    reasons.append(f"acousticness {song['acousticness']:.2f} vs target {user_prefs.get('acousticness', 0.5):.2f} (+{acousticness_pts:.2f})")

    score = genre_pts + mood_pts + energy_pts + valence_pts + danceability_pts + acousticness_pts
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song with score_song, sort by score descending, and return the top k."""
    scored = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
