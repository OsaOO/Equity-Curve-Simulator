"""
Author: OsaO
Date Created: 10/06/2024

Last Updated By: OsaO
Last Updated Date: 10/06/2024

Summary:
Calculates stats based off account balace progression
"""

import pandas as pd
import numpy as np

data = [[1000, 1200, 1100, 1500, 1800, 1700],
        [1000, 900, 700, 850, 1200, 1100],
        [1000, 1300, 1200, 1400, 1000, 800]
        ]

class StatCal ():
    def __init__(self, data):
        # Creates Numpy Array to perform calculations on
        self.arr = np.array(data)

        # Creates a dictionary that stores the stats once calculated
        # This dictionary object is then returned at completion
        self.stats = {}

        self.calculate()
    
    def calculate(self):
        # Begins required calculations

        self.EndBalanceAvg()
        self.MaxEquity()
        self.MinEquity()

        print(self.stats)

    def EndBalanceAvg(self):
        """
        Average end balance of all simulations run
        """
        endValues = [item[-1] for item in self.arr]
        avg = round(sum(endValues) / len(endValues), 2)
        self.stats["EndBalanceAvg"] = avg
    def MaxEquity(self):
        """
        Gets the max equity encountered from all simulations
        """
        self.stats["MaxEquity"] = (self.arr).max()
    def MinEquity(self):
        """
        Gets the min equity encountered from all simulations
        """
        self.stats["MinEquity"] = self.arr.min()


if __name__ == "__main__":
    StatCal(data)
