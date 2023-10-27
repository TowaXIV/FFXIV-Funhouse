import pandas as pd
import os
import json
import filenamepartextractor as fn
import logging

#%% Logging boot
logger = logging.getLogger(__name__)

logger.info(f'Activated logger.')

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
        logger.info('Start class "JSONClass".')
        self.inputData = dataset
        logger.info(f'End class "JSONClass" initialization.')

    def readjson(self):
        logger.info('Start function "readjson".')
        logger.info(f'Load file {self.inputData}.')
        with open(self.inputData, 'r') as f:
            data = json.load(f)
        logger.info('Enrich data with dirpath metadata.')
        dirpathMeta = fn.filenamepartextractor(self.inputData)
        dirpathMeta["data"] = data
        logger.info('Return data to function call.')
        return dirpathMeta
    
    def savejson(self):
        logger.info('Start function "savejson".')
        logger.debug(f'Key "dirpath" set to value: "{self.inputData["dirpath"]}".')
        logger.debug(f'Key "rootname" set to value: "{self.inputData["rootname"]}".')
        logger.debug(f'Key "extension" set to value: "{self.inputData["extension"]}".')
        oPath = os.path.join(self.inputData["dirpath"], f'{self.inputData["rootname"]}.{self.inputData["extension"]}')
        with open(oPath, 'w') as f:
                json.dump(self.inputData["data"], f, indent=4)
        logger.info('End function "savejson".')
