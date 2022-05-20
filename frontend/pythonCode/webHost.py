import plotly.express as px
from flask import Flask, render_template
from graphPlotter import plotGraph0, plotGraph1, plotGraph2, plotGraph3


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
	graphJSON0 = plotGraph0() 
	graphJSON1 = plotGraph1()
	graphJSON2 = plotGraph2()
	graphJSON3 = plotGraph3()
	return render_template("home.html", graphJSON0=graphJSON0, graphJSON1=graphJSON1, graphJSON2=graphJSON2, graphJSON3=graphJSON3)

if __name__ == "__main__":
	app.run(debug=True)