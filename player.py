class Player:
  def __init__(self, name, initial_cash):
    self.initial_cash = initial_cash
    self.name = name
    self._cash = initial_cash
  
  def deduct_bet(self, bet):
    self._cash -= bet

  def add_winnings(self, winnings):
    self._cash += winnings

  @property
  def balance(self):
    return self._cash
  
  @property
  def net_win_loss(self):
    return self.balance - self.initial_cash

  def __repr__(self):
    return f"{self.name} has a balance of ${self._cash: .2f}."