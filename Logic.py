import json as j
from postpy2.core import PostPython
from postpy2.core import PostPython

runner = ""
abbrevation  = {"<class 'str'>":'String', "<class 'bool'>":'Boolean', "<class 'int'>":'Int', "<class 'list'>":'List'}


def ParseJSON(json, result = {}):
    abbrevation  = {"<class 'str'>":'String', "<class 'bool'>":'Boolean', "<class 'int'>":'Int', "<class 'list'>":'List'}
    for parentkey in json: 
        result[parentkey] = []
        child = json[parentkey][0] if type(json[parentkey]) == type([]) and json[parentkey]!=[] else json[parentkey]
        if type(child)==type({}):
            ParseJSON(child, result)
            for childkey in child:
                childvalue = child[childkey]
                if type(childvalue) == type({}) or (type(childvalue) == type([]) and childvalue!=[] and type[childvalue[0]]==type({})):
                    result[parentkey].append({childkey:childkey+'JSON'})
                    ParseJSON(childvalue, result)
                else:
                    result[parentkey].append({childkey:abbrevation[str(type(childvalue))]})
        if result[parentkey]==[]: del result[parentkey]
    return result

def Fetch(jsonfilepath):
    global runner
    runner = PostPython(jsonfilepath)
    print("Fetch successful") ####################

def Check(json):
    return json if type(json[next(iter(json))]) == type({}) else {'':json}

def ParsePostman(json, jsonfilepath):
    print("In ParsePostman function\n") ##################
    resultJSON = {}
    Fetch(jsonfilepath)
    json = json['item'][0]['item']
    for item in json:
        print(item, '\n') #################
        req = item['request']
        body = req['body']
        url = req['url']
        reqbody, url, name =  [body['raw'], url['raw'], item['name']]
        request = Check(j.loads(reqbody))      
        response = Check(getattr(runner.Lsams, name.strip().lower().replace(" ", "_"))().json())
        parsedrequest = ParseJSON(request, {})
        print(name+": ", url, '\nRequest:\n', parsedrequest, '\n') ##################
        parsedresponse = ParseJSON(response, {})
        print("Response:\n", parsedresponse, '\n') ################# 
        resultJSON[url] = {"Request":parsedrequest, "Response":parsedresponse}
    return resultJSON
