import sys
from os import system
import getopt

from player import Player
from game import BlackJack
from question import Question

# Starts a game of Blackjack

def main():
  game_options = {
    "bet_min": 2,
    "bet_max": 10,
    "shoe_count": 3
  }
  try:
    matched_args, _ = getopt.getopt(sys.argv[1:], "hn:x:s:",["help", "bet_min=","bet_max=","shoe_count="])

    # Need bet min to be known before setting bet_max
    matched_args.sort(key= lambda option: option[0], reverse=True)

    for option, value in matched_args:
      if option in ["-h", "--help"]:
        print("""
        Options:
          -n, --bet_min: The table's minimum bet, must be >= default $2.
          -x, --bet_max: Table limit, must be >= default $10 and 5 * bet-min.
          -s --shoe_count: decks in the shoe. Default 3. Min 1, max 10.
        """)
        sys.exit()

      if not value.isnumeric():
        raise getopt.GetoptError("Option inputs must be an integer value.")
        
      value = int(value)
      if option in ["-n", "--bet_min"]:
        if value < 2:
          raise getopt.GetoptError("bet-min must be at least 2")  
        game_options.update({"bet_min": value})

      elif option in ["-x", "--bet_max"]:
        if value < 10 or value < 5 * game_options["bet_min"]:
          raise getopt.GetoptError("bet-max must be > 10 and 5 * bet_min")  
        game_options.update({"bet_max": value})

      elif option in ["-s", "--shoe_count"]:
        if not (1 <= value <= 10):
          raise getopt.GetoptError("shoe_count must be between 1 to 10")  
        game_options.update({"shoe_count": value})

  except getopt.GetoptError as e:
    print(e)
    sys.exit()

  system("clear")
  print("Hi! Welcome to the Black Jack table ...")
  name = input("What's your name? ")
  chips = Question.get_numeric_response("How many $'s of chips do you want to buy?")

  player = Player(name, chips)
  game = BlackJack(player, **game_options)
  game.play()

if __name__ == "__main__":
  main()