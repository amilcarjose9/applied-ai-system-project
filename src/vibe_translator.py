import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load the secret key from the .env file
load_dotenv()

# Initialize the Google GenAI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define the strict JSON schema using Pydantic
class VibeProfile(BaseModel):
    favorite_genre: str = Field(description="Choose ONE best fit from: pop, lofi, rock, ambient, jazz, synthwave, classical, hip-hop, metal, country, r&b, reggae, blues")
    favorite_mood: str = Field(description="A single descriptive word for the vibe")
    target_energy: float = Field(description="Float between 0.0 and 1.0", ge=0.0, le=1.0)
    target_valence: float = Field(description="Float between 0.0 (sad) and 1.0 (happy)", ge=0.0, le=1.0)
    target_danceability: float = Field(description="Float between 0.0 and 1.0", ge=0.0, le=1.0)
    target_acousticness: float = Field(description="Float between 0.0 (electronic) and 1.0 (acoustic)", ge=0.0, le=1.0)
    target_tempo_bpm: int = Field(description="Integer between 60 and 160", ge=60, le=160)

def create_profile_from_text(user_input: str) -> dict:
    """
    Takes natural language text and uses AI to translate it into 
    numerical audio parameters for the recommender.
    """
    print(f"🧠 AI is translating your vibe: '{user_input}'...")
    
    prompt = f'Translate the following music vibe into specific numerical targets: "{user_input}"'
    
    try:
        # Call the AI
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VibeProfile,
                temperature=0.5, # Keep temperature low for deterministic data extraction
            ),
        )
        
        # Parse the JSON response
        profile_data = response.parsed.model_dump()
        
        print("\n✨ AI Generated Profile:")
        for key, value in profile_data.items():
            print(f"  - {key}: {value}")
            
        return profile_data
        
    except Exception as e:
        print(f"\n❌ Error translating vibe: {e}")
        # Guardrail: A safe fallback profile so the app doesn't crash
        return {
            "favorite_genre": "pop",
            "favorite_mood": "neutral",
            "target_energy": 0.5,
            "target_valence": 0.5,
            "target_danceability": 0.5,
            "target_acousticness": 0.5,
            "target_tempo_bpm": 100
        }