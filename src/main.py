"""
Command line runner for the Music Recommender Simulation.
"""
from src.recommender import load_songs, recommend_songs

def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs into the catalog.\n")

    # Profile 1: The standard Pop fan
    pop_fan = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_danceability": 0.80
    }

    # Profile 2: The Cel-Shaded Gamer
    gamer_fan = {
        "favorite_genre": "chiptune",
        "favorite_mood": "energetic",
        "target_energy": 0.90,
        "target_danceability": 0.85
    }

    # Profile 3: The "Adversarial" Edge Case 
    # (High energy and highly danceable, but sad mood and acoustic?)
    confused_user = {
        "favorite_genre": "metal",
        "favorite_mood": "sad",
        "target_energy": 0.95,
        "target_danceability": 0.90
    }

    profiles = [
        ("The Pop Fan", pop_fan), 
        ("The Cel-Shaded Gamer", gamer_fan), 
        ("The Confused User", confused_user)
    ]

    for name, prefs in profiles:
        print(f"--- Recommendations for {name} ---")
        recommendations = recommend_songs(prefs, songs, k=3)
        for rank, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            print(f"   Because: {explanation}\n")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()