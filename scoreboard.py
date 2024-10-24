import json
from datetime import date
import os

class scoreboard:
    def __init__(self,fileLocation):
        self.fileLocation = fileLocation
    #Method to load the scores to memory
    def loadScores(self) -> list[dict]:
        #Check the file exist and the size is positive
        if os.path.exists(self.fileLocation) and os.stat(self.fileLocation).st_size > 0:
            file = open(self.fileLocation, "r")
            #load the json file content
            try:
                scores = json.load(file)
                return scores
            except:
                print("Scores file format is invalid or does not exist.")
                return []
    #Method to write a given score and name in the json file
    def writeScore(self,name,result):
        score = {
            "score": result,
            "name": name
        }
        #Check if file exist and the size is positive
        if os.path.exists(self.fileLocation) and os.stat(self.fileLocation).st_size > 0:
            #read existing file and append new data
            with open(self.fileLocation,"r") as file:
                loaded = json.load(file)
            loaded.append(score)
        else:
            #create new json
            loaded = [score]
        #overwrite/create file
        with open(self.fileLocation,"w") as scores:
            json.dump(loaded,scores)