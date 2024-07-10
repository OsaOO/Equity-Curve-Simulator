"""
Author: OsaO
Date Created: 20/05/2024

Last Updated By: OsaO
Last Updated Date: 10/07/2024

Summary:
App 2.0 which uses StreamLit to create the UI (no need for html / css)

TO-DO:
- Write code to get individual stats
- Make stats section look nicer
- Add discription about the project
- Add links to Github in required places
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from scr import RiskCalc
from scr.StatsCalc import getOverallStats

def simulate():
    # Runs Simulation
    simulations = RiskCalc.runSimulation(
        balance = st.session_state.balance,
        winrate = st.session_state.winrate / 100,
        riskPercentage = st.session_state.riskPercentage,
        riskReward = st.session_state.riskReward,
        noTrades = st.session_state.noTrades,
        noSimulations = st.session_state.noSimulations,
    )

    # Add spinner while simulation is running - ???

    # Gets a list of all simulation outcomes
    outcomes = [sim.equityTracker for sim in simulations]
    # Creates var holding x values (x value = Trade number)
    x_values = np.arange(0, st.session_state.noTrades + 1, 1).tolist()

    # Creates a plotly go figure
    fig = go.Figure()

    # Adds traces for each simulation
    for i, y_values in enumerate(outcomes, start=1):
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', 
                                 name=f'Simulation {i}'))
    
    # Configures figure
    fig.update_layout(
        title = {'text': 'Equity Curves',
                 'x':0.5,
                 'xanchor': 'center',
                 'yanchor': 'top',
                 'font': {'size':32}},
        xaxis_title = "Number of Trades",
        yaxis_title = "Account Balance",
    )
   
    # Gets the stats based on the simulations outcome
    statsOutcome = getOverallStats(simulations)
    print(statsOutcome)

    # Adds fiigure object to seesion to then be plotted
    st.session_state.fig = fig
    # Adds the stats to the session state
    st.session_state.stats = statsOutcome

def main_page():
    """
    Creates main lage layout 
    """

    # Streamlit UI
    st.title('Equity Curve Simulator')
    st.subheader('By Osa.OO')

    # Adds Markdown of h to use input options
    with st.expander("**📖 About this Simulation Project**"):
            st.markdown("ENTER Project information here")

    # Adds divider to seperate header(s)
    st.divider()

    # If there is a figure present, it displays the graph and stats containers
    # Only wont show on application load before the "Run Simulation" button has been pressed
    
    if "fig" in st.session_state:
        # Container where simulation graph is plotted
        with st.container(border=True):
            config = {'displayModeBar': False}
            st.plotly_chart(st.session_state.fig, theme="streamlit", use_container_width=True, config=config) 

        # Container where simulation stats is plotted
        with st.container():
            # Creates 2 columns in this container
            # Col 1 = Overall Stats
            # Col 2 = Vertical divider line
            # Col 3 = Individual Stats
            col1, col2, col3 = st.columns([10.9, 0.2, 10.9], vertical_alignment="top")

            with col1:
                st.subheader("Overall Simulation Stats")
                st.write(
                    f'''
                        - Average End Balance = {st.session_state.stats["AvgEndBalance"]}
                        - Max Equity = {st.session_state.stats["MaxEquity"]}
                        - Average Max Equity = {st.session_state.stats["AvgMaxEquity"]}
                        - Min Equity = {st.session_state.stats["MinEquity"]}
                        - Average Min Equity = {st.session_state.stats["AvgMinEquity"]}
                        - Max Consecutive Wins = {st.session_state.stats["MaxConsecWins"]}
                        - Max Consecutive Losses = {st.session_state.stats["MaxConsecLoss"]}
                        - Max Drawdown = {st.session_state.stats["MaxDrawdown"]}
                        - Average Drawdown = {st.session_state.stats["AvgDrawdown"]}
                    '''
                        )
            with col2:
                st.html(
                        '''
                            <div class="divider-vertical-line"></div>
                            <style>
                                .divider-vertical-line {
                                    border-left: 2px solid rgba(49, 51, 63, 0.2);
                                    height: 320px;
                                    margin: auto;
                                }
                            </style>
                        '''
                        )
            with col3:
                st.subheader("Individual SImulation Stats")  

    
def config_sidebar():
    """
    Setup and display the sidebar elements.
        - This function configures the sidebar of the Streamlit application,
    Sidebar includes form which user has ability to change input values for the simulation
    """

    # Creates a sidebar where the input controls are stored
    with st.sidebar:
        st.title("Simulation Inputs :chart_with_upwards_trend:")
        st.caption("*Made by Osa.OO*")
        
        # Adds divider
        st.write("---")

        # Adds note on how to use
        st.info("Note: Use the sliders to change the inputs for the simulation!")

        # Creates a form inside the sidebar with the inputs (sliders) for the simulation
        with st.form("input_form"):
            # Creates (centered) run simulation button
            col1, col2 = st.columns([1,3])

            # Form Submit button
            # onclick runs runction which runs the simulation using the input values from the form
            run_sim = col2.form_submit_button("Run Simulation", on_click=simulate, type="primary") # Button to Run simulation
            
            # Input sliders
            # Sliders values stored into streamlit session by key value
            #Inputs (sliders) - Slider inputs: min val, max max, value, step
            st.slider('Starting Balance', 1000, 100000, 10000, 1000, key="balance")
            st.slider('Win Rate (%)', 0, 100, 35, 1, key="winrate")
            st.slider('Risk Percentage (%)', 1, 10, 1, 1, key="riskPercentage")
            st.slider('Risk-to-Reward Ratio', 0.5, 10.0, 2.5, 0.25, key="riskReward")
            st.slider('Number of Trades', 50, 500, 300, step=50, key="noTrades")
            st.slider('Number of Simulations', 1, 100, 10, step=1, key="noSimulations")    

def main():
    """
    Main function to run the Streamlit application.
        - initializes the sidebar configuration and the main page layout.
     """
    
    # Sets Page config of the Streamlit Application
    st.set_page_config(page_title='Equity Curve Simulator', layout='wide',
                       initial_sidebar_state=st.session_state.get('sidebar_state', 'expanded'),
    )
    
    # Runs functions to display required UI elements
    config_sidebar()
    main_page()

if __name__ == "__main__":
    
    main()


