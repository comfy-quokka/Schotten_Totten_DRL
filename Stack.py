class Stack:
    def __init__(self):
        self.cards = []  # An empty list to store the cards in the stack.
        self.combination = 0  # The combination type of the cards in the stack.
        self.length = 0  # The number of cards in the stack.
        self.sum = 0  # The sum of the values of the cards in the stack.

    def append(self, card):
        # Add the given card to the stack.
        self.cards.append(card)
        self.cards = sorted(self.cards, key=lambda x: (x[0],x[1]))
        # Increment the length of the stack by 1.
        self.length += 1
        # Add the value of the card to the sum.
        self.sum += card[0]
        # Update the combination type of the stack.
        self.updateCombination()

    def updateCombination(self):
        # Update the combination type based on the cards in the stack.
        if self.isSum():
            self.combination = 0  # Combination type: Sum of values.
        if self.isStraight():
            self.combination = 1  # Combination type: Straight.
        if self.isColor():
            self.combination = 2  # Combination type: Color.
        if self.isBrelan():
            self.combination = 3  # Combination type: Brelan (Three of a kind).
        if self.isColorStraight():
            self.combination = 4  # Combination type: Color Straight.

    def isSum(self):
        # Check if there is at least one card in the stack.
        return len(self.cards) > 0

    def isStraight(self):
        # Check if there are exactly three cards in the stack and they form a straight sequence.
        return len(self.cards) == 3 and \
               self.cards[0][0] == self.cards[1][0] - 1 == self.cards[2][0] - 2

    def isColor(self):
        # Check if all the cards in the stack have the same color (suit).
        return len(self.cards) == 3 and all([True if card[1] == self.cards[0][1] else False for card in self.cards])

    def isBrelan(self):
        # Check if there are exactly three cards in the stack and they have the same value.
        return len(self.cards) == 3 and all(
            [True if card[0] == self.cards[0][0] else False for card in self.cards])

    def isColorStraight(self):
        # Check if the stack is both a color and a straight.
        return self.isColor() and self.isStraight()
