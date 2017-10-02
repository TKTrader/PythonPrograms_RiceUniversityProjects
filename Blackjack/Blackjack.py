# Mini-project #6 - Blackjack
# Author: Thomson Kneeland
# Implements Blackjack using codeSkulptor interface from RU;
# Will not run as standalone program!
# Typical blackjack rules
# player can choose to stand or be hit with a new card
# dealer automatically hits until score >= 17 or bust
# increments score accordingly (+1 or -1)
# tie goes to dealer

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize global variables
instruction = "Hit or Stand?"
outcome = ""
in_play = False
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        self.ace = False
        self.pos = ()

    def __str__(self):
        text = "Hand Contains "
        for i in self.hand:
            text += str(i) +" "
        return text    

    def add_card(self, card):
        if card.get_rank() == 'A':
                self.ace = True 
        self.hand.append(card)

    def get_value(self):
        value = 0
        for card in self.hand:
            value += VALUES[card.get_rank()]  
        if self.ace and (value <= 11):
            value += 10
        return value   
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
   
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += 100
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle cards randomly

    def deal_card(self):
        return self.deck.pop(0)
        # deal a card object from the deck
    
    def __str__(self):
        text = "Deck Contains "
        for card in self.deck:
            text += str(card) + " "
        return text    

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, outcome, score, instruction
    # create deck and shuffle
    deck = Deck()
    deck.shuffle()
    instruction = "Hit or Stand?"
    # Player forfeits hand if Deals before hand completed
    if in_play:
        outcome = "Player Forfeits Hand"
        score -= 1        
    elif in_play == False:    
        outcome = ""
    
    ## create Hands
    player = Hand()
    dealer = Hand()
    
    # deal first round of cards
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    ## deal second round of cards
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    in_play = True
    
    #Test Code
    #print deck
    #print "Player's " + str(player)
    #print "Dealer's " + str(dealer)

def hit():
    global in_play, player, score, outcome, instruction
    outcome = ""
    instruction = "Hit or Stand?"
    
    # hit player
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
        print "Player's " + str(player)
    
    # bust player    
    if in_play and player.get_value() > 21:
        in_play = False
        score -= 1
        instruction = "New Deal?"
        outcome = "You Have Busted!!!"
        
    # Change text instructions after bust    
    if in_play == False:
        instruction = "New Deal?"
       
def stand():
    global in_play, dealer, player, score, outcome, instruction
    instruction = "New Deal?"
    # play dealer's hand, hit dealer until hand >= 17
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        print "Dealer's " + str(dealer)
        in_play = False
        #evaluate hands for winner, update outcome message and score
        if dealer.get_value() > 21:
            score += 1
            outcome = "Dealer has Busted!!"
        elif dealer.get_value() >= player.get_value():
            score -= 1
            outcome = "Dealer wins!!"
        elif dealer.get_value() < player.get_value():
            score += 1
            outcome = "Player wins!!"           
    in_play = False
    
# draw handler    
def draw(canvas):
    global player, dealer
    canvas.draw_text('Blackjack', (200, 100), 60, 'Black')
    canvas.draw_text('Wins:   ' + str(score), (350, 170), 40, 'Yellow')
    canvas.draw_text('Dealer', (100, 170), 35, 'Black')
    canvas.draw_text('Player', (100, 350), 35, 'Black')
    canvas.draw_text(instruction, (220, 525), 35, 'Yellow')
    canvas.draw_text(outcome, (300, 350), 35, 'Yellow')
    player.draw(canvas, [100,370])
    dealer.draw(canvas, [100,190])
    # draw card back on first dealer card while game in play
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [100 + CARD_BACK_CENTER[0], 190 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
