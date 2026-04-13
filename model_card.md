# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
**VibeFinder 1.0**

---

## 2. Intended Use  
VibeFinder 1.0 is a classroom simulation designed to demonstrate how a content-based recommendation system operates. It generates ranked music suggestions by matching a user's explicit taste profile to the internal "DNA" (audio features and metadata) of songs in a catalog. It assumes the user already knows exactly what they want in terms of genre, mood, and numeric vibe (energy and danceability). It is not meant for production use, but rather as an educational tool to explore algorithmic weighting and bias.

---

## 3. How the Model Works  
This system uses a pure **content-based filtering** approach and relies on a point-based scoring algorithm. It does not use any collaborative data (like listening history or what other users click). 

When a user submits their preferences, the model acts as a judge, scoring every song in the catalog out of a possible 5.0 points:
* **Genre Match:** Awards +2.0 points for an exact text match.
* **Mood Match:** Awards +1.0 point for an exact text match.
* **Numeric Proximity:** Calculates the mathematical gap between the user's target numbers for Energy and Danceability and the song's actual numbers. It awards up to +1.0 point for each feature based on how close they are (e.g., a perfect match gets +1.0, a gap of 0.2 gets +0.8).

The songs are then sorted from highest to lowest score and the top results are returned. 

---

## 4. Data  
The model uses a highly simplified, static CSV catalog of 17 songs. 
* The baseline data included 10 songs focused heavily on pop, lofi, and chill aesthetics. 
* 7 additional tracks were manually added to increase diversity, introducing genres like cinematic, chiptune, hip-hop, metal, and R&B. 
* The dataset is entirely synthetic. Because it lacks historical user behavior data, the model cannot make recommendations based on what is currently popular or trending.

---

## 5. Strengths  
The system excels when a user has a highly specific, traditional musical request (e.g., "High-energy, highly danceable Pop music"). Because it heavily weights genre and calculates exact mathematical proximity for audio features, it is extremely accurate at isolating the perfect "vibe" within a well-defined musical category. The terminal output also provides clear, transparent explanations for *why* a song was recommended, which builds trust.

---

## 6. Limitations and Bias  
The algorithm suffers from a prominent **"Genre Filter Bubble"** bias. Because an exact genre match is rewarded with an overwhelming +2.0 points, the system structurally over-prioritizes genre over actual audio feel. 

If a user requests a highly danceable track but lists "Metal" as their favorite genre, the system will push an un-danceable, low-energy metal track to the top of the list simply because of the 2-point genre advantage, completely ignoring a mathematically perfect pop or hip-hop track that actually fits the requested vibe.

---

## 7. Evaluation  
The system was evaluated through terminal-based CLI stress testing using three distinct profiles:
1. **The Pop Fan:** (Standard baseline test)
2. **The Cel-Shaded Gamer:** (Testing for specific niche genres like Chiptune and high energy)
3. **The Confused User:** (An adversarial profile requesting Metal music that is sad, but highly energetic and highly danceable).

The Confused User profile was the most illuminating. It proved that the system's point-weights were unbalanced, as the algorithm recommended "Iron Fury" (a slow, angry metal song) over tracks with near-perfect danceability scores purely to satisfy the genre condition. 

---

## 8. Future Work  
If I were to continue developing this model, I would implement the following:
* **Weight Balancing:** Reduce the Genre match reward from +2.0 to +1.0 to encourage cross-genre discovery based on audio features (like energy and danceability).
* **Diversity Penalty:** Write a logic rule that subtracts points if the same artist appears back-to-back in the top recommendations, preventing one artist from dominating the results.
* **Expanded Data:** Integrate the `acousticness` and `valence` columns from the CSV into the scoring logic for deeper nuance.

---

## 9. Personal Reflection  
As a computer science student diving into software and AI engineering, it was fascinating to build the actual math behind the platforms I use every day. It is easy to assume that the algorithms running Spotify or TikTok are impossibly complex black boxes, but seeing how a few simple `if` statements and basic subtraction can create a "filter bubble" was a huge learning moment. It really highlighted how a developer's seemingly innocent choices—like deciding a genre match is worth 2 points instead of 1—can drastically alter what content a user is allowed to discover.