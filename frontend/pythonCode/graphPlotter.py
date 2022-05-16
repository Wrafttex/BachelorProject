from cProfile import label
from turtle import color
from dataFetcher import dataHandler
import numpy as np
import plotly.graph_objects as go
import json
import plotly
tagPredictData, tagRealData, gadePredictData, gadeRealData = dataHandler()

def remove_odd(l):
    return [x for x in l if x % 2 == 0]

hourIndex = remove_odd(np.arange(48))
hours24 = np.arange(24)

def plotGraph0(test = 0):
    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=tagPredictData.index, y=tagPredictData["NO2"].head(47),
                    mode="lines",
                    name="NO2 Predicted"))

    graph.add_trace(go.Scatter(x=tagPredictData.index, y=tagPredictData["NOX"].head(47),
                    mode="lines",
                    name="NOX Predicted"))

    graph.add_trace(go.Scatter(x=tagPredictData.index, y=tagPredictData["O3"].head(47),
                    mode="lines",
                    name="O3 Predicted",))  

    ## Real data
    graph.add_trace(go.Scatter(x=tagRealData.index, y=tagRealData["NO2"].head(47),
                    mode="lines",
                    name="NO2 Real"))

    graph.add_trace(go.Scatter(x=tagRealData.index, y=tagRealData["NOX"].head(47),
                    mode="lines",
                    name="NOX Real"))

    graph.add_trace(go.Scatter(x=tagRealData.index, y=tagRealData["O3"].head(47),
                    mode="lines",
                    name="O3 Real"))  

    if (test == False):
        graph.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgb(60,60,60)",
            font_color="rgba(0,0,0,100)",
            xaxis = dict(
                tickmode = 'array',
                tickvals  = hourIndex,
                ticktext = hours24
            )
            )
        graph.update_xaxes(fixedrange=False) 
        outputJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
        return outputJSON  
    else:
        return graph.show()     

def plotGraph1(test = 0):
    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadePredictData["NO2"].head(47),
                    mode="lines",
                    name="NO2 Predicted"))

    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadePredictData["NOX"].head(47),
                    mode="lines",
                    name="NOX Predicted"))

    ## Real data
    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadeRealData["NO2"].head(47),
                    mode="lines",
                    name="NO2 Real"))

    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadeRealData["NOX"].head(47),
                    mode="lines",
                    name="NOX Real"))

    if (test == False):
        graph.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgb(60,60,60)",
            font_color="rgba(0,0,0,100)",
            xaxis = dict(
                tickmode = 'array',
                tickvals  = hourIndex,
                ticktext = hours24
            )
            )
        outputJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
        return outputJSON 
    else:
        return graph.show()     