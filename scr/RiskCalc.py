"""
Author: OsaO
Date Created: 19/05/2024

Last Updated By: OsaO
Last Updated Date: 21/06/2024

Summary:
Risk simulator showing potential equity curve for a trading strategy with defined parameters.
    - Parameters: Starting Balance, Strategy Win Rate, Risk Percentage, Average trade Risk-to-Reward,
                  Number of trades taken, Number of simulations wanted 

TO-DO:
    - Calculations assume balance > 0 (not negative). E,g max drawdown calculation. Something to think about
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

        self.peakValue = 0 # Records peak value used for calculating max drawdown
        self.maxDrawdown = 0 # Max drawdown (2DP)

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
        # Handles a trades outcome regarding to the stats being collected
        # Also checks if it is the last trade in the simulation
            # If last trade, checks if the current ending streak greater than the recorded 
            # This is required for example when the simulation ends on the longest winning / losing streak, so that that streak is recorded

        PnL = 0 # Sets PnL to default value 
        
        if outcome == "W":
            # Winning trade
            PnL = (self.accBalance * (self.riskPercentage/100)) * self.riskReward
            self.accBalance += PnL # Winning trade, so PnL increases

            ### Updates required stats below ###

            # Winning trade
            # Checks to see if it is first winning trade (there has been a run of atleast 1 losing trade)
            if (self.winCounter == 0): # Fist winning trade after loss(es)
                # Calculates the drawdown encountered, and sees if its greater than recorded drawdown
                if (self.peakValue > 0):
                    newdd = round((((self.peakValue - self.equityTracker[-1]) / self.peakValue) * 100), 2)
                    if newdd > self.maxDrawdown: self.maxDrawdown = newdd

                # Checks to see if losing counter is greater than max loss
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

            # Losing trade
            # Checks to see if it is first losing trade (there has been a run of atleast 1 winning trade)
            if (self.lossCounter == 0): # Fist losing trade after win(s)
                self.peakValue = (self.equityTracker)[-1] #Records previous balance as peak for max drawdown calculation
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

    # Returns the outcome of the runs 
    return simulations

def plot(xRange, simOutputs):
    """
    Not used by the app - for testing / debugging within script only
    """
    # Gets list of xValues used to plot graph
    # xValues = number of trades, so generates list starting from 0 to number of trades with a step of 1
    xValues = np.arange(0, xRange+1, 1).tolist()

    # Plots each of the outcomes
    for sim in simOutputs:
        plt.plot(xValues, sim.equityTracker)

    # Sets chart environemnt
    plt.xlabel('Number of Trades')
    plt.ylabel('Account Balance')
    plt.grid('on')
    plt.show()

if __name__ == "__main__":
    import StatsCalc

    # Debugging / Testing
    balance = 1000
    winrate = 0.60
    riskPercentage = 1
    riskReward = 2
    noTrades = 50
    noSimulations = 7
    
    # Runs Simulator class
    simOutputs = runSimulation(balance, winrate, riskPercentage, riskReward, noTrades, noSimulations)
    #print(simOutputs)

    # Gets equity for each run
    #print([output.equityTracker for output in simOutputs])    

    # Plots the data
    #plot(noTrades, simOutputs)

    print(StatsCalc.calculate(simOutputs))
    pass
    # End Of Code



        