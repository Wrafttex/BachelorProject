from cProfile import label
from turtle import color
from dataFetcher import dataHandler
import numpy as np
import plotly.graph_objects as go
import json
import plotly
LGBMTagPredictData, LGBMTagRealData, LGBMGadePredictData, LGBMGadeRealData, LSTMTagPredictData, LSTMTTagRealData, LSTMTGadePredictData, LSTMTGadeRealData, LGBM24TagPredictData, LGBM24TagRealData, LGBM24GadePredictData, LGBM24GadeRealData = dataHandler()

def remove_odd(l):
    return [x for x in l if x % 2 == 0]

hourIndex = remove_odd(np.arange(48))
hours24 = np.arange(24)

def plotGraph0(test = 0):
    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=LGBMTagPredictData.index, y=LGBMTagPredictData["Pred_NO2"].head(47),
                    mode="lines",
                    name="NO2 Predicted"))

    graph.add_trace(go.Scatter(x=LGBMTagPredictData.index, y=LGBMTagPredictData["Pred_NOx"].head(47),
                    mode="lines",
                    name="NOX Predicted"))

    graph.add_trace(go.Scatter(x=LGBMTagPredictData.index, y=LGBMTagPredictData["Pred_O3"].head(47),
                    mode="lines",
                    name="O3 Predicted",))  

    ## Real data
    graph.add_trace(go.Scatter(x=LGBMTagRealData.index, y=LGBMTagRealData["Real_NO2"].head(47),
                    mode="lines",
                    name="NO2 Real"))

    graph.add_trace(go.Scatter(x=LGBMTagRealData.index, y=LGBMTagRealData["Real_NOx"].head(47),
                    mode="lines",
                    name="NOX Real"))

    graph.add_trace(go.Scatter(x=LGBMTagRealData.index, y=LGBMTagRealData["Real_O3"].head(47),
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
    graph.add_trace(go.Scatter(x=LGBMGadePredictData.index, y=LGBMGadePredictData["Pred_NO2"].head(47),
                    mode="lines",
                    name="NO2 Predicted"))

    graph.add_trace(go.Scatter(x=LGBMGadePredictData.index, y=LGBMGadePredictData["Pred_NOx"].head(47),
                    mode="lines",
                    name="NOX Predicted"))

    ## Real data
    graph.add_trace(go.Scatter(x=LGBMGadeRealData.index, y=LGBMGadeRealData["Real_NO2"].head(47),
                    mode="lines",
                    name="NO2 Real"))

    graph.add_trace(go.Scatter(x=LGBMGadeRealData.index, y=LGBMGadeRealData["Real_NOx"].head(47),
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

def plotGraph2(test = 0):
    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=LSTMTagPredictData.index, y=LSTMTagPredictData["Pred_NO2"].head(47),
                    mode="lines",
                    name="NO2 Predicted"))

    graph.add_trace(go.Scatter(x=LSTMTagPredictData.index, y=LSTMTagPredictData["Pred_NOx"].head(47),
                    mode="lines",
                    name="NOX Predicted"))

    graph.add_trace(go.Scatter(x=LSTMTagPredictData.index, y=LSTMTagPredictData["Pred_O3"].head(47),
                    mode="lines",
                    name="O3 Predicted",))  

    ## Real data
    graph.add_trace(go.Scatter(x=LSTMTTagRealData.index, y=LSTMTTagRealData["Real_NO2"].head(47),
                    mode="lines",
                    name="NO2 Real"))

    graph.add_trace(go.Scatter(x=LSTMTTagRealData.index, y=LSTMTTagRealData["Real_NOx"].head(47),
                    mode="lines",
                    name="NOX Real"))

    graph.add_trace(go.Scatter(x=LSTMTTagRealData.index, y=LSTMTTagRealData["Real_O3"].head(47),
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

def plotGraph3(test = 0):
    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=LSTMTGadePredictData.index, y=LSTMTGadePredictData["Pred_NO2"].head(47),
                    mode="lines",
                    name="NO2 Predicted"))

    graph.add_trace(go.Scatter(x=LSTMTGadePredictData.index, y=LSTMTGadePredictData["Pred_NOx"].head(47),
                    mode="lines",
                    name="NOX Predicted"))

    ## Real data
    graph.add_trace(go.Scatter(x=LSTMTGadeRealData.index, y=LSTMTGadeRealData["Real_NO2"].head(47),
                    mode="lines",
                    name="NO2 Real"))

    graph.add_trace(go.Scatter(x=LSTMTGadeRealData.index, y=LSTMTGadeRealData["Real_NOx"].head(47),
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