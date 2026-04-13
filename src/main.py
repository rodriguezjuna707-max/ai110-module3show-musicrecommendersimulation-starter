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


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: defines what this user wants in a song right now.
    # Categorical fields (genre, mood) use exact matching.
    # Numeric fields (0.0–1.0) use proximity scoring — closer to the target = higher score.
    user_prefs = {
        "genre":        "pop",   # favorite genre
        "mood":         "happy", # desired emotional tone
        "energy":       0.80,    # fairly high energy — upbeat but not aggressive
        "valence":      0.82,    # bright and positive sounding
        "danceability": 0.78,    # groovy enough to move to
        "acousticness": 0.20,    # mostly produced/electronic, not acoustic
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print("\n" + "=" * width)
    print(" MUSIC RECOMMENDATIONS ".center(width))
    print(f" For: {user_prefs['genre']} / {user_prefs['mood']} / energy {user_prefs['energy']} ".center(width))
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

    print("\n" + "=" * width + "\n")


if __name__ == "__main__":
    main()
