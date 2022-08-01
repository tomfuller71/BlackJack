class Hand:
  def __init__(self, deal, bet = 0, id = 1):
    self._cards = deal
    self._hard_value = deal[0].value + deal[1].value
    self._soft_value = deal[0].alt_value + deal[1].alt_value
    self.bet = bet
    self.id = id
    self._hand_value_progression = [
      max(deal[0].value, deal[0].alt_value),
      max(self._hard_value, self._soft_value)
    ]
  
  def add_card(self, card):
    self._cards.append(card)
    self._hard_value += card.value
    self._soft_value += card.alt_value
    self._hand_value_progression.append(self.max_value)

  def first_n_cards_str(self, n):
    return ", ".join(str(card) for card in self._cards[:n])

  def sum_of_cards(self, n):
    ace_high = sum([card.value for card in self._cards[: n]])
    ace_low = sum([card.alt_value for card in self._cards[: n]])
    return max(ace_high, ace_low)

  def pop_card(self):
    card = self._cards.pop()
    self._hard_value -= card.value
    self._soft_value -= card.alt_value
    return card

  @property
  def max_value(self):
    max_value = 0
    if self._hard_value <= 21:
      max_value = self._hard_value
    if self._soft_value <= 21 and self._soft_value > max_value:
      max_value = self._soft_value
    return max_value
  
  @property
  def is_bust(self):
    return self._hard_value > 21 and self._soft_value > 21
  
  @property
  def is_21(self):
    return self.max_value == 21
  
  @property
  def card_count(self):
    return len(self._cards)
  
  @property
  def is_natural(self):
    return self.is_21 and self.card_count == 2
  
  @property
  def first_card(self):
    return self._cards[0]
  
  @property
  def second_card(self):
    return self._cards[1]

  @property
  def last_card(self):
    return self._cards[-1]

  @property
  def first_is_Ace(self):
    return self._cards[0].value == 1
  
  @property
  def is_split(self):
    return (
      self.card_count == 2
      and self._cards[0].value == self._cards[1].value
    )
  
  @property
  def is_soft(self):
    return self._soft_value != self._hard_value
    
  def __repr__(self):
    return ", ".join(str(card) for card in self._cards)