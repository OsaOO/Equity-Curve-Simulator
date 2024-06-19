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
    def __init__(self, startBalance, winrate, riskPercentage, riskReward, noTrades, simType):
        ## Defines required stats variables ##
        self.simType = simType
        self.equityTracker = []
        self.accBalance = startBalance
        self.maxEquity = startBalance
        self.minEquity = startBalance
        self.winrate = winrate
        self.riskPercentage = riskPercentage
        self.riskReward = riskReward
        self.noTrades = noTrades

        self.maxWin = 0 # Maximum Consecutive wins
        self.winCounter = 0 # Consecutive wins counter
        self.maxLoss = 0 # Max Consecutive losses
        self.lossCounter = 0 # Maximum consecutive loss counter
    def run(self):
        if self.simType == "FixedRisk":
            # Runs Fixed Risk Simulation
            self.FixedRiskSim()

            # Once has wrapped up, needs another check for counters to check last run (should maybe be entered below here)
        elif self.simType == "0.5%":
            # TO BE ADDED
            pass
        else:
            # Invalid Simulation type provided
            return False
    def outcomeHandling(self, outcome, tradeNo):
        PnL = 0 # Sets PnL to default value 
        print(tradeNo)
        # Handles a trades outcome regarding to the stats being collected
        # Also checks if it is the last trade in the simulation
            # If last trade, checks if the current ending streak greater than the recorded 
            # This is required for example when the simulation ends on the longest winning / losing streak, so that that streak is recorded

        if outcome == "W":
            # Winning trade
            PnL = (self.accBalance * (self.riskPercentage/100)) * self.riskReward
            self.accBalance += PnL # Winning trade, so PnL increases

            ### Updates required stats below ###

            

            # Winning trade, so losing streak has ended
            # Checks to see if losing counter is greater than max loss
            if (self.winCounter == 0): # Fist winning trade after loss(es)
                if self.lossCounter > self.maxLoss:
                    self.maxLoss = self.lossCounter
                self.lossCounter = 0 # Resets loss counter back to zero
            self.winCounter += 1 # Increments win counter

            # Checks if it is last trade of simulation
            if (tradeNo == self.noTrades - 1):
                if self.winCounter > self.maxWin:
                    self.maxWin = self.winCounter
        else: #outcome = "L"
            # Losing trade
            PnL = (self.accBalance * (self.riskPercentage/100))
            self.accBalance -= PnL # Losing trade so PnL reduces

            ### Updates required stats below ###

            # Losing trade, so winning streak has ended
            # Checks to see if winning counter is greater than max loss
            if (self.lossCounter == 0): # Fist losing trade after win(s)
                if self.winCounter > self.maxWin:
                    self.maxWin = self.winCounter
                self.winCounter = 0
            self.lossCounter += 1 # Increments Loss Counter

            # Checks if it is last trade of simulation
            if (tradeNo == self.noTrades - 1):
                if self.lossCounter > self.maxLoss:
                    self.maxLoss = self.lossCounter            
        
        # Checks if a new maximum / minimum balance reached
        if self.accBalance > self.maxEquity:
            self.maxEquity = self.accBalance
        elif self.accBalance < self.minEquity:
            self.minEquity = self.accBalance

        # Appends new balance to tracking list
        self.equityTracker.append(self.accBalance)

    def FixedRiskSim(self):
        """
        Fixed Risk Simulation
            - Percentage risked per trade kept constant, not adaped / changed with losses
        """
        # Adds starting balance to balance tracking list
        self.equityTracker.append(self.accBalance)

        for tradeNo in range(self.noTrades):
            """
            Trade outcome randomly chosen / allocated
                - W = Winning trade
                - L = Losing trade
            """
            outcome = (choices(["W","L"], weights=[self.winrate, (1-self.winrate)]))[0]
            # Handles outcome
            self.outcomeHandling(outcome, tradeNo)

def runSimulation(balance, winrate, riskPercentage, riskReward, noTrades, noSimulations, simType="FixedRisk"):
    # Runs the Risk Simulation

    # A list stores all the class objects for each simuation
    # List is returned, so data for each simulation can then be individually be retrived
    simulations = []

    # Threading used to run simulations simultaneously
    threads = []

    for i in range(noSimulations):
        sim = SimulationItem(balance, winrate, riskPercentage, riskReward, noTrades, simType)
        t = threading.Thread(target=sim.run())
        threads.append(t)
        simulations. append(sim) # Appends the simulation class to the list of simulations

    # Starts all threads
    for x in threads:
        x.start()
    # Waits for all threads to finish
    for x in threads:
        x.join()
    
    ### All threads should be completed by this point ###

    # Returns the outcome of the runs generated
    return simulations

 
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
    balance = 1000
    winrate = 0.60
    riskPercentage = 1
    riskReward = 2
    noTrades = 5
    noSimulations = 7
    
    # Runs Simulator class
    sim = runSimulation(balance, winrate, riskPercentage, riskReward, noTrades, noSimulations)
    print("here")



        