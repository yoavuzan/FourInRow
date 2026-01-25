import sys
import os
import numpy as np

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from backend.game import Game

def print_board(board_state):
    # Flip the board for correct display (0,0 at bottom-left)
    print(np.flip(board_state, 0))
    print(" 0  1  2  3  4  5  6")

def main():
    game = Game()
    print_board(game.get_board_display()) # Print initial board

    while not game.game_over:
        player = game.get_current_player()
        
        try:
            col_input = input(f"{player.name}, choose a column (0-6): ")
            col = int(col_input.strip())
            
            if 0 <= col <= 6:
                success, message = game.play_turn(col)
                if not success:
                    print(f"Error: {message}")
        
                else: # Move was successful
                    print_board(game.get_board_display()) # Print updated board
                    if game.game_over:
                        print(f"\n--- GAME OVER ---")
                        print(f"Result: {message}")
            else:
                print("Error: Column must be between 0 and 6.")
        
        except ValueError:
            print("Error: Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nGame aborted. Exiting.")
            break
        print("-" * 20)

if __name__ == "__main__":
    main()
