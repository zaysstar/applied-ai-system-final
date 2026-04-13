## 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a pure content-based music recommendation simulation built in Python. Instead of relying on collaborative user data (like listening history or skip rates), this system mathematically analyzes the "DNA" of the songs themselves. By representing both the songs and a user's explicit "taste profile" as data dictionaries, the system uses a point-weighted algorithm to score and rank tracks. The goal of this project was to understand how simple scoring logic works and to observe how easily "filter bubbles" and biases can be accidentally programmed into recommendation platforms.

---

## How The System Works

The system operates by comparing a user's requested vibe against a catalog of songs, acting as a judge that awards points based on how closely they match.

* **Song Data (`Song`):** Each song in the dataset has categorical text features (`genre`, `mood`) and numerical audio features (`energy`, `danceability`, `tempo_bpm`, `valence`, `acousticness` on a 0.0–1.0 scale).
* **User Profile (`UserProfile`):** Stores the user's explicit target preferences: `favorite_genre`, `favorite_mood`, `target_energy`, and `target_danceability`.
* **The Scoring Logic:**  
  * Exact `genre` match: **+2.0 points**  
  * Exact `mood` match: **+1.0 points**  
  * `energy` match: **Up to +1.0 points** (calculated by how mathematically close the song's energy is to the user's target energy).  
  * `danceability` match: **Up to +1.0 points** (calculated just like energy).
* **The Ranking (`Recommender`):** The system loops through every song in the CSV, calculates a total score using the logic above, and sorts the list from highest score to lowest score to return the top *K* recommendations.

---

## Getting Started

## Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
Install dependencies:
pip install -r requirements.txt
Run the app:
python -m src.main
Running Tests

Run the starter tests with:

pytest
Experiments You Tried

To test the algorithm's accuracy and hunt for biases, I stress-tested the system using three distinct user profiles:

The Pop Fan:
A standard request for high-energy, happy pop music. The system worked perfectly, finding exact genre matches that also had math scores within 0.05 of the target energy.

The Cel-Shaded Gamer:
A request for highly energetic, highly danceable Chiptune music. This proved the system could successfully navigate niche genres in the expanded dataset.

The Confused User (Adversarial Test):
I created a user that asked for "Metal" music that is "Sad," but simultaneously requested extreme High-Energy (0.95) and High-Danceability (0.90).

Result:
The system recommended "Iron Fury"—a heavy metal track with a terrible danceability score of 0.55—over other tracks that perfectly matched the requested 0.90 danceability math. This proved the +2.0 genre weight was too strong.

Limitations and Risks

The Genre Filter Bubble:
Because the algorithm awards an overwhelming +2.0 points for an exact genre match, it suffers from a massive genre bias. It will force a bad mathematical match to the top of the list just to satisfy the genre string, completely preventing the user from discovering cross-genre tracks that actually fit their audio vibe better.

Tiny Catalog:
The system only pulls from a static CSV of 17 synthetic songs, meaning it lacks the depth to provide truly diverse recommendations over multiple uses.

No Collaborative Context:
Because it doesn't know what is trending or what the user's friends are listening to, the recommendations can feel a bit clinical or disconnected from real-world music culture.