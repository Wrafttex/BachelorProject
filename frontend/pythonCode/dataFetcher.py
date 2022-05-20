import pandas as pd

def dataHandler():
	# LightGBM Tag CSV
	LGBMTagPredictCSV = pd.read_csv(r"LightGBM\AAl_T_Prediction.csv")
	LGBMTagRealCSV    = pd.read_csv(r"LightGBM\AAl_G_Real.csv")

	# LightGBM Gade CSV
	LGBMGadePredictCSV = pd.read_csv(r"LightGBM\AAl_G_Prediction.csv")
	LGBMGadeRealCSV    = pd.read_csv(r"LightGBM\AAl_G_Real.csv")

	# LightGBM Tag CSV
	LSTMTagPredictCSV = pd.read_csv(r"LSTM\AAl_T_Prediction.csv")
	LSTMTTagRealCSV    = pd.read_csv(r"LSTM\AAl_T_Real.csv")

	# LightGBM Gade CSV
	LSTMTGadePredictCSV = pd.read_csv(r"LSTM\AAl_G_Prediction.csv")
	LSTMTGadeRealCSV    = pd.read_csv(r"LSTM\AAl_G_Real.csv")

	# LightGBM Extracting Tag Data
	LGBMTagPredictData = pd.DataFrame(LGBMTagPredictCSV, columns= ["Pred_NO2", "Pred_NOx", "Pred_O3"])
	LGBMTagRealData    = pd.DataFrame(LGBMTagRealCSV, columns= ["Real_NO2", "Real_NOx", "Real_O3"])

	# LightGBM Extracting Gade Data
	LGBMGadePredictData = pd.DataFrame(LGBMGadePredictCSV, columns= ["Pred_NO2", "Pred_NOx"])
	LGBMGadeRealData    = pd.DataFrame(LGBMGadeRealCSV, columns= ["Real_NO2", "Real_NOx"])

	# LightGBM Extracting Tag Data
	LSTMTagPredictData = pd.DataFrame(LSTMTagPredictCSV, columns= ["Pred_NO2", "Pred_NOx", "Pred_O3"])
	LSTMTTagRealData    = pd.DataFrame(LSTMTTagRealCSV, columns= ["Real_NO2", "Real_NOx", "Real_O3"])

	# LightGBM Extracting Gade Data
	LSTMTGadePredictData = pd.DataFrame(LSTMTGadePredictCSV, columns= ["Pred_NO2", "Pred_NOx"])
	LSTMTGadeRealData    = pd.DataFrame(LSTMTGadeRealCSV, columns= ["Real_NO2", "Real_NOx"])

	return LGBMTagPredictData, LGBMTagRealData, LGBMGadePredictData, LGBMGadeRealData, LSTMTagPredictData, LSTMTTagRealData, LSTMTGadePredictData, LSTMTGadeRealData