"""
Author: OsaO
Date Created: 19/05/2024

Last Updated By:
Last Updated Date: 

Summary: 
"""
from random import choices
import matplotlib.pyplot as plt
import numpy as np
import threading

class RiskSimulation:
    """
    Defines risk simulation class, which takes in required dynamic parameters relating to a potential equity curve 
    """
    def __init__(self, balance, winrate, riskPercentage, riskReward, noTrades, noSimulations):
        # Assigns Variables
        self.balance = balance
        self.winrate = winrate
        self.riskPercentage = riskPercentage
        self.riskReward = riskReward
        self.noTrades = noTrades
        self.noSimulations = noSimulations

        # An array storing the balace tracking arrays for each simulation performed
        self.outcomes = []

    def main(self):
        """
        Uses the imported class variables to plot equity curve(s)
        """

        # Threading used to run number of simulations simultaneously
        threads = []

    def runSimulation(self, balance):
        # Runs simulation

        """
        To determine is a trade is a win or loss, it used a list of 100 items, 
        where the items in the list are either a win or a loss.

        A random item is then chosen from the list
        - W = Winning trade
        - L = Losing trade
        """

        # Adds starting balance to balance tracking list
        balanceTracking = [balance]

        for i in range(self.noTrades):
            outcome = (choices(["W","L"], weights=[self.winrate, (1-self.winrate)], k=1))[0]
            PnL = 0

            if outcome == "W":
                # Winning trade
                PnL = (balance * (self.riskPercentage/100)) * self.riskReward
                balance = balance + PnL # Winning trade, so PnL increases
            else:
                #outcome = "L" -> Losing trade
                PnL = (balance * (self.riskPercentage/100))
                balance = balance - PnL # Losing trade so PnL reduces

            # Appends new balance to tracking list  
            balanceTracking.append(balance)
        
        (self.outcomes).append(balanceTracking)


        