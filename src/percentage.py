from random import randint

class Percentage:
    def __init__(self, percentage: int):
        self.percentage = percentage

    def roll(self) -> bool:
        return randint(0, 100) <= self.percentage
    
    def __float__(self) -> float:
        return self.percentage / 100