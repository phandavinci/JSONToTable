import json as j
import re
from postpy2.core import PostPython

runner = ""

def ParseJSON(json, result = {}):
    abbrevation  = {"<class 'str'>":'String', "<class 'bool'>":'Boolean', "<class 'int'>":'Int', "<class 'list'>":'List', "<class 'float'>":'Float', "<class 'NoneType'>":'None'}
    for parentkey in json: 
        result[parentkey] = []
        child = json[parentkey][0] if type(json[parentkey]) == type([]) and json[parentkey]!=[] else json[parentkey]
        if type(child)==type({}):
            ParseJSON(child, result)
            for childkey in child:
                childvalue = child[childkey]
                if type(childvalue) == type({}) or (type(childvalue) == type([]) and childvalue!=[] and type[childvalue[0]]==type({})):
                    result[parentkey].append({childkey:childkey})
                    ParseJSON(childvalue, result)
                else:
                    result[parentkey].append({childkey:abbrevation[str(type(childvalue))]})
        if result[parentkey]==[]: del result[parentkey]
    return result

def Fetch(jsonfilepath):
    global runner
    runner = PostPython(jsonfilepath)
    print("Fetch successful") ####################

def Check(json_str):
    json_str = re.sub(r'(?<=: )(?=,|})', '""', json_str)
    json = j.loads(json_str)
    return json if type(json) == type({}) and type(json[next(iter(json))]) == type({}) else {'':json}

def FixJSONName(name):
    return name.strip().lower().replace(" ", "_")

def GetReqBodyForGET(url):
    cleanedURL = url.split('?')[-1].split('&')
    convertedURL = {item.split('=')[0]:item.split('=')[1] for item in cleanedURL}
    return str(convertedURL).replace("'", '"')

def FormatURL(url, method):
    return f'({method})/'+'/'.join(url.split('?')[0].split('/')[3:])

def ParsePostman(json, jsonfilepath):
    Fetch(jsonfilepath)

    resultJSON = {}
    json = json['item'][0]['item']

    for item in json:
        req = item['request']
        url = req['url']['raw']
        method = req['method']
        name = item['name']
        
        requesttext = req['body']['raw'] if method != 'GET' else GetReqBodyForGET(url)
        request = Check(requesttext)     
        parsedrequest = ParseJSON(request, {})
        print(f"############ {name} : {url} ###################", '\nRequest:\n', parsedrequest, '\n') ################## 

        responsetext = getattr(runner.Lsams, FixJSONName(name))().text
        response = Check(responsetext)
        parsedresponse = ParseJSON(response, {})
        print("Response:\n", parsedresponse, '\n') ################# 

        resultJSON[FormatURL(url, method)] = {"Request":parsedrequest, "Response":parsedresponse}
    return resultJSON
