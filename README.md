# 🎵 Music Recommender Simulation
 
## Project Summary


**VibeFinder** is a pure content-based music recommendation simulation built in Python. Instead of relying on collaborative user data (like listening history or skip rates), this system mathematically analyzes the "DNA" of the songs themselves. By representing both the songs and a user's explicit "taste profile" as data dictionaries, the system uses a point-weighted algorithm to score and rank tracks.
 
The goal of this project was to understand how simple scoring logic works and to observe how easily **filter bubbles** and **biases** can be accidentally programmed into recommendation platforms.
 
---
 
## How The System Works
 
The system operates by comparing a user's requested vibe against a catalog of songs, acting as a judge that awards points based on how closely they match.
 
### Song Data (`Song`)
 
Each song in the dataset has:
- **Categorical text features:** `genre`, `mood`
- **Numerical audio features:** `energy`, `danceability`, `tempo_bpm`, `valence`, `acousticness` (all on a `0.0–1.0` scale)
### User Profile (`UserProfile`)
 
Stores the user's explicit target preferences:
- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_danceability`
### The Scoring Logic
 
| Feature | Points Awarded |
|---|---|
| Exact `genre` match | **+2.0 points** |
| Exact `mood` match | **+1.0 points** |
| `energy` match | **Up to +1.0 points** (based on mathematical closeness to target) |
| `danceability` match | **Up to +1.0 points** (calculated the same way as energy) |
 
### The Ranking (`Recommender`)
 
The system loops through every song in the CSV, calculates a total score using the logic above, and sorts the list from highest score to lowest to return the top *K* recommendations.
 
---
 
## Getting Started
 
### Setup
 
1. **Create a virtual environment** *(optional but recommended)*:
```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```
 
2. **Install dependencies:**
```bash
pip install -r requirements.txt
```
 
3. **Run the app:**
```bash
python -m src.main
```
 
### Running Tests
 
```bash
pytest
```
 
---
 
## Experiments
 
To test the algorithm's accuracy and hunt for biases, the system was stress-tested using three distinct user profiles:
 
### 1. The Pop Fan
A standard request for high-energy, happy pop music. The system worked perfectly, finding exact genre matches that also had math scores within `0.05` of the target energy.
 
### 2. The Cel-Shaded Gamer
A request for highly energetic, highly danceable Chiptune music. This proved the system could successfully navigate niche genres in the expanded dataset.
 
### 3. The Confused User *(Adversarial Test)*
A user that asked for **"Metal"** music that is **"Sad"**, but simultaneously requested extreme High-Energy (`0.95`) and High-Danceability (`0.90`).
 
> **Result:** The system recommended *"Iron Fury"* — a heavy metal track with a poor danceability score of `0.55` — over other tracks that perfectly matched the requested `0.90` danceability. This proved the `+2.0` genre weight was too strong.
 
---
 
## Limitations and Risks
 
### ⚠️ The Genre Filter Bubble
Because the algorithm awards an overwhelming `+2.0` points for an exact genre match, it suffers from a significant genre bias. It will force a bad mathematical match to the top of the list just to satisfy the genre string, preventing the user from discovering cross-genre tracks that actually fit their audio vibe better.
 
### 📦 Tiny Catalog
The system only pulls from a static CSV of **17 synthetic songs**, meaning it lacks the depth to provide truly diverse recommendations over multiple uses.
 
### 🤝 No Collaborative Context
Because it doesn't know what is trending or what the user's friends are listening to, recommendations can feel clinical or disconnected from real-world music culture.
 
---
 
## 🧠 Model Card & Reflection: VibeFinder AI
 
### 1. Limitations and Bias
 
While the AI agent is excellent at translating intent, the system still suffers from the **"Genre Filter Bubble"** inherited from the underlying scoring algorithm. Because exact genre matches are heavily weighted, the AI might correctly deduce a user wants highly danceable music, but if it guesses the genre "metal," the Python logic will still force a non-danceable metal song to the top. Additionally, the LLM sometimes attempts to suggest genres (like "classical") that do not exist in the tiny 17-song CSV catalog, resulting in lower overall match scores.
 
### 2. Potential Misuse
 
Because this is a read-only recommendation system, physical or societal harm is extremely low. However, at a system level, malicious users could write a script to repeatedly ping the CLI interface with massive text inputs, rapidly exhausting the Gemini API quota and racking up cloud computing costs. Rate-limiting would be required for any production web deployment.
 
### 3. Reliability Surprises
 
The biggest surprise during testing was how **fragile live API integration** can be. Immediate issues included `404 Not Found` errors because the specific model version requested was deprecated in the region, followed by `429 Rate Limit` errors. This reinforced that an AI engineer's job isn't just writing prompts — it's building **robust error-handling and fallback states** for when the cloud inevitably fails.
 
### 4. AI Collaboration Reflection
 
AI assistance was heavily used to build this architecture.
 
**✅ Helpful Instance:** The AI was incredibly helpful in designing the `try/except` fallback loop and updating the model endpoint to `gemini-flash-lite-latest` to bypass Google's strict free-tier rate limits.
 
**❌ Flawed Instance:** Initially, the AI suggested using `gemini-1.5-flash` with the `response_mime_type="application/json"` config. While structurally sound, it didn't account for the fact that the specific Google API account hadn't fully provisioned that exact model version string yet, leading to a confusing cascade of `grpc` framework errors that required manual debugging.
