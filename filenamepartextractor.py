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
        #dirpath
        listDir = inputData.split('\\')
        listDir.pop(-1)
        dirpath = '\\'.join(listDir)
        #filename
        filename = inputData.split('\\')[-1]
        #rootname
        listName = filename.split('.')
        listName.pop(-1)
        rootname = '.'.join(listName)
        #extension
        extension = filename.split('.')[-1]
        #dirname
        dirname = dirpath.split('\\')[-1]
        
        dictDirpath = {
            "dirpath": dirpath,
            "filename": filename,
            "rootname": rootname,
            "extension": extension,
            "dirname": dirname
        }
        return dictDirpath

if __name__ == "__main__":
    print("This script should not be run on its own.")