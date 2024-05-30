function updateLabel(labelId, value) {
    document.getElementById(labelId).textContent = value;
}

function runSimulation() {
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
            template: 'plotly_dark'
        };

        Plotly.newPlot('graph', traces, layout);
    });
}
