from recommender import load_songs, recommend_songs
from vibe_translator import create_profile_from_text

def main() -> None:
    # 1. Load the catalog
    songs = load_songs("data/songs.csv") 

    print("\n" + "=" * 60)
    print(" 🔮 WELCOME TO THE AI VIBE TRANSLATOR 🔮 ")
    print("=" * 60)
    
    while True:
        # 2. Get natural text from the user
        user_input = input("\nDescribe your ideal music vibe right now (or type 'quit'):\n> ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        # 3. Use AI to translate text to numbers
        ai_profile = create_profile_from_text(user_input)
        
        if not ai_profile:
            continue # Skip this round if the API failed entirely
            
        # 4. Feed the AI numbers into your existing math logic
        print("\n🔍 Finding your perfect tracks...")
        recommendations = recommend_songs(ai_profile, songs, k=3)

        # 5. Display the results
        for rank, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print(f"\n[{rank}] {song['title']} by {song['artist']}")
            print(f"    Match Score: {score:.2f} pts")
            print("    Why it matched:")
            
            reasons = explanation.split(", ")
            for reason in reasons:
                print(f"      ✓ {reason}")

if __name__ == "__main__":
    main()
