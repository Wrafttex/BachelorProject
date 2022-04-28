from dataFetcher import dataHandler
import plotly.graph_objects as go
import json
import plotly
tagPredictData, tagRealData, gadePredictData, gadeRealData = dataHandler()

def plotGraph0():

    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=tagPredictData.index, y=tagPredictData["NO2"],
                    mode='lines',
                    name='NO2 Predicted'))

    graph.add_trace(go.Scatter(x=tagPredictData.index, y=tagPredictData["NOX"],
                    mode='lines',
                    name='NOX Predicted'))

    graph.add_trace(go.Scatter(x=tagPredictData.index, y=tagPredictData["O3"],
                    mode='lines',
                    name='O3 Predicted',))  

    ## Real data
    graph.add_trace(go.Scatter(x=tagRealData.index, y=tagRealData["NO2"],
                    mode='lines',
                    name='NO2 Real'))

    graph.add_trace(go.Scatter(x=tagRealData.index, y=tagRealData["NOX"],
                    mode='lines',
                    name='NOX Real'))

    graph.add_trace(go.Scatter(x=tagRealData.index, y=tagRealData["O3"],
                    mode='lines',
                    name='O3 Real'))  

    return json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)       

def plotGraph1():

    graph = go.Figure()

    ## Predicted data
    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadePredictData["NO2"],
                    mode='lines',
                    name='NO2 Predicted'))

    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadePredictData["NOX"],
                    mode='lines',
                    name='NOX Predicted'))

    ## Real data
    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadePredictData["NO2"],
                    mode='lines',
                    name='NO2 Real'))

    graph.add_trace(go.Scatter(x=gadePredictData.index, y=gadePredictData["NOX"],
                    mode='lines',
                    name='NOX Real'))

    return json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)  