import imp
import plotly.express as px
from flask import Flask, render_template
from graphPlotter import plotGraph0, plotGraph1


app = Flask(__name__)

@app.route("/")
def home():
        graph0=0
        return render_template("home.html", graph0=plotGraph0(), graph1=plotGraph1())

if __name__ == "__main__":
        app.run(debug=True)