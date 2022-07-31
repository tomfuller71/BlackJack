from logging import critical
from tracemalloc import start
from deck import Deck
from hand import Hand
from os import system
class BlackJack:
  def __init__(self, player):
    self.deck = Deck()
    self.player = player
    self.natural_bonus = 0.5
    self.player_hands = []

  def play(self):
    system("clear")
    print("Starting game ...")

    while True:
      self.play_hand()
      if self.game_over():
        break

    self.end()

  # Play methods
  def play_hand(self):
    # out of order from physical as deal and dealer result are independent
    self.deal()
    self.get_dealer_result()

    self.player_bet()
    self.print_player_hands()
    self.player_plays()
    self.print_dealer_progression()
    self.score_player_hands()
    print(f"\nBalance now ${self.player.balance}.")

  def deal(self):
    self.dealer_hand = Hand(self.deck.deal_two())
    self.player_hands = [Hand(self.deck.deal_two())]

  def get_dealer_result(self):
    while self.dealer_hand.max_value < 17 and not self.dealer_hand.is_bust:
      self.dealer_hand.add_card(self.deck.deal_one())

  def print_dealer_playing(self):
      print("\nDealer's turn:")
      self.print_dealer_hand()

  def player_bet(self):
      print(f"Balance: ${self.player.balance}")
      bet = int(input("How much do you want to bet? "))
      system("clear")

      while bet > self.player.balance:
        print("You don't have that much!")
        bet = int(input("How much do you want to bet? "))
        system("clear")

      self.player.deduct_bet(bet)
      self.player_hands[0].bet = bet

  def player_plays(self):
    self.check_for_splits()

    for hand in self.player_hands:
      while not (hand.is_bust or hand.is_21) :
        system("clear")
        print(f"Dealer has: {self.dealer_hand.first_card}")
        self.print_player_hands()

        action = self.get_player_action(hand)
        if action == "Hit":
          self.hit(hand)
        elif action == "Double":
          self.double(hand)
          break
        else:
          break
  
  def score_player_hands(self):
    for hand in self.player_hands:
      winner = ""
      if hand.is_bust:
        winner = "Dealer"
      else:
        if self.dealer_hand.is_bust:
          winner = "Player"
        elif self.dealer_hand.max_value > hand.max_value:
          winner = "Dealer"
        elif self.dealer_hand.max_value < hand.max_value:
          winner = "Player"
        else:
          winner = "Push"
          
      self.update_for_winner(hand, winner)

  # Player sub methods
  def check_for_splits(self):
    if self.player_hands[0].is_split and self.player_splits():
      self.split_cards()

  def hit(self, hand):
    new_card = self.deck.deal_one()
    hand.add_card(new_card)

  def double(self, hand):
    self.player.deduct_bet(hand.bet)
    hand.bet *= 2
    print(f"Bet raised to ${hand.bet}.")
    self.hit(hand)

  def update_for_winner(self, hand, winner):
    print("\n")
    if len(self.player_hands) > 1:
      print(f"For hand {hand.id}:")
    if winner == "Dealer":
      print(f"Dealer wins.")
    elif winner == "Player":
      original_bet = hand.bet
      winnings = original_bet * 2
      if (len(self.player_hands) == 1 and hand.is_natural):
        winnings += original_bet * self.natural_bonus

      self.player.add_winnings(winnings)
      print(f"Congrats, you won and made ${winnings - original_bet}.")
    else:
      self.player.add_winnings(hand.bet)
      print(f"That's a push.")

  def game_over(self):
    if self.player.balance == 0:
      return True
    else:
      return self.get_if_player_continues()

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
  
  # Helper functions
  def player_splits(self):
    split = input("Do you want to split (Y/N)? ")[0].upper()
    while split not in ["Y", "N"]:
      split = input("Enter Y or N: ")[0].upper()
    return split == "Y"

  def split_cards(self):
    first_hand = self.player_hands[0]
    split_card = first_hand.pop_card()
    bet = first_hand.bet

    self.player.deduct_bet(bet)

    new_card_1, new_card_2 = self.deck.deal_two()
    first_hand.add_card(new_card_1)

    second_hand = Hand([split_card, new_card_2], bet, 2)
    self.player_hands.append(second_hand)

  def print_player_hands(self):
    for hand in self.player_hands:
      hand_index = "Current hand"
      if len(self.player_hands) > 1:
        hand_index = f"Hand {hand.id}"
      
      score = "bust" if hand.is_bust else str(hand.max_value)
      print(f"{hand_index}, bet ${hand.bet}, has {score}: {hand}")
   
  def print_dealer_progression(self):
    if self.all_player_hands_bust():
      return 

    print("\n")

    for index, max_value in enumerate(
      self.dealer_hand._hand_value_progression
      ):
      cards_str = self.dealer_hand.first_n_cards_str(index + 1)
      if max_value == 0:
        print(f"Dealer busted: {cards_str}")
      else:
        print(f"Dealer has {max_value}: {cards_str}")
  
  def get_player_action(self, hand):
    start_str = "\n"
    if len(self.player_hands) > 1:
      start_str = f"\nHand {hand.id}: "

    actions = self.get_allowable_actions(hand)
    actions_str = ", ".join(actions[:-1]) + " or " + actions[-1]
    action_inputs = [action[0] for action in actions]
    action = input(f"{start_str}Would you like to {actions_str}?")[0].upper()
    while action not in action_inputs:
      print(f"Please input {actions_str}:")
      action = input(">> ")[0].upper()

    return actions[action_inputs.index(action)]
  
  def get_allowable_actions(self, hand):
    actions = ["Hit", "Stand"]
    if self.player.balance >= hand.bet and hand.card_count == 2:
       actions.append("Double")
    return actions

  def get_if_player_continues(self):
    play_again = input("Want to go again (Y/N)? ").upper().strip()[0]
    while play_again not in ["Y", "N"]:
      play_again = input("Want to go again (Y/N)? ").upper().strip()[0]
    system("clear")
    return play_again == "N"
  
  def all_player_hands_bust(self):
    for hand in self.player_hands:
      if not hand.is_bust:
        return False
    return True