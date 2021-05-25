import re
import requests
import json as json

# Function to check if email valid
def checkEmail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return(True)
    else:
        return(False)
 

class oecdAPI():
    def oecdGetSeries(dataref,variable,location):
        if variable['keyPosition']==0:
            link = f"https://stats.oecd.org/SDMX-JSON/data/{dataref}/{variable['id']}.{location['id']}"
        else:
            link = f"https://stats.oecd.org/SDMX-JSON/data/{dataref}/{location['id']}.{variable['id']}"

        response = requests.get(link)
        return(response.json())


    def oecdOutput(dataref,variable,location):
        data = oecdAPI.oecdGetSeries(dataref,variable,location)
        # Data
        series = [obs[0] for obs in data['dataSets'][0]['series']['0:0']['observations'].values()] # Accessing data
        years = [year['id'] for year in data['structure']['dimensions']['observation'][0]['values']]#years

        #Meta data
        meta = data['structure']['attributes']['series']
        finalSet = {} 
        for i in range(len(meta)):
            if meta[i]['values']:
                finalSet[meta[i]['name'].lower()] = meta[i]['values'][0]['name']

        # Adding variable name & location
        structure = data['structure']['dimensions']['series']
        for i in range(len(structure)):
            if structure[i]['values'][0]['name'] == "country":
                tempo = "location"
            else:
                tempo = structure[i]['values'][0]['name']
            finalSet[structure[i]['name'].lower()] = tempo

        # Adding data
        finalSet['data']={}
        for pos in range(len(series)):
            finalSet['data'][years[pos]] = series[pos]

        # Adding source & dataset title
        finalSet['source']='OECD'
        finalSet['title']=data['structure']['name']
        
        return(finalSet)