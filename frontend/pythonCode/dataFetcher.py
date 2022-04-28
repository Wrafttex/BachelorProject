import pandas as pd

def dataHandler():
        # Tag CSV
        tagPredictCSV = pd.read_csv(r"frontend\data\Aalborg_Tag_Predicted_output.csv")
        tagRealCSV    = pd.read_csv(r"frontend\data\Aalborg_Tag_Real_output.csv")

        # Gade CSV
        gadePredictCSV = pd.read_csv(r"frontend\data\Aalborg_Gade_Predicted_output.csv")
        gadeRealCSV    = pd.read_csv(r"frontend\data\Aalborg_Gade_Real_output.csv")

        # Extracting Tag Data
        tagPredictData = pd.DataFrame(tagPredictCSV, columns= ["NO2", "NOX", "O3"])
        tagRealData    = pd.DataFrame(tagRealCSV, columns= ["NO2", "NOX", "O3"])

        ##tagPredictNO2 = tagPredictData["NO2"].tolist()
        ##tagPredictNOX = tagPredictData["NOX"].tolist()
        ##tagPredictO3  = tagPredictData["O3"].tolist()
        ##tagRealNO2    = tagRealData["NO2"].tolist()
        ##tagRealNOX    = tagRealData["NOX"].tolist()
        ##tagRealO3     = tagRealData["O3"].tolist()

        # Extracting Gade Data
        gadePredictData = pd.DataFrame(gadePredictCSV, columns= ["NO2", "NOX"])
        gadeRealData    = pd.DataFrame(gadeRealCSV, columns= ["NO2", "NOX"])

        ##gadePredictNO2 = gadePredictData["NO2"].tolist()
        ##gadePredictNOX = gadePredictData["NOX"].tolist()
        ##gadeRealNO2    = gadeRealData["NO2"].tolist()
        ##gadeRealNO2    = gadeRealData["NOX"].tolist()

        return tagPredictData, tagRealData, gadePredictData, gadeRealData