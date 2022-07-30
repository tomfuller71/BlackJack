class Card:
  def __init__(self, face, suit):
    self._face = face
    self._suit = suit
  
  def __repr__(self):
    return self._face + self._suit
  
  @property
  def value(self):
    if self._face in ["10", "J", "Q", "K"]:
      return 10
    elif self._face == "A":
      return 1
    else:
      return int(self._face)

  @property
  def alt_value(self):
    if self._face == "A":
      return 11
    else:
      return self.value