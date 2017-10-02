# Pong City
# Author: Thomson Kneeland
# Program uses GUI interface provided by Codeskulptor and does not stand alone (see screenshots)
# implementation of pong program, keeping track of scores for both players
#  player 1 uses 'w' and 's' keys to manipulate paddle
#  player 2 uses 'up' and 'down' keys to manipulate paddle
# ball velocity increases with each paddle strike

import simplegui
import random

# initialize globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball position and velocity for start of game
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]
ball_vel[0] = random.randrange(120,240)/60
ball_vel[1] = -random.randrange(60,180)/60
direction = LEFT

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_vel[0] = random.randrange(125,245)/60
    ball_vel[1] = -random.randrange(65,185)/60
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel[0] *= -1
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    ball_pos = [WIDTH/2, HEIGHT/2]
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(0)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, P1_win, P2_win, direction
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball 
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # upper and lower borders
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] *= -1
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1  
        
    # determine if ball hits gutters or paddles
    # left paddle and gutter
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS) and ((paddle1_pos +HALF_PAD_HEIGHT >= ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT)):
        ball_vel[0] *= -1.1  
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS) and ((ball_pos[1] < paddle1_pos - HALF_PAD_HEIGHT) or ball_pos[1] > (paddle1_pos + HALF_PAD_HEIGHT)):
            score2 += 1
            spawn_ball(LEFT)
    # right paddle and gutter     
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS) and ((paddle2_pos + HALF_PAD_HEIGHT >= ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT)):
        ball_vel[0] *= -1.1
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS) and ((ball_pos[1] < paddle2_pos - HALF_PAD_HEIGHT) or ball_pos[1] > (paddle2_pos + HALF_PAD_HEIGHT)):
            score1 += 1
            spawn_ball(RIGHT)       
   
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "Green")
    
    # update paddles' vertical positions
    if (paddle1_pos <= HEIGHT - PAD_HEIGHT/2 and paddle1_vel>0) or (paddle1_pos >= PAD_HEIGHT/2 and paddle1_vel <0):
        paddle1_pos += paddle1_vel
    if (paddle2_pos <= HEIGHT - PAD_HEIGHT/2 and paddle2_vel>0) or (paddle2_pos >= PAD_HEIGHT/2 and paddle2_vel <0):
        paddle2_pos += paddle2_vel     
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos + HALF_PAD_HEIGHT], [0, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]], 1, 'Orange', 'Orange')
    canvas.draw_polygon([[WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH-PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH-PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], 1, 'Orange', 'Orange')
    
    # draw scores
    canvas.draw_text("Player 1:  " + str(score1) +"           Player 2:  "+
                     str(score2), [120,50], 30, "Red")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 7
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 7
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 7  
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 7    
       
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:  
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:  
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["s"]:  
        paddle1_vel = 0   
    if key == simplegui.KEY_MAP["down"]:  
        paddle2_vel = 0    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
Rematch = frame.add_button("Restart Match!", new_game)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
