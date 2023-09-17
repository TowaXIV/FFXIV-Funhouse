import pandas as pd
import os
import filenamepartextractor as fn

iFile = r'C:\Users\Martijn\Documents\Python\Funhouse\database\items.txt'

#%% Class: CSV Suite 

class CSVClass:
    def __init__(self,dataset):
        self.inputData = dataset
    
    def readcsv(self): #Returns dict of extracted dirpath, and CSV data in DataFrames with named columns
        data = pd.read_csv(self.inputData, sep=',', skipinitialspace=True,)
        dirpathMeta = fn.filenamepartextractor(self.inputData)
        dirpathMeta["data"] = data
        print(dirpathMeta)
        return dirpathMeta
    
    def savetocsv(self):
        oName = input("Name of file: ")
        self.inputData["rootname"] = oName

        oPath = os.path.join(self.inputData["dirpath"], f'{self.inputData["rootname"]}.{self.inputData["extension"]}')
        print(oPath)
        self.inputData["data"].to_csv(oPath, index=False)

if __name__ == "__main__":
    #debugging
    csvData = CSVClass(iFile).readcsv()
    #CSVClass(csvData).savetocsv()
