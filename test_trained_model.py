import tensorflow as tf
from tensorflow import keras

import numpy as np
import os

from Agent import Agent
from Game import Game

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

game = Game(9)

qfunction = keras.models.load_model('trained_model')

agent = Agent()

wins = 0
N = 10000
for ii in range(N):
    game.reset(display=0) 

    while game.done == False:
        if game.player == 0:
            state = tf.experimental.numpy.atleast_2d(game.state.astype('float32'))
            Q = qfunction(state)
            actionMask = np.array([(i%6 in game.validCard[game.player]) and (i//6 in game.validStone[game.player]) for i in range(54)])
            action = np.argmax(Q*actionMask)
        else:
            action = agent.action(game.validCard[game.player], game.validStone[game.player])

        game.step(action)
    if game.winner == 0:
        wins += 1
        
    if ii % 100 == 99:
        print('Test iteration # '+str(ii+1)+' done')
print('Evaluated win rate : '+str(wins/N))
