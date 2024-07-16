"""
Author: OsaO
Date Created: 20/05/2024

Last Updated By: OsaO
Last Updated Date: 20/05/2024

Summary: 

ToDo:
- Update and Improve UI (make look nicer / more modern)
- Add Different risk strategies (i.e not only fixed risk)
"""

from flask import Flask, render_template, request, jsonify
import random
import plotly.graph_objects as go
import plotly.io as pio

import numpy as np
import os.path

from scr import RiskCalc
from scr.StatsCalc import getOverallStats

app = Flask(__name__)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json

    # Runs the simulations and records the outcome 
    simulations = RiskCalc.runSimulation(
        balance = data['balance'],
        winrate=data['win_rate'] / 100,
        riskPercentage=2,
        riskReward=data['risk_reward_ratio'],
        noTrades=data['number_of_trades'],
        noSimulations=data['number_of_simulations'],
    )

    # Gets a list of all simulation outcomes
    outcomes = [sim.equityTracker for sim in simulations]

    # Gets the stats based on the simulations outcome
    statsOutcome = getOverallStats(simulations)
    print(statsOutcome)
    
    # Returns data back to json function
    # Json function then plots the outcome equity graph and displays stats data
    x_values = np.arange(0, data['number_of_trades'] + 1, 1).tolist()
    return jsonify({'outcomes': outcomes, 'x_values': x_values, 'stats':statsOutcome})

if __name__ == '__main__':
    app.run(debug=True)