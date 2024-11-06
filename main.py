import json as j
import Logic
import Convert

jsonfilepath = 'C:\A\Atlas\Personal\Script\JsonToTable\inputpostman.json'
with open(jsonfilepath, 'r') as file:
    json = j.load(file)

if json=={}: raise Exception("JSON is empty")


print("Entered Postman\n")

parsedJSON = Logic.ParsePostman(json, jsonfilepath) 

print("Parsed the Postman collection:\n", parsedJSON, '\n')

Convert.ToWord(parsedJSON)

print("Word Document Created")

