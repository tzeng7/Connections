# Connections Game CSV Statistics Design

## Overview
This document outlines the design for tracking Connections game statistics in a CSV file format.

## Data Requirements
Based on user requirements, we need to track:
- Model used for the game
- List of all guesses made during the game
- Whether the game was won or lost

## CSV Structure

### File: `connections_stats.csv`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| timestamp | datetime | When the game was played | 2025-01-20 10:30:45 |
| model | string | AI model used | ChatGPTLLMPrompter |
| guesses | string | JSON array of all guesses | [["APPLE","ORANGE","BANANA","GRAPE"],["DOG","CAT","BIRD","FISH"]] |
| game_outcome | string | "won" or "lost" | won |
| total_guesses | integer | Number of guesses made | 3 |

## Implementation Plan

### 1. StatWriter Class
Create a `StatWriter` class with methods:
- `__init__(csv_file_path)` - Initialize with CSV file path
- `write_game_stats(model, guesses, outcome)` - Write a single game's stats
- `_ensure_csv_exists()` - Create CSV with headers if it doesn't exist

### 2. GameAutomation Integration
Modify the [`Connections`](GameAutomation.py:19) class:
- Add `StatWriter` instance in `__init__`
- Track all guesses in a list during gameplay
- Determine final outcome (won/lost) at game end
- Call `write_game_stats()` when game completes

### 3. Game Outcome Detection
Enhance existing methods:
- Use [`has_won()`](GameAutomation.py:27) to detect victory
- Use [`has_ended_incorrect()`](GameAutomation.py:41) to detect loss
- Track final state in [`play()`](GameAutomation.py:149) method

### 4. Guess Tracking
Modify [`make_guess()`](GameAutomation.py:139) method:
- Store each guess in instance variable
- Include both successful and failed attempts

## Code Integration Points

### Current Game Flow Analysis
1. [`setup()`](GameAutomation.py:116) - Initialize game
2. [`play()`](GameAutomation.py:149) - Main game loop
3. [`make_guess()`](GameAutomation.py:139) - Individual guess attempts
4. Game end detection via win/loss conditions

### Required Modifications
1. Add `self.all_guesses = []` to track guesses
2. Add `self.stat_writer = StatWriter("connections_stats.csv")` 
3. Append each guess to `self.all_guesses`
4. Call `stat_writer.write_game_stats()` at game end

## Example CSV Output
```csv
timestamp,model,guesses,game_outcome,total_guesses
2025-01-20 10:30:45,ChatGPTLLMPrompter,"[[""APPLE"",""ORANGE"",""BANANA"",""GRAPE""],[""DOG"",""CAT"",""BIRD"",""FISH""]]",won,2
2025-01-20 10:35:12,GeminiLLMPrompter,"[[""RED"",""BLUE"",""GREEN"",""YELLOW""],[""CHAIR"",""TABLE"",""SOFA"",""BED""],[""HAPPY"",""SAD"",""ANGRY"",""CALM""]]",lost,3
```

## Next Steps
1. Switch to Code mode to implement the StatWriter class
2. Integrate stat tracking into GameAutomation class
3. Test with sample data
4. Verify CSV file creation and updates