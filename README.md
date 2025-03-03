# Connections

LLM wrapper to use Google's Gemini API to play NYT Connections where users
are tasked to match 16 unique words to 4 themes. 

### TODO:
- Link game to automation
  - if theme is correct, take out words from the game's list
  - if 3 words match a theme, specify prompt / see if the "one away" element can be reached
  - if incorrect, repeat. 
- Use hints provided by site to help LLM find answers 
  - add to prompt before playing
