# implementation of card game - Memory    Author:  Thomson Kneeland
# uses Codeskulptor interface and simplegui (not stand alone GUI)
# User can select two cards at a time; Goal is to find all pairs in least number of tries
# which is tracked on left

import simplegui
import random
sequence = []
exposed = []
state = 0
card_num1 = []
card_num2 = []
card_pos1 = []
card_pos2 = []
counter = 0

# helper function to initialize globals
def new_game():
    global sequence, counter, state, exposed
    sequence = range(8)
    sequence.extend(range(8))
    random.shuffle(sequence)
    exposed = []
    for x in range(16):
        exposed.append(0)
    counter = 0
    state = 0
     
# define event handlers
def mouseclick(pos):
    global exposed, state, sequence, card_num1, card_num2, card_pos1, card_pos2, counter
    card = pos[0]//50  ## find position of click
    #initial state of game
    if state == 0 and exposed[card] == 0:
        card_pos1 = card
        exposed[card] = 1
        state = 1
        card_num1 = sequence[card]
    # second card picked    
    if state == 1 and exposed[card] == 0:
        card_pos2 = card
        exposed[card] = 1
        state = 2
        card_num2 = sequence[card]
        counter += 1
    # 3rd card picked, match found    
    if state == 2 and exposed[card] == 0 and (card_num1 == card_num2):
        card_pos1 = card
        exposed[card] = 1
        state = 1
        card_num1 = sequence[card]
        card_num2 = []
    # 3rd card picked, match not found    
    if state == 2 and exposed[card] == 0 and (card_num1 != card_num2):
        exposed[card_pos1] = 0
        exposed[card_pos2] = 0
        card_pos1 = card
        exposed[card] = 1
        state = 1
        card_num1 = sequence[card]
        card_num2 = []
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = "+str(counter))
    global sequence
    for num in range(len(sequence)):
        if exposed[num] == 1:
            canvas.draw_text(str(sequence[num]), (8 +50*num, 75), 70, 'Red')
        elif exposed[num] == 0:
            canvas.draw_polygon([(num*50, 100), (50+num*50, 100),
                                 (50+num*50, 0), (num*50,0) ], 3,'Black','Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
