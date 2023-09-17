import pandas as pd
import os
import json
import filenamepartextractor as fn

#%% Class: CSV Suite 
class CSVClass:
    def __init__(self,dataset):
        self.inputData = dataset
    
    def readcsv(self): #Returns dict of extracted dirpath, and CSV data in DataFrames with named columns
        data = pd.read_csv(self.inputData, sep=';', skipinitialspace=True,)
        dirpathMeta = fn.filenamepartextractor(self.inputData)
        dirpathMeta["data"] = data
        return dirpathMeta
    
    def savetocsv(self):
        oPath = os.path.join(self.inputData["dirpath"], f'{self.inputData["rootname"]}.{self.inputData["extension"]}')
        #print(oPath)
        self.inputData["data"].to_csv(oPath, sep=';',index=False)

#%% Class: JSON Suite
class JSONClass:
    def __init__(self,dataset):
        self.inputData = dataset

    def readjson(self):
        with open(self.inputData, 'r') as f:
            data = json.load(f)
        dirpathMeta = fn.filenamepartextractor(self.inputData)
        dirpathMeta["data"] = data
        return dirpathMeta
    
    def savejson(self):
        oPath = os.path.join(self.inputData["dirpath"], f'{self.inputData["rootname"]}.{self.inputData["extension"]}')
        with open(oPath, 'w') as f:
                json.dump(self.inputData["data"], f, indent=4)
