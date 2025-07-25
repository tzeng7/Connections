import csv
import os
import json
from datetime import datetime
from typing import List

class StatWriter:
    def __init__(self, csv_file_path: str = "connections_stats.csv"):
        """
        Initialize StatWriter with CSV file path
        
        Args:
            csv_file_path: Path to the CSV file for storing game statistics
        """
        self.csv_file_path = csv_file_path
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['model', 'guesses', 'game_outcome', 'total_guesses'])
    
    def write_game_stats(self, model: str, guesses: List[str], outcome: str):
        """
        Write game statistics to CSV file
        
        Args:
            model: Name of the AI model used (e.g., 'ChatGPTLLMPrompter')
            guesses: List of guesses, where each guess is a list of 4 words
            outcome: 'won' or 'lost'
        """
        total_guesses = len(guesses)
        
        with open(self.csv_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([model, guesses, outcome, total_guesses])
        
        print(f"Game stats written to {self.csv_file_path}: {model} - {outcome} ({total_guesses} guesses)")
    