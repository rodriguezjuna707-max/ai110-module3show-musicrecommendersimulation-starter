# Model Card: Music Recommender Simulation

## 1. Model Name
**VibeFinder 1.0**

---

## 2. Intended Use
Suggests 5 songs from an 18-song catalog based on a user's preferred genre, mood, and energy level. Built for classroom exploration — not for real-world use.

---

## 3. How It Works
Each song gets a score from 0 to 5. The score is higher when the song's genre and mood match the user's, and when its energy, valence, danceability, and acousticness are close to the user's targets. Genre and mood are the biggest factors. The top 5 scores are returned with an explanation of why each song was picked.

---

## 4. Data
- 18 songs, 15 genres, 12 moods
- No songs were added or removed
- Lofi has 3 songs; pop has 2; every other genre has exactly 1
- Gaps: no Latin, no K-pop, no R&B subgenres, very few sad or melancholic songs

---

## 5. Strengths
- Works well when the user's genre is in the catalog (e.g. pop, lofi, rock)
- Explanations are clear — every recommendation shows which features matched and by how much
- Energy is the strongest numeric signal and meaningfully separates the catalog

---

## 6. Limitations and Bias

**Main weakness: genre matching is all-or-nothing.**

The system gives a full penalty to any genre that does not match exactly, no matter how similar the genres are. A rock fan gets a worse result from a metal song (score 2.81) than from an electronic song (score 3.61), because the electronic song happened to share the "intense" mood tag. Metal and rock sound nearly identical, but the system treats them as unrelated. This locks users inside their exact genre label and hides the closest sonic matches. The problem is worse because 13 of 15 genres appear only once — a single mismatch eliminates the only song in that whole style.

---

## 7. Evaluation

Tested 7 profiles total — 3 normal and 4 adversarial.

**Normal profiles**
- High-Energy Pop (pop / happy / energy 0.90) — results felt right; Sunrise City won cleanly with genre + mood + near-perfect energy
- Chill Lofi (lofi / chill / energy 0.30) — top 3 were all lofi songs; no surprises
- Deep Intense Rock (rock / intense / energy 0.92) — #1 was correct, but seeing an electronic song (Drop Zone) rank above a metal song (Fury Road) was unexpected and revealed the adjacent-genre flaw

**Adversarial profiles**
- Conflicting preferences (indie / sad / energy 0.90) — the system split between a quiet sad song and loud angry songs; neither felt like a real match, which is the correct behavior to flag
- Rare genre (bossa nova) — best possible score was 3.95/5.0 regardless of how well numerics matched; surprising how much one missing genre label costs
- All-neutral numerics (jazz / relaxed / all at 0.50) — #2 through #5 scored within 0.11 of each other, making rankings almost arbitrary; showed how little numeric features differentiate when the user has no strong preferences
- Acoustic metalhead (metal / intense / acousticness 1.0) — the acousticness preference contributed +0.01 to the winner's score and was effectively ignored; that was the biggest surprise in the whole experiment set

---

## 8. Future Work
- Replace binary genre matching with a similarity score (e.g. rock and metal share 80%, pop and classical share 10%)
- Add more songs per genre so a genre miss isn't automatically a dead end
- Learn from listening history so the system adapts to each user over time

---

## 9. Personal Reflection
Building this showed me that a recommender's biggest decisions aren't in the code — they're in the weights. Choosing how much genre matters versus energy matters determines who gets good results and who doesn't. Real apps like Spotify almost certainly learned those weights from millions of skips and replays rather than guessing them by hand, which is why they can surface a metal song for a rock fan while this system cannot.
