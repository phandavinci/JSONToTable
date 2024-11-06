import json as j
from postpy2.core import PostPython

runner = ""

def ParseJSON(json, result = {}):
    abbrevation  = {"<class 'str'>":'String', "<class 'bool'>":'Boolean', "<class 'int'>":'Int', "<class 'list'>":'List'}
    parentkey = next(iter(json)) 
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
    from postpy2.core import PostPython
    runner = PostPython(jsonfilepath)

def Check(json):
    return json if type(json[next(iter(json))]) == type({}) else {'':json}

def ParsePostman(jsonfilepath):
    JSON = {jsonfilepath}
    Fetch()
    for item in JSON.item.item:
        req = item.request
        method, header, reqbody, url, name =  [req.method, req.header, req.body.raw, req.url.raw, item.name]
        response = getattr(runner.Lsams, name.strip().lower().replace(" ", "_"))().json()
        JSON[url] = {
            'Request':ParseJSON(Check(reqbody)), 
            'Response': ParseJSON(Check(response))
        }
    return JSON
