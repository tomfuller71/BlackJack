from card import Card
from random import shuffle

class Deck:
  suits = ["❤", "♠︎", "♣︎", "♣︎"]
  faces = ["A", "K", "Q", "J"] + [str(i) for i in range(2,11)]

  @classmethod
  def make_deck(cls):
    deck = []
    for suit in cls.suits:
      for face in cls.faces:
        deck.append(Card(face, suit))
    shuffle(deck)
    return deck
  
  def __init__(self):
    self.cards = Deck.make_deck()
    
  def deal_one(self):
    if self.count == 0:
      self.cards = self.make_deck()

    return self.cards.pop()

  def deal_two(self):
    return [self.deal_one(), self.deal_one()]

  @property
  def count(self):
    return len(self.cards)