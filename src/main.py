"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    # 1. Load the catalog
    songs = load_songs("data/songs.csv") 

    # 2. Define the target user profile
    user_prefs = {
        "favorite_genre": "pop", 
        "favorite_mood": "happy", 
        "target_energy": 0.80,
        "target_valence": 0.85,
        "target_tempo_bpm": 120
    }

    # 3. Generate recommendations
    recommendations = recommend_songs(user_prefs, songs, k=5)

    # 4. Format and display the output
    print("\n" + "=" * 55)
    print(" 🎧 YOUR CUSTOM PLAYLIST RECOMMENDATIONS 🎧")
    print("=" * 55)

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        
        # Display Title, Artist, and Score
        print(f"\n[{rank}] {song['title']} by {song['artist']}")
        print(f"    Match Score: {score:.2f} pts")
        print("    Why it matched:")
        
        # Split the explanation string into clean bullet points
        if explanation == "No specific matches found.":
            print(f"      - {explanation}")
        else:
            reasons = explanation.split(", ")
            for reason in reasons:
                print(f"      ✓ {reason}")
            
    print("\n" + "=" * 55 + "\n")


if __name__ == "__main__":
    main()
