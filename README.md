# Connections

LLM wrapper to use and compare different LLM models to play NYT Connections where users
are tasked to match 16 unique words to 4 themes. The LLM will be prompted based on a history
of pre-existing Connections themes to give it an idea of what type of matches or 
themes the game typically uses.

The game is currently run on four different LLM models. Due to concerns on
resource exhaustion or rate limits, the games will be performed on the least trained
variants for each model and will switch to a more trained version as the game stalls. For now,
when the model guesses matches incorrectly twice, the model will swap to the Pro model
with the prexisting chat history for it to work on.

The game will use the model's guesses and run Selenium automation to click on 
the cards that match each word within the guess.

Running the script will play today's Connections only.

## Compare LLM models on how well they can solve Connections
```commandline
Deepseek
Gemini
ChatGPT
Claude
```

```commandline
GameAutomation.py
```

# Stats Collection

*connections_stats.csv* and *total_statistics.csv* hold the statistics for each LLM for the first 50 connections games in the Connections archive. This is used to benchmark how well each LLM can play the game and match words to a specific theme. 

*connections_stats.csv* shows each LLMs progression through each game and each individual guess that the model made. 

*total_statistics.csv* shows the total stats for each model.
