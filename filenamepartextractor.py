import logging

logger = logging.getLogger(__name__)

logger.info(f'Activated logger.')

r"""
Python script that takes a string directory input,
parses the input and returns numerous outputs:

Input: C:\Users\<User>\Documents\Python\Funhouse\items.txt

dirpath: C:\Users\<User>\Documents\Python\Funhouse
filename: items.txt
rootname: items
extension: txt
dirname: Funhouse
"""
def filenamepartextractor(inputData): #Inspired by FME's FileNamePartExtractor transformer.
        logging.info('Start function "filenamepartextractor".')
        #dirpath
        listDir = inputData.split('\\')
        listDir.pop(-1)
        dirpath = '\\'.join(listDir)
        logging.debug(f'Key "dirpath" set to value: "{dirpath}".')
        #filename
        filename = inputData.split('\\')[-1]
        logging.debug(f'Key "filename" set to value: "{filename}".')
        #rootname
        listName = filename.split('.')
        listName.pop(-1)
        rootname = '.'.join(listName)
        logging.debug(f'Key "rootname" set to value: "{rootname}".')
        #extension
        extension = filename.split('.')[-1]
        logging.debug(f'Key "extension" set to value: "{extension}".')
        #dirname
        dirname = dirpath.split('\\')[-1]
        logging.debug(f'Key "dirname" set to value: "{dirname}".')

        dictDirpath = {
            "dirpath": dirpath,
            "filename": filename,
            "rootname": rootname,
            "extension": extension,
            "dirname": dirname
        }
        logger.info('Return data to function call.')
        return dictDirpath

if __name__ == "__main__":
    print("This script should not be run on its own.")