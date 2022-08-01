from card import Card
from random import shuffle

class Deck:
  suits = ["❤", "♠︎", "♣︎", "♣︎"]
  faces = ["A", "K", "Q", "J"] + [str(i) for i in range(2,11)]

  @classmethod
  def make_deck(cls, shoe_count):
    deck = []
    for _ in range(shoe_count):
      for suit in cls.suits:
        for face in cls.faces:
          deck.append(Card(face, suit))
    shuffle(deck)
    return deck

  def __init__(self, shoe_count):
    self.shoe_count = shoe_count
    self.cards = Deck.make_deck(self.shoe_count)
    
  def deal_one(self):
    if self.count == 0:
      self.cards = self.make_deck(self.shoe_count)

    return self.cards.pop()

  def deal_two(self):
    return [self.deal_one(), self.deal_one()]

  @property
  def count(self):
    return len(self.cards)
  
  # @classmethod
  # def test_split_deck(cls):
  #   deck = []
  #   deck.append(Card("6","❤" ))
  #   deck.append(Card("7","❤" ))
  #   deck.append(Card("8","❤" ))
  #   deck.append(Card("9","❤" ))
  #   deck.append(Card("10","❤" ))
  #   deck.append(Card("J","❤" ))
  #   deck.append(Card("Q","❤" ))
  #   deck.append(Card("K","❤" ))
  #   deck.append(Card("3","❤" ))
  #   deck.append(Card("2","❤" ))
  #   return deck
  