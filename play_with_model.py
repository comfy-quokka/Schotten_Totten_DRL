import tensorflow as tf
from tensorflow import keras

import numpy as np
import os

from Agent import Agent
from Game import Game


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

game = Game(9)
# display = 0 to hide the game status
# display = 1 to display the game status with clear screen
# display = 2 to display the game status without clear screen

qfunction = keras.models.load_model('trained_model')

agent = Agent()

wins = 0
N = 1
for ii in range(N):
    game.reset(display=1) 

    while game.done == False:
        if game.player == 0:
            state = tf.experimental.numpy.atleast_2d(game.state.astype('float32'))
            Q = qfunction(state)
            actionMask = np.array([(i%6 in game.validCard[game.player]) and (i//6 in game.validStone[game.player]) for i in range(54)])
            action = np.argmax(Q*actionMask)
        else:
            card = int(input('Select the card to play: '))
            stone = int(input('Select the card to play: '))
            action = card-1+(stone-1)*6

        game.step(action)
    if game.winner == 0:
        wins += 1
        
