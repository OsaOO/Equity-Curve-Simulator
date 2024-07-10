"""
Author: OsaO
Date Created: 19/05/2024

Last Updated By: OsaO
Last Updated Date: 30/05/2024

Summary:
Risk simulator showing potential equity curve for a trading strategy with defined parameters.
    - Parameters: Starting Balance, Strategy Win Rate, Risk Percentage, Average trade Risk-to-Reward,
                  Number of trades taken, Number of simulations wanted 
"""
from random import choices
import matplotlib.pyplot as plt
import numpy as np
import threading

class SimulationItem:
    """
    For each individual simulation performed, a class is created storing data relating to the simulation run 
    """
    def __init__(self, startBalance, winrate, riskPercentage, riskReward, noTrades):
        ## Defines required stats variables ##
        self.equityTracker = []
        self.accBalance, self.maxEquity, self.minEquity = startBalance
        self.winrate = winrate
        self.riskPercentage = riskPercentage
        self.riskReward = riskReward
        self.noTrades = noTrades

        self.maxWin = 0 # Maximum Consecutive wins
        self.winCounter = 0 # Consecutive wins counter
        self.maxLoss = 0 # Max Consecutive losses
        self.lossCounter = 0 # Maximum consecutive loss counter
    def run(self):
        pass
    def outcomeHandling(self, outcome):
        PnL = 0 # Sets PnL to default value 
        # Handles a trades outcome regarding to the stats being collected
        if outcome == "W":
            # Winning trade
            PnL = (self.accBalance * (self.riskPercentage/100)) * self.riskReward
            self.accBalance += PnL # Winning trade, so PnL increases

            ### Updates required stats below ###

            # Winning trade, so losing streak has ended
            # Checks to see if losing counter is greater than max loss
            if self.winCounter == 0: # Fist winning trade after loss(es)
                if self.lossCounter > self.maxLoss:
                    self.maxLoss = self.lossCounter
                self.lossCounter = 0 # Resets loss counter back to zero
            # Increments win counter
            self.winCounter += 1 # Increments win counter
        else: #outcome = "L"
            # Losing trade
            PnL = (self.accBalance * (self.riskPercentage/100))
            self.accBalance -= PnL # Losing trade so PnL reduces

            ### Updates required stats below ###

            # Losing trade, so winning streak has ended
            # Checks to see if winning counter is greater than max loss
            if self.lossCounter == 0: # Fist losing trade after win(s)
                if self.winCounter > self.maxWin:
                    self.maxWin = self.winCounter
                self.winCounter = 0
            # Increments Loss Counter
            self.lossCounter += 1

        # Checks if a new maximum / minimum balance reached
        if self.accBalance > self.maxEquity:
            self.maxEquity = self.accBalance
        elif self.accBalance < self.minEquity:
            self.minEquity = self.accBalance

    def FixedRiskSim(self):
        """
        Fixed Risk Simulation
            - Percentage risked per trade kept constant, not adaped / changed with losses
        """
        # Adds starting balance to balance tracking list
        self.equityTracker.append(self.accBalance)


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

    def runSimulation(self):
        # Runs the Risk Simulation
        # All the required inputs should have already been provided when class decleared
        
        # Threading used to run number of simulations simultaneously
        threads = []

        for i in range(self.noSimulations):
            t = threading.Thread(target=self.FixedRiskSim(self.startBalance))
            threads.append(t)

        # Starts all threads
        for x in threads:
            x.start()
        # Waits for all threads to finish
        for x in threads:
            x.join()
        
        ### All threads should be completed by this point ###

        # Returns the outcome of the runs generated
        return self.outcomes
        
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
    
    def plot(self):
        """
        Not used by the app - for testing / debugging within script only
        """
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

if __name__ == "__main__":
    # Debugging / Testing
    balance = 100000
    winrate = 0.60
    riskPercentage = 1
    riskReward = 2
    noTrades = 50
    noSimulations = 7
    
    # Runs Simulator class
    #sim = RiskSimulation(balance, winrate, riskPercentage, riskReward, noTrades, noSimulations)
    print("here")



        