from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
                
    except FileNotFoundError:
        print(f"Error: The file at '{csv_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while parsing the CSV: {e}")
        
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Calculates a match score between a user profile and a song.
    Returns the total score and a list of reasons for that score.
    """
    score = 0.0
    reasons = []

    # 1. Categorical Bonuses
    if song.get('genre') == user_prefs.get('favorite_genre'):
        score += 2.0
        reasons.append("Genre match (+2.00)")
        
    if song.get('mood') == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append("Mood match (+1.00)")

    # 2. Continuous Proximity Scores
    
    # Energy (Weight: x1.5)
    if 'target_energy' in user_prefs and 'energy' in song:
        energy_diff = abs(user_prefs['target_energy'] - song['energy'])
        energy_pts = (1.0 - energy_diff) * 1.5
        score += energy_pts
        reasons.append(f"Energy match (+{energy_pts:.2f})")

    # Valence (Weight: x1.0)
    if 'target_valence' in user_prefs and 'valence' in song:
        valence_diff = abs(user_prefs['target_valence'] - song['valence'])
        valence_pts = (1.0 - valence_diff) * 1.0
        score += valence_pts
        reasons.append(f"Valence match (+{valence_pts:.2f})")

    # Danceability (Weight: x1.0)
    if 'target_danceability' in user_prefs and 'danceability' in song:
        dance_diff = abs(user_prefs['target_danceability'] - song['danceability'])
        dance_pts = (1.0 - dance_diff) * 1.0
        score += dance_pts
        reasons.append(f"Danceability match (+{dance_pts:.2f})")

    # Acousticness (Weight: x0.5)
    if 'target_acousticness' in user_prefs and 'acousticness' in song:
        acoustic_diff = abs(user_prefs['target_acousticness'] - song['acousticness'])
        acoustic_pts = (1.0 - acoustic_diff) * 0.5
        score += acoustic_pts
        reasons.append(f"Acousticness match (+{acoustic_pts:.2f})")

    # Tempo (Weight: x1.0) - Requires Normalization
    if 'target_tempo_bpm' in user_prefs and 'tempo_bpm' in song:
        # Min-max scaling: mapping 60-160 BPM to a 0.0-1.0 scale
        min_bpm, max_bpm = 60.0, 160.0
        
        def normalize_bpm(bpm: float) -> float:
            # Clamps the value between the min and max limits
            clamped = max(min_bpm, min(max_bpm, bpm))
            return (clamped - min_bpm) / (max_bpm - min_bpm)
            
        norm_target = normalize_bpm(user_prefs['target_tempo_bpm'])
        norm_song = normalize_bpm(song['tempo_bpm'])
        
        tempo_diff = abs(norm_target - norm_song)
        tempo_pts = (1.0 - tempo_diff) * 1.0
        score += tempo_pts
        reasons.append(f"Tempo match (+{tempo_pts:.2f})")

    # Return the score rounded to 2 decimal places alongside the explanation list
    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores all songs against user preferences and returns the top k matches.
    """
    scored_catalog = []
    
    # 1. Score every song in the catalog
    for song in songs:
        score, reasons_list = score_song(user_prefs, song)
        explanation = ", ".join(reasons_list) if reasons_list else "No specific matches found."
        scored_catalog.append((song, score, explanation))
        
    # 2. Rank the catalog from highest to lowest score
    scored_catalog.sort(key=lambda item: item[1], reverse=True)
    
    # 3. Return only the top k results using list slicing
    return scored_catalog[:k]
