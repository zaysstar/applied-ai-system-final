import csv
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
        # Using sorted() to return a new sorted list without modifying the original self.songs
        return sorted(self.songs, key=lambda song: self._calculate_score(user, song), reverse=True)[:k]

    def _calculate_score(self, user: UserProfile, song: Song) -> float:
        """Helper method to calculate numeric score for OOP recommend()"""
        score = 0.0
        if song.genre.lower() == user.favorite_genre.lower(): score += 2.0
        if song.mood.lower() == user.favorite_mood.lower(): score += 1.0
        score += max(0, 1.0 - abs(song.energy - user.target_energy))
        
        # Handling the boolean likes_acoustic preference
        if user.likes_acoustic and song.acousticness >= 0.5: score += 1.0
        elif not user.likes_acoustic and song.acousticness < 0.5: score += 1.0
        
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower(): reasons.append("Genre match (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower(): reasons.append("Mood match (+1.0)")
        
        energy_pts = round(1.0 - abs(song.energy - user.target_energy), 2)
        reasons.append(f"Energy match (+{energy_pts})")

        if user.likes_acoustic and song.acousticness >= 0.5: reasons.append("Acoustic match (+1.0)")
        elif not user.likes_acoustic and song.acousticness < 0.5: reasons.append("Non-acoustic match (+1.0)")
        
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert numeric strings to proper types
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song['genre'].lower() == user_prefs.get('favorite_genre', '').lower():
        score += 2.0
        reasons.append("Genre match (+2.0)")

    if song['mood'].lower() == user_prefs.get('favorite_mood', '').lower():
        score += 1.0
        reasons.append("Mood match (+1.0)")

    if 'target_energy' in user_prefs:
        energy_diff = abs(song['energy'] - user_prefs['target_energy'])
        energy_pts = round(1.0 - energy_diff, 2)
        score += energy_pts
        reasons.append(f"Energy match (+{energy_pts})")

    if 'target_danceability' in user_prefs:
        dance_diff = abs(song['danceability'] - user_prefs['target_danceability'])
        dance_pts = round(1.0 - dance_diff, 2)
        score += dance_pts
        reasons.append(f"Danceability match (+{dance_pts})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort the list of tuples in-place based on the score (index 1), descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_songs[:k]