from player import Player
from game import BlackJack

# Let's start a game of Blackjack

def main():
  print("Hi! Welcome to the Black Jack table ...")
  name = input("What's your name? ")
  chips = int(input("How many $'s of chips do you want to buy? "))

  player = Player(name, chips)
  game = BlackJack(player)
  game.play()

if __name__ == "__main__":
  main()