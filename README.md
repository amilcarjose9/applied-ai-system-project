# 🎵 AI-Powered Music Vibe Translator

## Original Project: Music Recommender Simulation
Originally, the "Music Recommender Simulation" was a strictly rule-based engine designed to demonstrate how platforms like Spotify match tracks to users. It relied on hardcoded user "taste profiles" containing specific mathematical targets (e.g., 0.8 energy, 0.2 acousticness) and calculated proximity scores against a database of songs to rank the best matches. While mathematically sound, it required users to speak like computers to get a good recommendation.

## Project Summary
This project enhances that foundational recommendation engine by integrating **Generative AI (Gemini API)** to act as a "Vibe Translator." Instead of manually entering decimal values, users simply type how they feel or what they are doing in natural language (e.g., *"I need to study late at night while it's raining"*). The AI agent translates this human intent into a structured JSON object of exact numerical audio parameters, bridging the gap between human emotion and programmatic scoring algorithms.

## Architecture Overview
The system relies on a hybrid architecture, passing control between natural language processing and deterministic math.

![System Diagram](/assets/ai-vibe-translator-system-diagram.png)

1. **User Input:** Natural language text is captured via the terminal.
2. **AI Agent (Vibe Translator):** Uses the Gemini 2.5 Flash model to interpret the prompt. It enforces a strict Pydantic schema to guarantee the output is perfectly formatted JSON.
3. **Scoring Logic:** The traditional recommendation engine receives the AI's data and scores the CSV catalog based on mathematical distances.
4. **Evaluation Loop:** AI translations and final scores are logged to the console for real-time human evaluation and debugging.

## Setup Instructions
To run this project locally, ensure you have Python 3.9+ installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amilcarjose9/applied-ai-system-project.git
   cd applied-ai-system-project
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your API Key:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```text
   GEMINI_API_KEY="your_api_key_here"
   ```
4. **Run the application:**
   ```bash
   cd src
   python main.py
   ```

## Sample Interactions

**Example 1: The Lofi Study Session**
> **Input:** *"I just want to chill in the rain."*
> **AI Output (`VibeProfile`):**
> * Genre: lofi
> * Mood: Calm
> * Energy: 0.3
> * Valence: 0.5
> * Danceability: 0.2
> * Acousticness: 0.7
> * Tempo: 75 BPM
> 
> **System Result:** Successfully recommended *Library Rain* and *Midnight Coding*.

![Lofi Study Session AI output](/assets/ai_outputs/lofi_study_session.png)

**Example 2: The Intense Workout**
> **Input:** *"I am lifting heavy weights and need to feel like a superhero."*
> **AI Output (`VibeProfile`):**
> * Genre: metal
> * Mood: triumphant
> * Energy: 0.95
> * Valence: 0.9
> * Danceability: 0.6
> * Acousticness: 0.1
> * Tempo: 145 BPM
> 
> **System Result:** Successfully recommended *Iron and Blood* and *Gym Hero*.

![Intense Workout AI output](/assets/ai_outputs/intense_workout.png)

## Design Decisions
* **Strict Structured Outputs over Prompt Engineering:** Initially, I considered writing a long prompt asking the LLM to format its response as JSON. Instead, I used the `google-genai` SDK's `response_schema` feature with a **Pydantic** model. *Trade-off:* This slightly restricts the AI's "conversational" nature, but it guarantees absolute type safety (e.g., ensuring `target_energy` is always a float between 0.0 and 1.0) so the math engine never crashes from bad data.
* **Separation of AI and Math:** I chose *not* to give the entire `songs.csv` database to the AI to let it pick songs directly. *Trade-off:* It limits the AI's direct control over the playlist. *Benefit:* It makes the system vastly cheaper, faster, and prevents the AI from hallucinating songs that don't exist in our database. The AI simply provides the "steering wheel" for the traditional math engine.

## Reliability and Testing Summary
To ensure the AI Vibe Translator works reliably, I implemented **Logging and Error Handling** alongside **Human Evaluation**.

* **What worked (Logging):** Every time a user enters a prompt, the system prints the AI's extracted parameters to the console. This allowed me to easily evaluate the model's accuracy in real-time.
* **What worked (Guardrails):** A robust `try/except` block wraps the API call. If the user loses internet or the API times out, the system catches the error, logs it, and falls back to a safe default profile to prevent a total crash.

During testing, I discovered that entering the exact same prompt twice (e.g., "chill in the rain") sometimes results in slightly different AI targets (e.g., an acousticness of 0.8 vs 0.7). Rather than being a bug, this probabilistic behavior acts as a natural "jitter," dynamically reshuffling the final playlist and solving the problem of recommendation monotony. 

## Reflection
This project taught me a crucial lesson about building AI-integrated software: LLMs are fantastic reasoning engines, but terrible data structurers unless constrained. I learned that bridging the gap between natural human language and rigid, mathematical backend logic requires treating the AI not just as a chatbot, but as a specialized microservice. By utilizing Pydantic schemas, I realized how powerful AI can be when you force it to adhere to standard software engineering principles like strong typing and error handling. It shifted my perspective from just "writing good prompts" to engineering robust AI pipelines.