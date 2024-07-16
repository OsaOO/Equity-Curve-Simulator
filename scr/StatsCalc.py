"""
Author: OsaO
Last Updated By: OsaO
Last Updated Date: 16/07/2024

Summary:
Calculates stats based off account balace progression

Stats Calculated:
- End Average Balance, Max Equity, Min Equity, Average Max Equity, Average Min Equity
"""

import numpy as np
import timeit

def getOverallStats(simOutputs):
    """
    Generates the stats based on all simulations ran

    simOutputs (arg) - A list containing all the simulation objects
    """

    # Creates a stats dictionary that stores the stats once calculated
    # This dictionary object is then returned at completion
    global stats
    stats = {}

    """
    # Gets the Equity data from the simulations and put into np array
    equityData = np.array([output.equityTracker for output in simOutputs])

    - Above currently not in use.
      Tested speed of required data extraction and was slightly slower than current method
    """

    # Calls required functions to get stats
    
    avgEndBalance(simOutputs)

    maxEquityList = [sim.maxEquity for sim in simOutputs] # Creates list of maxEquity form all sims
    minEquityList = [sim.minEquity for sim in simOutputs] # Creates list of minEquity form all sims
    maxEquity(simOutputs, maxEquityList)
    minEquity(simOutputs, minEquityList)
    avgMaxEquity(simOutputs, maxEquityList)
    avgMinEquity(simOutputs, minEquityList)

    maxConsecWins(simOutputs)
    maxConsecLoss(simOutputs)

    maxDrawdownList = [sim.maxDrawdown for sim in simOutputs] # Creates list of maxDrawdown form all sims
    maxDrawdown(simOutputs, maxDrawdownList)
    avgDrawdown(simOutputs, maxDrawdownList)

    # Returns the stats
    return stats

def getSingleStats(simulation):
    """
    Gets stats based of one individual simulation

    simulation (arg) - Selected simulation object
    """
    # Creates a stats dictionary that stores the stats once calculated
    # This dictionary object is then returned at completion
    global stats
    stats = {}
    
    # Adds Stats
    stats["StartBalance"] = simulation.equityTracker[0]
    stats["EndBalance"] = round(simulation.accBalance, 2)
    stats["MaxEquity"] = round(simulation.maxEquity, 2)
    stats["MinEquity"] = round(simulation.minEquity, 2)
    stats["MaxDrawdown"] = round(simulation.maxDrawdown, 2)
    stats["MaxConsecWins"] = simulation.maxWin
    stats["MaxConsecLoss"] = simulation.maxLoss

    # Returns the stats
    return stats


##### FUNCTIONS FOR GETING REQUIRED STATS #####

def avgEndBalance(simOutputs):
    """
    Average end balance of all simulations run
    """
    endValues = [sim.accBalance for sim in simOutputs]
    avg = round(sum(endValues) / len(endValues), 2)
    stats["AvgEndBalance"] = avg
def maxEquity(simOutputs, maxEquityList):
    """
    Gets the max equity encountered from all simulations
    """
    stats["MaxEquity"] = round(max(maxEquityList), 2)
def minEquity(simOutputs, minEquityList):
    """
    Gets the min equity encountered from all simulations
    """
    stats["MinEquity"] = round(min(minEquityList), 2)
def avgMaxEquity(simOutputs, maxEquityList):
    """
    Gets the avergae max equity encountered from all simulations
    """
    avg = round(sum(maxEquityList) / len(maxEquityList),2)
    stats["AvgMaxEquity"] = avg
def avgMinEquity(simOutputs, minEquityList):
    """
    Gets the avergae min equity encountered from all simulations
    """
    avg = round(sum(minEquityList) / len(minEquityList),2)
    stats["AvgMinEquity"] = avg
def maxConsecWins(simOutputs):
    """
    Gets the maximum consecutive wins encountered from all the simulations
    """
    mWin = max([sim.maxWin for sim in simOutputs])
    stats["MaxConsecWins"] = mWin
def maxConsecLoss(simOutputs):
    """
    Gets the maximum consecutive losses encountered from all the simulations
    """
    mLoss = max([sim.maxLoss for sim in simOutputs])
    stats["MaxConsecLoss"] = mLoss
def maxDrawdown(simOutputs, maxDrawdownList):
    """
    Gets the maximum drawdown encountered from all the simulations
    """
    stats["MaxDrawdown"] = max(maxDrawdownList)
def avgDrawdown(simOutputs, maxDrawdownList):
    """
    Gets the avergae (max) drawdown encountered from all simulations
    """
    avg = round(sum(maxDrawdownList) / len(maxDrawdownList),2)
    stats["AvgDrawdown"] = avg 


if __name__ == "__main__":
    data = [
        [1000, 1200, 1100, 1500, 1800, 1700],
        [1000, 900, 700, 850, 1200, 1100],
        [1000, 1300, 1200, 1400, 1000, 800]
        ]
    
    #a = (getStats(data))
    #print(a.calculate())