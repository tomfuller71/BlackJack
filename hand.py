class Hand:
  def __init__(self, deal):
    self._cards = deal
    self._hard_value = deal[0].value + deal[1].value
    self._soft_value = deal[0].alt_value + deal[1].alt_value
  
  def add_card(self, card):
    self._cards.append(card)
    self._hard_value += card.value
    self._soft_value += card.alt_value

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
  def first_is_Ace(self):
    return self._cards[0].value == 1
    
  def __repr__(self):
    return ", ".join(str(card) for card in self._cards)