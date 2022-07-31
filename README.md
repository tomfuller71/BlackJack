# BlackJack
Simple Terminal based Black Jack game.
## New in V3:
  - Player can buy "Insurance" if Dealer has open showing Ace on the deal.
  - Allow terminal args for options:
    - -n, --bet_min: The table's minimum bet.
    - -x, --bet_max: The tables initial bet limit.
    - -s --shoe_count: The number of decks in the dealing shoe.


## New in v2
  - Player can split pair with matched bet. Can only split once. No "natural" bonus for splits.
  - Clear terminal on transitions from betting to playing a hand.
  - Increased info shown to user.

## v1:
- Player enters name and then the initial amount of chips they want to buy.
- Player goes first.
  - Player inputs the bet amount (limit of their balance).
  - Player can Hit, Stand or Double depending on state of hand and his chip balance.
  - If player doubles down, they double their initial bet and then only get one hit.
  - If player busts then Dealer automatically wins.
  
- Dealer plays next:
    - Dealer must hit on less than 17, must stick on 17 or more.
    
- If player wins the hand with a "Natural" (10 value card and an Ace) then 1.5 x on pay out.
- Push on dealer and player having same result

## To do in V4:
  - Have "Clue" option that present optimal choice for player based on strategy tables.
