import pandas as pd
from collections import defaultdict
import json

class StatsAnalyzer:
    def __init__(self, csv_file_path="connections_stats.csv"):
        self.csv_file_path = csv_file_path
        # CSV has no headers, so we need to specify column names
        self.df = pd.read_csv(csv_file_path, header=None, names=['model', 'guesses', 'game_outcome', 'total_guesses'])
        
    def analyze_stats(self):
        """Analyze game statistics and return comprehensive results"""
        results = {
            'model_summary': {},
            'guess_distribution': {},
            'overall_stats': {}
        }
        
        # Group by model
        for model in self.df['model'].unique():
            model_data = self.df[self.df['model'] == model]
            
            # Basic win/loss stats
            total_games = len(model_data)
            wins = len(model_data[model_data['game_outcome'] == 'won'])
            losses = len(model_data[model_data['game_outcome'] == 'lost'])
            win_rate = (wins / total_games) * 100 if total_games > 0 else 0
            
            # Win distribution by number of guesses
            won_games = model_data[model_data['game_outcome'] == 'won']
            guess_distribution = {}
            
            for guesses in [4, 5, 6, 7, 8, 9, 10]:
                count = len(won_games[won_games['total_guesses'] == guesses])
                guess_distribution[f'{guesses}_guesses'] = count
            
            # Average guesses for won games
            avg_guesses_won = won_games['total_guesses'].mean() if len(won_games) > 0 else 0
            
            results['model_summary'][model] = {
                'total_games': total_games,
                'wins': wins,
                'losses': losses,
                'win_rate': round(win_rate, 2),
                'avg_guesses_when_won': round(avg_guesses_won, 2),
                'guess_distribution': guess_distribution
            }
        
        # Overall statistics
        total_games = len(self.df)
        total_wins = len(self.df[self.df['game_outcome'] == 'won'])
        total_losses = len(self.df[self.df['game_outcome'] == 'lost'])
        overall_win_rate = (total_wins / total_games) * 100 if total_games > 0 else 0
        
        results['overall_stats'] = {
            'total_games': total_games,
            'total_wins': total_wins,
            'total_losses': total_losses,
            'overall_win_rate': round(overall_win_rate, 2)
        }
        
        return results
    
    def create_summary_csv(self, output_file="total_statistics.csv"):
        """Create a comprehensive CSV summary of all statistics"""
        stats = self.analyze_stats()
        
        # Create summary table data
        summary_data = []
        
        # Sort models by win rate for better display
        models_sorted = sorted(stats['model_summary'].items(), 
                             key=lambda x: x[1]['win_rate'], reverse=True)
        
        for model, data in models_sorted:
            row = {
                'Model': model,
                'Total_Games': data['total_games'],
                'Wins': data['wins'],
                'Losses': data['losses'],
                'Win_Rate_Percent': data['win_rate'],
                'Avg_Guesses_When_Won': data['avg_guesses_when_won'],
                'Wins_4_Guesses': data['guess_distribution']['4_guesses'],
                'Wins_5_Guesses': data['guess_distribution']['5_guesses'],
                'Wins_6_Guesses': data['guess_distribution']['6_guesses'],
                'Wins_7_Guesses': data['guess_distribution']['7_guesses'],
                'Wins_8_Guesses': data['guess_distribution']['8_guesses'],
                'Wins_9_Guesses': data['guess_distribution']['9_guesses'],
                'Wins_10_Guesses': data['guess_distribution']['10_guesses']
            }
            summary_data.append(row)
        
        # Create DataFrame and save to CSV
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(output_file, index=False)
        
        print(f"Summary statistics saved to {output_file}")
        
        # Also print a brief overview
        print("\n" + "=" * 60)
        print("CONNECTIONS GAME STATISTICS SUMMARY")
        print("=" * 60)
        
        overall = stats['overall_stats']
        print(f"Total Games: {overall['total_games']}")
        print(f"Total Wins: {overall['total_wins']}")
        print(f"Total Losses: {overall['total_losses']}")
        print(f"Overall Win Rate: {overall['overall_win_rate']}%")
        
        print(f"\nModel Rankings by Win Rate:")
        for i, (model, data) in enumerate(models_sorted, 1):
            print(f"{i}. {model}: {data['win_rate']}% ({data['wins']}/{data['total_games']})")
        
        print(f"\nDetailed statistics saved to: {output_file}")
        print("=" * 60)

if __name__ == "__main__":
    analyzer = StatsAnalyzer()
    analyzer.create_summary_csv()