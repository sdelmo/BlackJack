# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:34:09 2021

@author: Sebastian Delgado
Description: A blackjack game using OOP, blackjack uses a deck of 52 cards.
The player plays against a "dealer", placing an initial bet, trying to get closer to 21 than the dealer
If player goes above 21 it busts (loses)
If dealer goes above 21 it busts
On each turn, player can hit or stand (take a card or end turn)
Jack, Queen, and King count as 10
Aces can be either 1 or 11

"""
from random import shuffle

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck():
    def __init__(self):
        self.deck = []

        for s in suits:
            for r in ranks:
                self.deck.append(Card(r, s))

    def shuffle(self):
        shuffle(self.deck)

    def deal_one(self):
        single_card = self.deck.pop()
        return single_card

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each card object's print string
        return 'The deck has: ' + deck_comp


class Hand:
    def __init__(self):
        self.value = 0         # empty list that we append cards to
        self.cards = []           # Start a 0 keep adding till 21
        self.aces = 0             # Keep track of aces (11 or 1)

    def add_card(self, card):
        # card passed in is from deck
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:    # since an ace would add us over 21, if there is an ace
            self.value -= 10                     # substract 10 from total
            self.aces -= 1                       # substract 1 from aces


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Input how any chips you want to bet: '))
        except ValueError:
            print('You did not enter an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry your bet can't exceed", Chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal_one())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # control game loop

    while True:
        player_choice = input('Do you want to hit or stand: ')
        if player_choice[0].lower() == 'h':
            hit(deck, hand)
        elif player_choice[0].lower() == 's':
            playing = False
        else:
            print('Sorry, please try again')
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    print('PLayer busts')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    chips.win_bet()
    print('Player wins')


def dealer_busts(player, dealer, chips):
    print('Dealer busts a nut!')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('Dealer wins')
    chips.lose_bet()


def push(player, dealer):
    print('Dealer and player tie!, its a push')


while True:
    print('Welcome to sebs blackjack extravaganza, get as close to 21 as you \n\
    can without going over. aces count as 1 or 11')

    # Create a deck instance
    NewDeck = Deck()
    # Shuffle the deck
    NewDeck.shuffle()

    # Create hand instance for player, and deal him two cards
    player_hand = Hand()
    player_hand.add_card(NewDeck.deal_one())
    player_hand.add_card(NewDeck.deal_one())
    # Create hand instance for dealer, and deal him two cards
    dealer_hand = Hand()
    dealer_hand.add_card(NewDeck.deal_one())
    dealer_hand.add_card(NewDeck.deal_one())

    # Set up some chips for the player

    player_chips = Chips()

    # Take a bet from the player

    take_bet(player_chips)

    # Show the player's two cards, and only one card from dealer

    show_some(player_hand, dealer_hand)

    while playing:
        hit_or_stand(NewDeck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(NewDeck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    print("\nPlayer's winnings stand at", player_chips.total)

    new_game = input("Would you like to play another hand, enter y or n: ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thanks for playing')
        break
