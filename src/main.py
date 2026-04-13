"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs       # python src/main.py
except ImportError:
    from src.recommender import load_songs, recommend_songs   # python -m src.main


# ---------------------------------------------------------------------------
# Named user preference profiles
# Each dict maps feature names to the user's target values.
# Categorical fields (genre, mood) use exact matching.
# Numeric fields (0.0–1.0) use proximity scoring.
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.90,    # wants the highest-energy tracks available
    "valence":      0.85,    # bright and euphoric
    "danceability": 0.88,    # very danceable
    "acousticness": 0.05,    # almost no acoustic texture — purely produced
}

CHILL_LOFI = {
    "genre":        "lofi",
    "mood":         "chill",
    "energy":       0.30,    # low-key, background-music vibe
    "valence":      0.45,    # mellow, neither sad nor ecstatic
    "danceability": 0.35,    # not meant for dancing — just vibing
    "acousticness": 0.70,    # warm, slightly acoustic texture
}

DEEP_INTENSE_ROCK = {
    "genre":        "rock",
    "mood":         "intense",
    "energy":       0.92,    # near-maximum raw power
    "valence":      0.30,    # dark, driven sound — not uplifting
    "danceability": 0.40,    # rhythmic but not dance-floor
    "acousticness": 0.08,    # heavy distortion, very little acoustic warmth
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# These are designed to stress-test the scoring logic and expose weaknesses.
# ---------------------------------------------------------------------------

# EDGE 1 — Conflicting categorical + numeric intent
# High energy (0.9) paired with a "sad" mood creates a contradiction:
# the system will reward energy matches but ignore that "sad" songs in the
# catalog tend to be low-energy, so the top result may feel emotionally wrong.
CONFLICTING_ENERGY_SAD = {
    "genre":        "indie",
    "mood":         "sad",
    "energy":       0.90,    # aggressive energy — conflicts with sad mood
    "valence":      0.15,    # very low valence (dark/gloomy)
    "danceability": 0.50,
    "acousticness": 0.40,
}

# EDGE 2 — Genre that almost certainly has no catalog representative
# "bossa nova" is unlikely to appear in an 18-song catalog.
# The user will be capped at 3.0/5.0 maximum no matter how good the
# numeric match is, exposing the "small catalog genre penalty" bias.
RARE_GENRE = {
    "genre":        "bossa nova",
    "mood":         "chill",
    "energy":       0.35,
    "valence":      0.60,
    "danceability": 0.50,
    "acousticness": 0.65,
}

# EDGE 3 — All numeric targets at 0.5 (the exact midpoint)
# A "perfectly average" user has zero numeric discrimination power.
# Every song scores identically on energy/valence/danceability/acousticness,
# so ranking falls entirely to genre/mood luck — reveals catalog bias.
PERFECTLY_AVERAGE = {
    "genre":        "jazz",
    "mood":         "relaxed",
    "energy":       0.50,
    "valence":      0.50,
    "danceability": 0.50,
    "acousticness": 0.50,
}

# EDGE 4 — Extreme acoustic preference (1.0) with an electric genre
# A user who wants maximum acousticness but loves metal/rock will get
# penalized heavily on both ends — tests whether numeric and categorical
# signals can both bottom out simultaneously.
ACOUSTIC_METALHEAD = {
    "genre":        "metal",
    "mood":         "intense",
    "energy":       0.95,
    "valence":      0.20,
    "danceability": 0.30,
    "acousticness": 1.00,    # wants fully acoustic sound from a metal catalog
}


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

def print_recommendations(user_prefs: dict, songs: list, label: str, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    width = 60
    print("\n" + "=" * width)
    print(f" {label} ".center(width))
    print(f" {user_prefs['genre']} / {user_prefs['mood']} / energy {user_prefs['energy']} ".center(width))
    print("=" * width)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        bar_filled = round((score / 5.0) * 20)
        bar = "#" * bar_filled + "-" * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       [{bar}] {score:.2f} / 5.0")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print("       Why recommended:")
        for reason in reasons:
            print(f"         - {reason}")

    print("\n" + "=" * width)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Named profiles ---
    print_recommendations(HIGH_ENERGY_POP,    songs, "HIGH-ENERGY POP")
    print_recommendations(CHILL_LOFI,         songs, "CHILL LOFI")
    print_recommendations(DEEP_INTENSE_ROCK,  songs, "DEEP INTENSE ROCK")

    # --- Adversarial / edge-case profiles ---
    print("\n\n" + "#" * 60)
    print("  ADVERSARIAL / EDGE-CASE PROFILES".center(60))
    print("#" * 60)

    print_recommendations(CONFLICTING_ENERGY_SAD, songs, "EDGE 1 — Conflicting: high energy + sad mood")
    print_recommendations(RARE_GENRE,             songs, "EDGE 2 — Rare genre (bossa nova)")
    print_recommendations(PERFECTLY_AVERAGE,      songs, "EDGE 3 — All numerics at 0.5 (perfectly average)")
    print_recommendations(ACOUSTIC_METALHEAD,     songs, "EDGE 4 — Acoustic metalhead (contradictory)")


if __name__ == "__main__":
    main()
