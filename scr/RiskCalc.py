"""
Author: OsaO
Date Created: 19/05/2024

Last Updated By: OsaO
Last Updated Date: 19/05/2024

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
        self.startBalance = balance
        self.winrate = winrate
        self.riskPercentage = riskPercentage
        self.riskReward = riskReward
        self.noTrades = noTrades
        self.noSimulations = noSimulations

        # An array storing the balace tracking arrays for each simulation performed
        self.outcomes = []

        self.main()

    def main(self):
        """
        Uses the imported class variables to plot equity curve(s)
        """

        # Threading used to run number of simulations simultaneously
        threads = []

        for i in range(self.noSimulations):
            t = threading.Thread(target=self.FixedRisk(self.startBalance))
            threads.append(t)

        # Starts all threads
        for x in threads:
            x.start()

        # Waits for all threads to finish
        for x in threads:
            x.join()
        
        # All threads should be completed by this point

        # Gets list of xValues used to plot graph
        # xValues = number of trades, so generates list starting from 0 to number of trades with a step of 1
        xValues = np.arange(0, self.noTrades+1, 1).tolist()

        # Plots each of the outcomes
        for outcome in self.outcomes:
            plt.plot(xValues, outcome)
    
        # Sets chart environemnt
        plt.xlabel('Number of Trades')
        plt.ylabel('Account Balance')
        plt.grid('on')
        plt.show()

    def FixedRiskSim(self, accBalance):
        """
        Fixed Risk Simulation
            - Percentage risked per trade kept constant, not adaped / changed with losses
        """
        # Adds starting balance to balance tracking list
        balanceTracking = [accBalance]

        for i in range(self.noTrades):
            """
            Trade outcome randomly chosen / allocated
                - W = Winning trade
                - L = Losing trade
            """
            outcome = (choices(["W","L"], weights=[self.winrate, (1-self.winrate)]))[0]
            PnL = 0

            if outcome == "W":
                # Winning trade
                PnL = (accBalance * (self.riskPercentage/100)) * self.riskReward
                accBalance += PnL # Winning trade, so PnL increases
            else:
                #outcome = "L" -> Losing trade
                PnL = (accBalance * (self.riskPercentage/100))
                accBalance -= PnL # Losing trade so PnL reduces

            # Appends new balance to tracking list  
            balanceTracking.append(accBalance)
        (self.outcomes).append(balanceTracking)


if __name__ == "__main__":
    balance = 100000
    winrate = 0.60
    riskPercentage = 1
    riskReward = 2
    noTrades = 50
    noSimulations = 7
    
    # Runs Simulator class
    sim = RiskSimulation(balance, winrate, riskPercentage, riskReward, noTrades, noSimulations)
    



        