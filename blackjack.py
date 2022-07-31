import sys
from os import system
import getopt

from player import Player
from game import BlackJack

# Let's start a game of Blackjack

def main():
  game_options = {}
  try:
    matched_args, _ = getopt.getopt(sys.argv[1:], "hn:x:s:",["help", "bet_min","bet_max=","shoe_count="])

    for option, value in matched_args:
      if option in ["-h", "--help"]:
        print("""
        Options:
          -n, --bet_min: The table's minimum bet.
          -x, --bet_max: The tables initial bet limit.
          -s --shoe_count: The number of decks in the dealing shoe.
        """)
        sys.exit()

      if not value.isnumeric():
        raise getopt.GetoptError("Option inputs must be an integer value.")
        
      value = int(value)
      if option in ["-n", "--bet_min"]:
        game_options.update({"bet_min": value})
      elif option in ["-x", "--bet_max"]:
        game_options.update({"bet_max": value})
      elif option in ["-s", "--shoe_count"]:
        game_options.update({"shoe_count": value})

  except getopt.GetoptError as e:
    print(e)
    sys.exit()

  print(game_options)

  system("clear")
  print("Hi! Welcome to the Black Jack table ...")
  name = input("What's your name? ")

  chips = input("How many $'s of chips do you want to buy? ")
  while not chips.isnumeric():
    chips = input("Must be a number: ")

  player = Player(name, int(chips))
  game = BlackJack(player, **game_options)
  game.play()

if __name__ == "__main__":
  main()