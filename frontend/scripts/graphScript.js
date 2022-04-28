function dataFetcher() {
	var testData = [new Array(10),new Array(10),new Array(10)];

	testData[0] = testData[0].fill(10).map(() => Math.random());
	testData[1] = testData[1].fill(10).map(() => Math.random());
	testData[2] = testData[2].fill(10).map(() => Math.random());

	return testData;
}

async function readCSV() {
	var reader = new FileReader();
	var data;
	var processedData;
	let result = await fetch("data\\Aalborg_Gade_Predicted_output.csv").then(r => r.blob());
	
	data = result.text();
	processedData = (await data).replace( /\n/g, " " ).split(" ");
	console.log(processedData);

	


	return result.toString();
};

readCSV();

function plotChart(){
	const indexLables = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

	var data = dataFetcher();

	var chart0 = new Chart("chart0", {
		type: "line",
		data: {
			lables: indexLables,
			datasets: [
				{
					data: data[0],
					borderColor: "red",
					fill: false
				},
				{
					data: data[1],
					borderColor: "blue",
					fill: false
				},
				{
					data: data[2],
					borderColor: "green",
					fill: false
				},
			]
		},
		options: {}
	});

	data = dataFetcher();

	var chart1 = new Chart("chart1", {
		type: "line",
		data: {
			lables: indexLables,
			datasets: [
				{
					data: data[0],
					borderColor: "red",
					fill: false
				},
				{
					data: data[1],
					borderColor: "blue",
					fill: false
				},
				{
					data: data[2],
					borderColor: "green",
					fill: false
				},
			]
		},
		options: {}
	});
}

plotChart();