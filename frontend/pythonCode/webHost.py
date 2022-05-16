import plotly.express as px
from flask import Flask, render_template
from graphPlotter import plotGraph0, plotGraph1


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	graphJSON0 = plotGraph0() 
	graphJSON1 = plotGraph1()
	return render_template("home.html", graphJSON0=graphJSON0, graphJSON1=graphJSON1)

if __name__ == "__main__":
	app.run(debug=True)