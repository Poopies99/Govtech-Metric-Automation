# Contains methods relevant to TeamCity
import json
import os
import main
import constants
import cloud

def getBuilds():
    data = []
    
    for i in constants.TEAMCITY_BUILD_DETAILS():
        data += getTeamCityData(i["ID"], i["Name"])
    
    cloud.uploadToCloud('Builds.csv', data)
    
    return data
    
def getTeamCityData(buildID, buildName):
    data = main.fetchData(constants.TEAMCITY_BUILD_URL(buildID), constants.TEAMCITY_BUILD_HEADER, constants.TEAMCITY_BUILD_AUTH())

    # Add additional Info
    for i in data["build"]:
        i["buildID"] = buildID
        i["name"] = buildName
        i["sprint"] = findSprint(i["finishDate"])
        i["finalStatus"] = getFinalStatus(i)
        
    return data["build"]
    
def findSprint(completeTime):
    with open('/tmp/SprintPoints.json', 'r') as file:
        info = json.loads(file.read())
        info = info[::-1]
        for i in info:
            if changeTimeFormat(i["End Time"]) > completeTime > changeTimeFormat(i["Start Time"]):
                return i["Sprint"]
                
def getFinalStatus(data):
    currentStatus = data["status"]
    temp = []

    with open('/tmp/BuildStatus.json', 'r') as file:
        temp = json.loads(file.read())
        
    for i in temp:
        if i["Build ID"] == str(data["id"]):
            return "Success"
            
    if currentStatus == "SUCCESS":
        return "Success"
    elif currentStatus == "FAILURE":
        return "Failure"
    else:
        return "Unknown"
        
def changeTimeFormat(time):
    res =  time.replace('-', '').replace(':', '').replace('.', '+').replace('Z','0')
    return res