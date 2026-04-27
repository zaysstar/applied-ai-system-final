"""
Applied AI System: The "Vibe-Translator" Agent
"""
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from src.recommender import load_songs, recommend_songs

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file.")
    exit()

# Configure the Gemini API
genai.configure(api_key=api_key)

def get_vibe_from_agent(user_input: str) -> dict:
    """
    Acts as an AI Agent translating natural language into a structured JSON taste profile.
    """
    print("\n🤖 Agent is analyzing your vibe...")
    
    # Switch to the 'lite' model to avoid strict Free Tier quota limits
    model = genai.GenerativeModel('gemini-flash-lite-latest')
    
    prompt = f"""
    You are a data-extraction agent for a music recommendation engine.
    Read the user's input and translate their 'vibe' into a JSON object.
    
    The JSON MUST contain exactly these 4 keys:
    - "favorite_genre" (string: guess the closest genre from this list: pop, lofi, rock, ambient, jazz, synthwave, indie pop, chiptune, cinematic, hip-hop, metal, r&b, country, folk)
    - "favorite_mood" (string: guess the closest emotion/mood)
    - "target_energy" (float between 0.0 and 1.0)
    - "target_danceability" (float between 0.0 and 1.0)
    
    User Input: "{user_input}"
    """

    try:
        # Request the JSON generation
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2 
            )
        )
        
        # Parse the JSON string from Gemini back into a Python dictionary
        user_prefs = json.loads(response.text)
        return user_prefs

    except Exception as e:
        print(f"\n⚠️ Agent encountered an API limit or error.")
        print(f"Fallback mode activated! Using default pop profile.")
        # Fallback profile so your app STILL runs even if Google's servers block you!
        return {
            "favorite_genre": "pop", 
            "favorite_mood": "happy", 
            "target_energy": 0.8, 
            "target_danceability": 0.8
        }

def main() -> None:
    # 1. Load Data
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs into the catalog.")

    # 2. Get Natural Human Input
    print("-" * 50)
    print("🎧 Welcome to VibeFinder AI 🎧")
    print("-" * 50)
    user_text = input("Tell me what you're doing right now, or how you're feeling: ")
    
    if not user_text.strip():
        print("I need a vibe to work with! Try again.")
        return

    # 3. Agentic Workflow: Translate text -> Code
    user_prefs = get_vibe_from_agent(user_text)
    
    print("\n🧠 Agent generated this target profile:")
    print(json.dumps(user_prefs, indent=2))
    print("-" * 50)

    # 4. Standard Recommender Logic
    recommendations = recommend_songs(user_prefs, songs, k=3)

    print("\n🎶 Top Recommendations 🎶\n")
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"   Because: {explanation}\n")

if __name__ == "__main__":
    main()