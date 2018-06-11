import urllib.parse as urlparse
from urllib.parse import urlencode
import requests
import re

serverURL = "http://127.0.0.1:5000/"

def getRequestType(string):
    if(string == "CreateAction"):
        return "POST"
    if(string == "UpdateAction"):
        return "PUT"
    if(string == "DeleteAction"):
        return "DELETE"
    return "GET"

def getURL(jsonPart):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if(isinstance(jsonPart,list)):
        for i in jsonPart:
            url = getURL(value)
            if(url != None):
                return url
    else:
        for key, value in jsonPart.items():
            if(isinstance(value, dict) or isinstance(value, list)):
                url = getURL(value)
                if(url != None):
                    return url

            if(re.match(regex,value) is not None):
                return value
    return None

class Action():
    def __init__(self,jsonPart, modifiable):
        self.isModifiable = modifiable
        self.type = getRequestType(jsonPart["@type"])
        self.url = getURL(jsonPart)
        if(self.url != None):
            self.path = list(urlparse.urlparse(self.url))[2]
        else:
            self.path = "UNKNOWN"


    def __repr__(self):
        return str(self.path) + " " + str(self.type) + " " + str(self.url) + " " + str(self.isModifiable)

    def __str__(self):
        return str(self.path) + " " + str(self.type)

# get an url and modify its parameters
no = "nN"
def modParams(url):
    full_query = urlparse.urlparse(url).query
    par = urlparse.parse_qs(full_query)
    url_parts = list(urlparse.urlparse(url))
    rmList = []
    for ob in par:
        setParam = "Y"
        print("set param " + str(ob) + "? (Y/n) ")
        setParam = input()
        if(setParam in no and len(setParam)>0):
            rmList.append(ob)
        else:
            print("new param value:")
            par[ob] = input()
            while(len(par[ob]) < 1):
                print("Ivalide input -> new param value:")
                par[ob] = input()
    for ob in rmList:
        del par[ob]
    url_parts[4] = urlencode(par)
    return str(urlparse.urlunparse(url_parts))


actions = ["CreateAction","UpdateAction","SearchAction","DeleteAction"]
def isAction(string):
    for ob in actions:
        if(string == ob):
            return True
    return False

#search in an json for different actions
def getActions(jsonPart, ActionList,modifiable ):
    if(isinstance(jsonPart,list)):
        for i in jsonPart:
            getActions(i, ActionList,modifiable)
    elif('@type' in jsonPart and isAction(jsonPart["@type"])):
        action = Action(jsonPart,modifiable)
        if(action.url != None):
            ActionList.append(action)
    else:
        for key, value in jsonPart.items():
            if(isinstance(value, dict) or isinstance(value, list)):
                getActions(value, ActionList,modifiable)

def chooseAction(ActionList):
    if(len(ActionList) < 1):
        print("No Actions available")
        return
    for index,ob in enumerate(ActionList):
        print(str(index) + ") " + str(ob))
    print("Choose Action: ")
    n = input();
    while(not n.isdigit() or int(n) < 0 or int(n) > len(ActionList) - 1 ):
        print("Invlide -> Choose Action: ")
        n = input();
    n = int(n)
    action = ActionList[n]
    url = action.url

    #mod action
    if(action.isModifiable):
        url = modParams(url)

    data = {}
    #run action
    if(action.type == 'PUT'):
        resp = requests.put(url=url)
        if("json" in resp.headers['content-type']):
            data = resp.json()
    if(action.type == 'POST'):
        resp = requests.post(url=url)
        if("json" in resp.headers['content-type']):
            data = resp.json()
    if(action.type == 'GET'):
        resp = requests.get(url=url)
        if("json" in resp.headers['content-type']):
            data = resp.json()
    if(action.type == 'DELETE'):
        resp = requests.delete(url=url)
        if("json" in resp.headers['content-type']):
            data = resp.json()
    if(len(data) > 0):
        print(data)
        print("list Actions? (Y/n)")
        listActions = input()
        recActionList = []
        if(not (listActions in no and len(listActions)>0)):
            getActions(data,recActionList,False)
            chooseAction(recActionList)
    else:
        print(resp)



if __name__ == '__main__':
    ActionList = []

    #get json
    data = {}
    resp = requests.get(url=serverURL)
    if("json" in resp.headers['content-type']):
        data = resp.json()

    #get available actions
    getActions(data,ActionList,True)
    loop = True
    loopStr = "T"
    while(loop):
        chooseAction(ActionList)
        print("Wanna run another action? (Y/n)")
        loopStr = input()
        loop = (not (loopStr in no and len(loopStr)>0))


