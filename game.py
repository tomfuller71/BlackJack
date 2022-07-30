from deck import Deck
from hand import Hand
from os import system


class BlackJack:
  def __init__(self, player):
    self.deck = Deck()
    self.player = player
    self._current_bet = 0
    
  def play(self):
    system("clear")
    print("Starting game ...")

    while True:
      self.play_hand()
      if self.game_over():
        break

    self.end()

  def play_hand(self):
    winner = ""

    self.player_bet()
    self.deal()
    self.player_plays()

    if self.player_hand.is_bust:
      winner = "Dealer"
    else:
      self.dealer_plays()

      if self.dealer_hand.is_bust:
        winner = "Player"
      elif self.dealer_hand.max_value > self.player_hand.max_value:
        winner = "Dealer"
      elif self.dealer_hand.max_value < self.player_hand.max_value:
        winner = "Player"
      else:
        winner = "Push"
      
    self.update_for_winner(winner)

  def player_bet(self):
      print(f"Balance: ${self.player.balance}")
      bet = int(input("How much do you want to bet? "))
      system("clear")

      while bet > self.player.balance:
        print("You don't have that much!")
        bet = int(input("How much do you want to bet? "))
        system("clear")

      self.player.deduct_bet(bet)
      self._current_bet = bet
  
  def deal(self):
    self.dealer_hand = Hand(self.deck.deal_two())
    self.player_hand = Hand(self.deck.deal_two())
    

  def print_player_hand(self):
    if self.player_hand.is_bust:
      print(f"{self.player.name} has bust: {self.player_hand}")
    else:
      print(f"{self.player.name} has {self.player_hand.max_value}: {self.player_hand}")
  
  def print_dealer_hand(self, open_ = True):
    if open_:
      if self.dealer_hand.is_bust:
        print(f"Dealer has bust: {self.dealer_hand}")
      else:
        print(f"Dealer has {self.dealer_hand.max_value}: {self.dealer_hand}")
    else:
      print(f"Dealer has: {self.dealer_hand.first_card}, ?")

  def player_plays(self):
    system("clear")
    self.print_dealer_hand(open_ = False)
    self.print_player_hand()

    while True:
      if self.player_hand.is_bust or self.player_hand.is_21:
        break

      actions = ["Hit", "Stand"]
      if self.player.balance > self._current_bet and self.player_hand.card_count == 2:
        actions.append("Double")

      action = self.get_player_action(actions)
      if action == "Hit":
        self.hit()
      elif action == "Double":
        self.double()
        break
      else:
        break
    
  def get_player_action(self, actions):
    actions_str = ", ".join(actions[:-1]) + " or " + actions[-1]
    action_inputs = [action[0] for action in actions]

    print(f"Would you like to {actions_str}?")
    action = input(">> ")[0].upper()
    while action not in action_inputs:
      print(f"Please input {actions_str}:")
      action = input(">> ")[0].upper()

    return actions[action_inputs.index(action)]
  
  def hit(self):
    new_card = self.deck.deal_one()
    self.player_hand.add_card(new_card)
    self.print_player_hand()

  def double(self):
    self.player.deduct_bet(self._current_bet)
    self._current_bet *= 2
    print(f"Bet raised to ${self._current_bet}.")
    self.hit()

  def dealer_plays(self):
    self.print_player_hand()
    print("\nDealer's turn:")
    self.print_dealer_hand()
    while self.dealer_hand.max_value < 17 and not self.dealer_hand.is_bust:
      new_card = self.deck.deal_one()
      self.dealer_hand.add_card(new_card)
      self.print_dealer_hand()

  def update_for_winner(self, winner):
    print("\n")
    if winner == "Dealer":
      print(f"Unlucky.  Balance now ${self.player.balance}")
    elif winner == "Player":
      multiplier = 1.5 if self.player_hand.is_natural else 1
      winnings = self._current_bet * multiplier
      self.player.add_winnings(self._current_bet + winnings)
      print(f"Congrats, you won ${winnings}.  Balance now ${self.player.balance}")
    else:
      self.player.add_winnings(self._current_bet)
      print(f"That's a push. Balance now ${self.player.balance}")

  def game_over(self):
    if self.player.balance == 0:
      return True
    else:
      return self.get_if_player_continues()
  
  def get_if_player_continues(self):
    play_again = input("Want to go again (Y/N)? ").upper().strip()[0]
    while play_again not in ["Y", "N"]:
      play_again = input("Want to go again (Y/N)? ").upper().strip()[0]
    system("clear")
    return play_again == "N"
  
  def end(self):
    message = ""
    net_cash = abs(self.player.net_win_loss)

    if self.player.net_win_loss < 0:
      message = f"Unlucky! But thanks for the ${net_cash} you lost..."
    elif self.player.net_win_loss > 0:
      message = f"Congrats! You won ${net_cash}. Grr..."
    else:
      message = f"You broke even ... Congrats I guess."

    print(message)
  