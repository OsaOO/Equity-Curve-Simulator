function updateLabel(labelId, value) {
    // Updates a label with a specific ID to specified value
    document.getElementById(labelId).textContent = value;
}

function firstLoad(){
    // Attemping to load an empty grpah (on page load up)
    // NOTE: Currently not working as intended!
    const layout = {
        title: 'Equity Curves',
        xaxis: { title: 'Number of Trades' },
        yaxis: { title: 'Account Balance' },
        template: 'plotly_dark',
        legend: {"orientation": "h",
            x: 0,
            y: -0.35
        },
        hovermode: 'closest',
    };

    Plotly.newPlot('graph', {}, layout, {displayModeBar: false});

}

function runSimulation() {
    // Gets the data from the input elemensts
    const balance = parseFloat(document.getElementById('balance').value);
    const winRate = parseFloat(document.getElementById('win-rate').value);
    const riskPercentage = parseFloat(document.getElementById('risk-percentage').value);
    const riskRewardRatio = parseFloat(document.getElementById('risk-reward-ratio').value);
    const numberOfTrades = parseInt(document.getElementById('number-of-trades').value);
    const numberOfSimulations = parseInt(document.getElementById('number-of-simulations').value);

    const data = {
        balance: balance,
        win_rate: winRate,
        riskPercentage: riskPercentage,
        risk_reward_ratio: riskRewardRatio,
        number_of_trades: numberOfTrades,
        number_of_simulations: numberOfSimulations
    };

    fetch('/simulate', {
        // Sends post request with the data from the input elements
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const outcomes = data.outcomes;
        const xValues = data.x_values;
        const stats = data.stats;

        // Creates variables required by plotly to plot graph
        const traces = outcomes.map((outcome, index) => {
            return {
                x: xValues,
                y: outcome,
                mode: 'lines',
                name: `Simulation ${index + 1}`
            };
        });
        const layout = {
            title: 'Equity Curves',
            xaxis: { title: 'Number of Trades' },
            yaxis: { title: 'Account Balance' },
            template: 'plotly_dark',
            legend: {"orientation": "h",
                x: 0,
                y: -0.35
            },
            hovermode: 'closest',
        };

        // Plots Graph to element with id "graph"
        Plotly.newPlot('graph', traces, layout, {displayModeBar: false});

        // Updates Label to display the Calculated Stats
        // Maybe create mapping table to only perform one if statement
        // ENTER CODE BELOW HERE
        if ("AvgEndBalance" in stats) {
            document.getElementById("avgBalance").textContent = stats["AvgEndBalance"];    
        }
        if ("MaxEquity" in stats) {
            document.getElementById("maxSim").textContent = stats["MaxEquity"];    
        }
        if ("AvgMaxEquity" in stats) {
            document.getElementById("avgMaxSim").textContent = stats["AvgMaxEquity"];    
        }
        if ("MinEquity" in stats) {
            document.getElementById("minSim").textContent = stats["MinEquity"];    
        }
        if ("AvgMinEquity" in stats) {
            document.getElementById("avgMinSim").textContent = stats["AvgMinEquity"];    
        }
        if ("MaxConsecWins" in stats) {
            document.getElementById("maxConsecWins").textContent = stats["MaxConsecWins"];    
        }
        if ("MaxConsecLoss" in stats) {
            document.getElementById("maxConsecLoss").textContent = stats["MaxConsecLoss"];    
        }
        if ("MaxDrawdown" in stats) {
            document.getElementById("maxDD").textContent = stats["MaxDrawdown"];    
        }
        if ("AvgDrawdown" in stats) {
            document.getElementById("avgDD").textContent = stats["AvgDrawdown"];    
        }
        
    });
}
