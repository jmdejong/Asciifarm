
class Heal:
    
    def __init__(self, interval, amount=1):
        """ interval is the number of steps until next healing, amount is the amount of health that gets added in a healing """
        self.interval = interval
        self.amount = amount
        self.nextHeal = None
