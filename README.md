# StuyTCG by Senioritis
## Roster: Tudor Ganshaw (pm), Amy Shrestha, Steven Wu, Hannah Grimskog-Tran

## Summary
StuyTCG is web-based trading card game (TCG) themed around Stuyvesant. Users will be able to pull cards, show off their collections, and battle other users using teacher cards from different departments. Cards will have 4 values: HP, Attack (or Special), Defense, and Speed. Users can also tour the card encyclopedia of 24 cards, where users can choose their starting 8 cards (they can choose at most 2 of a card). Out of those 8 cards, users will keep 5 on hand, one of which will be the active card in battle, and 3 cards in the deck. If a card has 0 or less HP remaining, that card is “KO’d” and goes into the user’s discard pile. The user must then select a new card from their hand to become their active card, and pull a new card from their deck into their hand. One side wins when the other player no longer has any cards left to play.

#### Visit our live site at [senioritis.dev](https://senioritis.dev)  

## Install Guide
1) Clone the repository into a local directory:
```
git clone git@github.com:tganshaw/senioritis__tudorg_amys90_hannah61_stevenw92.git senioritis
```
2) Enter the cloned repository directory:
```
cd senioritis
```
3) Create a virtual environment:
```
python3 -m venv venv
```
4) Activate the virtual environment for Linux, Windows, or Mac:

  a. Linux
  ```
  . venv/bin/activate
  ```
  b. Windows
  ```
  venv\Scripts\activate
  ```
  c. Mac
  ```
  source venv/bin/activate
  ```
5) Install necessary modules:
```
pip install -r requirements.txt
```

## Launch codes
1) Cd into app folder:
```
cd senioritis/app
```
2) Run `__init__.py`
```
python3 __init__.py
```