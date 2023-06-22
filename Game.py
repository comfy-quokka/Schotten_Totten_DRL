import os
import random
import numpy as np

from Stack import Stack

class Game():

    def __init__(self, stoneNumber):
        self.stoneNumber = stoneNumber
    
    def reset(self, display=0):
        # Initialize game state
        self.turn = 0

        self.display = display

        # Create a deck of cards with values ranging from 1 to 9 and suits ranging from 0 to 5
        self.deck = [(i, j) for i in range(1, 10) for j in range(6)]
        # Shuffle the deck
        random.shuffle(self.deck)

        # Initialize the stone stacks for both players
        self.stone = [[Stack() for _ in range(self.stoneNumber)],[Stack() for _ in range(self.stoneNumber)]]
        # Initialize the valid stone positions for both players
        self.validStone = [[_ for _ in range(self.stoneNumber)],[_ for _ in range(self.stoneNumber)]]
        # Initialize the first third of each stone position
        self.firstThird = [-1 for _ in range(self.stoneNumber)]
        # Initialize the stone winners for each stone position
        self.stoneWinner = [-1 for _ in range(self.stoneNumber)]

        # Initialize the players' hands
        self.hand = [[],[]]

        # Deal 6 cards to each player from the deck
        for _ in range(6):
            self.hand[0].append(self.deck.pop())
            self.hand[1].append(self.deck.pop())
        self.hand[0] = sorted(self.hand[0], key=lambda x: (x[0], x[1]))
        self.hand[1] = sorted(self.hand[1], key=lambda x: (x[0], x[1]))
        self.validCard = [[_ for _ in range(6)],[_ for _ in range(6)]]
        self.player = 0
        self.winner = None 
        self.done = False
        
        # Generate the initial game state
        self.generateState()
        
        self.reward = 0

        # Display the game status if required
        self.displayGameStatus()

        return self.state

    def step(self, action):
        # Increment the turn counter
        self.turn += 1
        
        # Initialize the reward
        self.reward = 0

        # Convert the action into card index and stone index
        cardToPlay, stoneToPlay = action%6, action//6

        # Check if the move is valid, otherwise choose a random valid move
        cardToPlay, stoneToPlay = self.isMoveValid(cardToPlay, stoneToPlay)

        # Update the game status based on the chosen move
        self.updateStatus(cardToPlay, stoneToPlay)

        # Check if a stone is completed and update the winner status
        getStone = self.updateStoneWinner(stoneToPlay)

        # Check if the game is finished
        self.isFinished()

        # Update the reward based on the game status
        self.updateReward()

        # Switch to the other player's turn
        self.player = 1 - self.player

        # Generate the new game state
        self.generateState()

        # Display the game status if required
        self.displayGameStatus()
        
        return self.state, self.reward, self.done

    def isMoveValid(self, cardToPlay, stoneToPlay):
        # Check if the chosen move is valid, otherwise choose a random valid move
        if cardToPlay not in self.validCard[self.player] or stoneToPlay not in self.validStone[self.player]:
            cardToPlay = random.choice(self.validCard[self.player])
            stoneToPlay = random.choice(self.validStone[self.player])
            # self.reward = -1000

        return cardToPlay, stoneToPlay

    def updateStatus(self, cardToPlay, stoneToPlay):
        # Remove the chosen card from the player's hand and add it to the chosen stone stack
        card = self.hand[self.player].pop(cardToPlay)
        self.stone[self.player][stoneToPlay].append(card)
        # If there are cards remaining in the deck, draw a card and add it to the player's hand
        if self.deck:
            self.hand[self.player].append(self.deck.pop())
            # Sort the player's hand
            self.hand[self.player] = sorted(self.hand[self.player], key=lambda x: (x[0], x[1]))
        # Update the valid card indices for the player
        self.validCard[self.player] = [_ for _ in range(len(self.hand[self.player]))]

    def updateStoneWinner(self, stoneToPlay):
        getStone = 0
        # Check if the chosen stone stack has reached 3 cards
        if self.stone[self.player][stoneToPlay].length == 3:
            # Remove the chosen stone stack from the valid stone positions for the player
            self.validStone[self.player].remove(stoneToPlay)
            # Check if this is the first completed third of the stone position
            if self.firstThird[stoneToPlay] == -1:
                self.firstThird[stoneToPlay] = self.player
            else:
                # Compare the active player's combination value with the component player's combination value
                active = self.stone[self.player][stoneToPlay]
                component = self.stone[self.firstThird[stoneToPlay]][stoneToPlay]

                if active.combination > component.combination:
                    # The active player's combination value is higher, update the stone winner and set getStone to 1
                    self.stoneWinner[stoneToPlay] = self.player
                    getStone = 1
                elif active.combination == component.combination and active.sum > component.sum:
                    # The combination values are equal but the active player's sum is higher, update the stone winner and set getStone to 1
                    self.stoneWinner[stoneToPlay] = self.player
                    getStone = 1
                else:
                    # The component player's combination value is higher or equal, update the stone winner with the component player
                    self.stoneWinner[stoneToPlay] = self.firstThird[stoneToPlay]
                    getStone = -1
        return getStone

    def isFinished(self):
        # Check if any player has completed a sequence of 3 stones in a row
        # for index in range(self.stoneNumber-2):
        #     winnerSet = [self.stoneWinner[index], self.stoneWinner[index+1], self.stoneWinner[index+2]]
        #     if winnerSet == [0,0,0]:
        #         self.done = True
        #         self.winner = 0
        #     elif winnerSet == [1,1,1]:
        #         self.done = True
        #         self.winner = 1
        # Check if any player has won by completing 5 stones
        if not self.winner: 
            if self.stoneWinner.count(0) == self.stoneNumber//2+1:
                self.done = True
                self.winner = 0
            elif self.stoneWinner.count(1) == self.stoneNumber//2+1:
                self.done = True
                self.winner = 1

    def generateState(self):
        # Generate the current game state as a numpy array
        fieldNumbers = np.zeros(self.stoneNumber*6)
        fieldColors = -np.ones(self.stoneNumber*6)
        handNumbers = np.zeros(6)
        handColors = -np.ones(6)
        for ii in range(2):
            for jj in range(self.stoneNumber):
                numbers = [card[0] for card in self.stone[ii][jj].cards]
                colors = [card[1] for card in self.stone[ii][jj].cards]
                index = jj*6+ii*3

                fieldNumbers[index:index+len(numbers)] = numbers
                fieldColors[index:index+len(colors)] = colors

        handNumbers[:len(self.hand[self.player])] = [card[0] for card in self.hand[self.player]]
        handColors[:len(self.hand[self.player])] = [card[1] for card in self.hand[self.player]]
        self.state = np.concatenate((fieldNumbers, handNumbers, fieldColors+1, handColors+1))
        # self.state = np.reshape(self.state, (1, -1))
        # print(self.state.shape)

    def updateReward(self):
        # Update the reward based on the game status
        # if getStone == 1:
        # self.reward += (self.stone[self.player][0].combination-self.stone[1-self.player][0].combination)*100+(self.stone[self.player][0].sum- self.stone[1-self.player][0].sum)
        # elif getStone == -1:
        #     self.reward += (self.stone[self.player][0].combination-self.stone[1-self.player][0].combination)*100+self.stone[self.player][0].sum

        if self.done:
            if self.player == self.winner:
                self.reward += 1
            else:
                self.reward -= 1
    
    def displayGameStatus(self):
        # Display the current game status
        if self.display:
            if self.display == 1:
                os.system('clear')
            print('')
            print('############################################################')
            print('')
            print('Trun # '+str(self.turn))
            print('')
            print('Deck left: '+str(len(self.deck)))
            print('')
            # print('Player 0 hand  '+str(self.hand[0]))
            print('Player 1 hand  '+str(self.hand[1]))
            print('')
            for ii in range(self.stoneNumber):
                print('stone '+str(ii+1)+'  '+str(self.stone[0][ii].cards)+' | '+str(self.stone[1][ii].cards))
            print('')
            print(self.stoneWinner)
            print('')
            if self.winner in {0,1}:
                print('-----------------')
                print('| Player '+str(self.winner)+' win! |')
                print('-----------------')
            else:
                print('Player '+str(self.player)+' turn')
            # print(self.state)
            # print(self.reward)
            # print(self.done)
            print('')
            print('############################################################')
            print('')
