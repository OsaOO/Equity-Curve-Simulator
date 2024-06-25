"""
Author: OsaO
Date Created: 10/06/2024

Last Updated By: OsaO
Last Updated Date: 10/06/2024

Summary:
Calculates stats based off account balace progression

Stats Calculated:
- End Average Balance, Max Equity, Min Equity

Stats to add:
- Average Max Equity, Average Min Equity
"""

import numpy as np
import timeit

#def __init__(self, data):
#    # Creates Numpy Array to perform calculations on
#    self.arr = np.array(data)


def calculate(simOutputs):
    # Begins required calculations

    # Creates a dictionary that stores the stats once calculated
    # This dictionary object is then returned at completion

    global stats
    stats = {}

    # Gets the Equity data from the simulations and put into np array
    equityData = np.array([output.equityTracker for output in simOutputs])

    # Stats that relate to the simulation run as a whole
    
    endBalanceAvg(simOutputs)
    maxEquity(simOutputs)
    minEquity(simOutputs)
    avgMaxEquity(simOutputs)
    avgMinEquity(simOutputs)
    
    # Stats that relate to an individual simulation from total simulations run
    # RUN FUNCTIONS HERE!
    # - Create seperte function for individual stats run

    # Returns the stats
    return stats

def endBalanceAvg(simOutputs):
    """
    Average end balance of all simulations run
    """
    endValues = [sim.accBalance for sim in simOutputs]
    avg = round(sum(endValues) / len(endValues), 2)
    stats["EndBalanceAvg"] = avg
def maxEquity(simOutputs):
    """
    Gets the max equity encountered from all simulations
    """
    stats["MaxEquity"] = round(max([sim.maxEquity for sim in simOutputs]), 2)
def minEquity(simOutputs):
    """
    Gets the min equity encountered from all simulations
    """
    stats["MinEquity"] = round(min([sim.minEquity for sim in simOutputs]), 2)
def avgMaxEquity(simOutputs):
    """
    Gets the avergae max equity encountered from all simulations
    """
    maxVals = [sim.maxEquity for sim in simOutputs]
    avg = round(sum(maxVals) / len(maxVals),2)
    stats["AvgMaxEquity"] = avg
def avgMinEquity(simOutputs):
    """
    Gets the avergae min equity encountered from all simulations
    """
    minVals = [sim.minEquity for sim in simOutputs]
    avg = round(sum(minVals) / len(minVals),2)
    stats["AvgMinEquity"] = avg
def maxConsecWins(simOutputs):
    """
    Gets the maximum consecutive wins encountered from all the simulations
    """
    mWin = max([sim.MaxLoss for sim in simOutputs])
    stats["MaxConsecWins"] = mWin
def maxConsecLoss(simOutputs):
    """
    Gets the maximum consecutive losses encountered from all the simulations
    """
    mLoss = max([sim.MaxLoss for sim in simOutputs])
    stats["MaxConsecLoss"] = mLoss
def maxDrawdown(simOutputs):
    """
    Gets the maximum drawdown encountered from all the simulations
    """
    mDD = max([sim.maxDrawdown for sim in simOutputs])
    stats["MaxDrawdown"] = mDD
def avgDrawdown(simOutputs):
    """
    Gets the avergae (max) drawdown encountered from all simulations
    """
    vals = [sim.maxDrawdown for sim in simOutputs]
    avg = round(sum(vals) / len(vals),2)
    stats["AvgDrawdown"] = avg 


if __name__ == "__main__":
    data = [
        [1000, 1200, 1100, 1500, 1800, 1700],
        [1000, 900, 700, 850, 1200, 1100],
        [1000, 1300, 1200, 1400, 1000, 800]
        ]
    
    a = (getStats(data))
    print(a.calculate())



"""
Code used for comparing time of functions


    c1 = '''stats["MaxEquity"] = round((equityData).max(), 2)'''
    c2 = '''stats["MaxEquity"] = round(max([sim.maxEquity for sim in simOutputs]), 2)'''

    #t = timeit.Timer(lambda: maxEquity(equityData))
    print(timeit.repeat(lambda: c1, repeat=5))
    #t2 = timeit.Timer(lambda: maxEquity2(simOutputs))
    print(timeit.repeat(lambda: c2, repeat=5))
"""