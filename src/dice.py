from random import randint

class Dice():
    def __init__(self, sides=6):
        """initiate a dice object with predefined sides"""
        self.sides = sides
    
    def roll(self):
        """give a random number between 1 and the number of sides"""
        return randint(1, self.sides)