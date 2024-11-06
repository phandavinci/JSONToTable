import json as j
import Logic
import Convert

filepath = open('inputpostman.json', 'r')

try:
    json = j.load(filepath)
    if json=={}: raise Exception("JSON is empty")
except:
    print("Give a valid JSON file")

try: 
    parsedJSON = Logic.ParsePostman(filepath) 
    print(parsedJSON)
except Exception as error: 
    raise Exception(f"Error while parsing JSON, {error}")

try:
    Convert.ToWord(parsedJSON)
except Exception as error:
    raise Exception(f"Errow while converting to excel, {error}")


