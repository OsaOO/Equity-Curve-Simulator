"""
Author: OsaO
Date Created: 20/05/2024

Last Updated By: OsaO
Last Updated Date: 20/05/2024

Summary: 
"""

from flask import Flask, render_template, request
import random
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)