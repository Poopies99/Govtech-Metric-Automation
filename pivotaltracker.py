import main
import constants
import re
import datetime
from datetime import timedelta
import json

# Returns Sprint Details of Sprints in the Current FY  
def getSprintData(team, sprintID, projectID):
    url = constants.PIVOTAL_SPRINTS_URL(projectID)
    sprints = main.fetchData(url, constants.PIVOTAL_HEADERS, None) 
    
    refinedSprintList = []
    
    # ID of first sprint this FY
    for i in sprints:
        if i["id"] >= sprintID:
            # Change Sprint name to match story label, add team attribute, start and end time
            data = {
                "id": i["id"],
                "name": refineSprintName(i["name"]),
                "current_state": i["current_state"],
                "points_accepted": i["points_accepted"],
                "points_total": i["points_total"],
                "counts_accepted": i["counts_accepted"],
                "counts_total": i["counts_total"],
                "team": team,
                "end_time": adjustToLocalTime(i["deadline"]),
                "start_time": findStartTime(i["deadline"]),
            }
            
            refinedSprintList.append(data)
        
    return refinedSprintList
    
def refineSprintName(name):
    res = 'sprint' + re.sub("[^0-9]", "", name)

    return res[:10]

# Returns an array of strings containing the names of sprints4020 onwards
def getSprintList(team, sprintID, projectID):
    sprintList = []
    sprintData = getSprintData(team, sprintID, projectID)
    
    for i in sprintData:
        sprintList.append(i["name"])
    
    return sprintList

def getVelocityDetails(team, projectID):
    velocityData = main.fetchData(constants.PIVOTAL_VELOCITY_URL(projectID), constants.PIVOTAL_HEADERS, None)
    
    velocityData["team"] = team
    
    return velocityData
    
# Convert UTC Time to Local Time
def adjustToLocalTime(time):
    res = datetime.datetime.strptime(time, constants.DATETIME_DEADLINE_FORMAT)
    
    hoursDiff = timedelta(hours=constants.DATETIME_UTC_TO_LOCAL)
    
    res = res - hoursDiff
    
    return res.strftime("%Y-%m-%d %H:%M:%S")

# Returns the startTime by substrating each sprint duration  
def findStartTime(time):
    res = datetime.datetime.strptime(time, constants.DATETIME_DEADLINE_FORMAT)
    
    dayDiff = timedelta(days=constants.DATETIME_SPRINT_DURATION)
    
    res = res - dayDiff    
    
    return res.strftime("%Y-%m-%d %H:%M:%S")
    