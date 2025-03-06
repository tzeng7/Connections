# Connections

LLM wrapper to use Google's Gemini API to play NYT Connections where users
are tasked to match 16 unique words to 4 themes. The LLM will be prompted based on a history
of pre-existing Connections themes to give it an idea of what type of matches or 
themes the game typically uses.

The game is currently run on Gemini 2.0 Flash model as there were worries of resource
exhaustion if I used a more well-trained model such as Gemini 2.0 Pro. For now,
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

TODO:
find out how to swap model openai
deepseek api
claude api


