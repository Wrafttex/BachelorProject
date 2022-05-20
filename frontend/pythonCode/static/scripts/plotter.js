var Plotly = require("plotly-latest");

var graph0 = {{ graphJSON1|tojson }};
var graph1 = {{ graphJSON1|tojson }};

Plotly.newPlot("graph0", graph0, {}, {"displayModeBar": True});
Plotly.newPlot("graph1", graph1, {}, {"displayModeBar": True});