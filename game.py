from os import system

from deck import Deck
from hand import Hand
from question import Question
from strategy import strategy


class BlackJack:
  def __init__(self, player, bet_min, bet_max, shoe_count):
    self.deck = Deck(shoe_count)
    self.player = player
    self.natural_bonus = 0.5
    self.player_hands = []
    self.bet_min = bet_min
    self.bet_max = bet_max

  def play(self):
    system("clear")
    print(f"Welcome, {self.player.name}.")
    print(f"This table's minimum bet in ${self.bet_min:.2f} and maximum is ${self.bet_max:.2f}.  Good luck!")

    while True:
      self.play_hand()
      if self.game_over():
        break
      else:
        system("clear")

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
    print(self.player)

  def deal(self):
    self.dealer_hand = Hand(self.deck.deal_two())
    self.player_hands = [Hand(self.deck.deal_two())]

  def get_dealer_result(self):
    while self.dealer_hand.max_value < 17 and not self.dealer_hand.is_bust:
      self.dealer_hand.add_card(self.deck.deal_one())

  def player_bet(self):
    print(self.player)
    limit = min(self.player.balance, self.bet_max)

    bet = Question.get_numeric_response(
      "How much do you want to bet?",
      min=self.bet_min,
      max=limit,
      num_type=float
    )

    self.player.deduct_bet(bet)
    self.player_hands[0].bet = bet

  def player_plays(self):
    for hand in self.player_hands:
      action_taken = ""
      while True :
        system("clear")
        print(f"Dealer has: {self.dealer_hand.first_card}\n")

        if action_taken:
          self.print_action_taken(action_taken, hand)
        
        self.print_player_hands()

        if (
          (hand.is_bust or hand.is_21)
           or (action_taken in ["Double", "Stand"])
        ):
          break

        action_taken = self.get_player_action(hand)
        if action_taken == "Hit":
          self.hit(hand)
        elif action_taken == "Double":
          self.double(hand)
        elif action_taken == "Pair-Split":
          self.split_cards(hand)
        elif action_taken == "Insurance":
          self.insurance(hand)
  
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
  
  def split_cards(self, hand):
    split_card = hand.pop_card()
    bet = hand.bet

    self.player.deduct_bet(bet)

    new_card_1, new_card_2 = self.deck.deal_two()
    hand.add_card(new_card_1)

    new_hand = Hand([split_card, new_card_2], bet, 2)
    self.player_hands.append(new_hand)
  
  def hit(self, hand):
    new_card = self.deck.deal_one()
    hand.add_card(new_card)

  def double(self, hand):
    self.player.deduct_bet(hand.bet)
    hand.bet *= 2
    print(f"Bet raised to ${hand.bet}.")
    self.hit(hand)
  
  def insurance(self, hand):
    insurance_cost = hand.bet / 2
    self.player.deduct_bet(insurance_cost)
    self.dealer_hand.insurance = insurance_cost

  def update_for_winner(self, hand, winner):
    self.check_insurance()

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

    print("\n")

  def game_over(self):
    if self.player.balance == 0:
      return True
    else:
      return not Question.get_bool_YN_response("Want to go again (Y/N)?")

  def end(self):
    message = ""
    net_cash = abs(self.player.net_win_loss)

    if self.player.net_win_loss < 0:
      message = f"Unlucky! But thanks for the ${net_cash: .2f} you lost..."
    elif self.player.net_win_loss > 0:
      message = f"Congrats! You won ${net_cash: .2f}. Grr..."
    else:
      message = f"You broke even ... Congrats I guess."

    print(message)

  # Helper functions

  def print_player_hands(self):
    if hasattr(self.dealer_hand, "insurance"):
      print(f"Insurance taken: ${self.dealer_hand.insurance}\n")

    for hand in self.player_hands:
      hand_index = "Current hand"
      if len(self.player_hands) > 1:
        hand_index = f"Hand {hand.id}"
      
      score = "bust" if hand.is_bust else str(hand.max_value)
      print(f"{hand_index}:")
      print(f"Bet ${hand.bet:.2f}.  Score {score}. Cards: {hand}\n")
   
  def print_dealer_progression(self):
    if self.all_player_hands_bust():
      return 

    for index, max_value in enumerate(self.dealer_hand._hand_value_progression):
      if index == 0:
        continue

      cards_str = self.dealer_hand.first_n_cards_str(index + 1)
      if max_value == 0:
        print(f"Dealer busted: {cards_str}")
      else:
        print(f"Dealer has {max_value}: {cards_str}")
    print("\n")
  
  def get_player_action(self, hand):
    start_str = "\n"
    if len(self.player_hands) > 1:
      start_str = f"\nHand {hand.id}: "

    actions = self.get_allowable_actions(hand)
    question = f"{start_str}Would you like to {', '.join(actions[:-1])} or {actions[-1]}?"

    return Question.get_response_from_list(question, actions)
  
  def get_allowable_actions(self, hand):
    actions = ["Hit", "Stand"]

    if hand.card_count == 2:
      actions.append("Clue")

      if self.player.balance >= hand.bet and hand.is_split:
        actions.append("Pair-Split")
        
      if self.player.balance >= hand.bet:
        actions.append("Double")

      if (not self.insurance_taken()
        and len(self.player_hands) == 1
        and self.dealer_hand.first_is_Ace
        ):
        actions.append("Insurance")

    return actions

  def all_player_hands_bust(self):
    for hand in self.player_hands:
      if not hand.is_bust:
        return False
    return True

  def check_insurance(self):
    if self.insurance_taken():
      if self.dealer_hand.second_card.value == 10:
        payout = self.dealer_hand.insurance * 2
        self.player.add_winnings(payout)
        print(f"Insurance pays ${payout}.")
      else:
        print("Insurance lost.")

  def insurance_taken(self):
    return hasattr(self.dealer_hand, "insurance")

  def print_action_taken(self, action, hand):
    if action == "Double":
      print(f"Double down. Bet raised to ${hand.bet:.2f}.")
    elif action == "Pair-Split":
      print("You split your pair.")
    elif action == "Hit":
      print("Hitting.")
    elif action == "Insurance":
      print("You took insurance on dealer having Black Jack.")
    elif action == "Clue":
      print(f"Recommended action is: {self.get_strategy(hand)}")
    else:
      print("Standing.")

    if action in ["Double", "Hit"]:
      print(f"You got a {hand.last_card}.")

    print("\n")

  def get_strategy(self, hand):
    picture_cards = ["K", "Q", "J"]

    key = self.dealer_hand.first_card._face
    if key in picture_cards:
      key = str(10)

    if hand.is_split:
      split_face = hand.first_card._face
      if split_face in picture_cards:
        split_face = "10"
      return strategy[key]["split"][split_face]
    elif hand.is_soft:
      return strategy[key]["soft"][str(min(19, hand._soft_value))]
    else:
      hard_value = hand._hard_value
      if hard_value < 8:
        hard_value = 8
      if hard_value > 17:
        hard_value = 17
      return strategy[key]["hard"][str(hard_value)]

      