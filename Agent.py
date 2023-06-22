import random

class Agent():
    def __init__(self):
        pass

    def action(self, validCard, validStone):
        # Randomly select a card to play from the validCard list.
        cardToPlay = random.choice(validCard)
        # Randomly select a stone position to play from the validStone list.
        stoneToPlay = random.choice(validStone)
        # Calculate the action index by multiplying cardToPlay by 9 and adding stoneToPlay.
        return cardToPlay + stoneToPlay*6