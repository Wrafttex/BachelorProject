import pandas as pd

def dataHandler():
	# LightGBM Tag CSV
	LGBMTagPredictCSV = pd.read_csv(r"LightGBM\AAl_T_Prediction.csv")
	LGBMTagRealCSV    = pd.read_csv(r"LightGBM\AAl_T_Real.csv")

	# LightGBM Gade CSV
	LGBMGadePredictCSV = pd.read_csv(r"LightGBM\AAl_G_Prediction.csv")
	LGBMGadeRealCSV    = pd.read_csv(r"LightGBM\AAl_G_Real.csv")

	# LightGBM 24Gade CSV
	LGBM24GadePredictCSV = pd.read_csv(r"LightGBM\AAl_G_24h_Prediction.csv")
	LGBM24GadeRealCSV    = pd.read_csv(r"LightGBM\AAl_G_24h_Real.csv")

	# LightGBM 24Tag CSV
	LGBM24TagPredictCSV = pd.read_csv(r"LightGBM\AAl_T_24h_Prediction.csv")
	LGBM24TagRealCSV    = pd.read_csv(r"LightGBM\AAl_T_24h_Real.csv")

	# LSTM Tag CSV
	LSTMTagPredictCSV = pd.read_csv(r"LSTM\AAl_T_Weather_Prediction.csv")
	LSTMTTagRealCSV    = pd.read_csv(r"LSTM\AAl_T_Real.csv")

	# LSTM Gade CSV
	LSTMTGadePredictCSV = pd.read_csv(r"LSTM\AAl_G_Weather_Prediction.csv")
	LSTMTGadeRealCSV    = pd.read_csv(r"LSTM\AAl_G_Real.csv")

	# LightGBM Extracting Tag Data
	LGBMTagPredictData = pd.DataFrame(LGBMTagPredictCSV, columns= ["Pred_NO2", "Pred_NOx", "Pred_O3"])
	LGBMTagRealData    = pd.DataFrame(LGBMTagRealCSV, columns= ["Real_NO2", "Real_NOx", "Real_O3"])

	# LightGBM Extracting Gade Data
	LGBMGadePredictData = pd.DataFrame(LGBMGadePredictCSV, columns= ["Pred_NO2", "Pred_NOx"])
	LGBMGadeRealData    = pd.DataFrame(LGBMGadeRealCSV, columns= ["Real_NO2", "Real_NOx"])

	# LightGBM 24h Extracting Tag Data
	LGBM24TagPredictData = pd.DataFrame(LGBM24TagPredictCSV, columns= ["Pred_NO2", "Pred_NOx", "Pred_O3"])
	LGBM24TagRealData    = pd.DataFrame(LGBM24TagRealCSV, columns= ["Real_NO2", "Real_NOx", "Real_O3"])

	# LightGBM 24h Extracting Gade Data
	LGBM24GadePredictData = pd.DataFrame(LGBM24GadePredictCSV, columns= ["Pred_NO2", "Pred_NOx"])
	LGBM24GadeRealData    = pd.DataFrame(LGBM24GadeRealCSV, columns= ["Real_NO2", "Real_NOx"])

	# LSTM Extracting Tag Data
	LSTMTagPredictData = pd.DataFrame(LSTMTagPredictCSV, columns= ["Pred_NO2", "Pred_NOx", "Pred_O3"])
	LSTMTTagRealData    = pd.DataFrame(LSTMTTagRealCSV, columns= ["Real_NO2", "Real_NOx", "Real_O3"])

	# LSTM Extracting Gade Data
	LSTMTGadePredictData = pd.DataFrame(LSTMTGadePredictCSV, columns= ["Pred_NO2", "Pred_NOx"])
	LSTMTGadeRealData    = pd.DataFrame(LSTMTGadeRealCSV, columns= ["Real_NO2", "Real_NOx"])

	return LGBMTagPredictData, LGBMTagRealData, LGBMGadePredictData, LGBMGadeRealData, LSTMTagPredictData, LSTMTTagRealData, LSTMTGadePredictData, LSTMTGadeRealData, LGBM24TagPredictData, LGBM24TagRealData, LGBM24GadePredictData, LGBM24GadeRealData