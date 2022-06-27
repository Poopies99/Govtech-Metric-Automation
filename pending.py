# Contain methods relevant to find time in pending state
import os
import json
import constants
import re
import datetime
import main
import pivotaltracker
import cloud

def generateTimeToQAReady():
    res = []
    
    for i in constants.PIVOTAL_SQUAD_DETAILS():
        url = constants.PIVOTAL_STORIES_URL(i["Pivotal Tracker Project ID"])
        storiesData = main.fetchData(url, constants.PIVOTAL_HEADERS, None)
        sprintList = pivotaltracker.getSprintList(i["Squad Name"], i["Sprint 4020 Onwards"], i["Pivotal Tracker Project ID"])
        res += filterAndRefine(storiesData, sprintList, i["Squad Name"], i["Pivotal Tracker Project ID"])
    
    cloud.uploadToCloud('StartToQA.csv', res)
    
    return res
    
def filterAndRefine(stories, sprintList, team, projectID):
    storyList = []
    
    # Add Stories ONLY in this FY
    for i in stories:
        # Return object has "stories" parameter that needs to be specified
        for j in i["stories"]:
            for k in j["labels"]:
                if k["name"] in sprintList and j["current_state"] == 'accepted' and 'estimate' in j:
                    j["team"] = team
                    storyList.append(refine(j, team, projectID))
                    break
    
    return storyList

def refine(item, team, projectID):
    # Perhaps we should have it labelled as Appian or ROR
    data = {
        "Team": team,
        "Sprint": getSprint(item),
        "State": item["current_state"],
        "Type": item["story_type"],
        "Estimate": item["estimate"],
        # "Title": item["name"],
        "ID": item["id"],
        "Tag": getTag(item),
        "Time from Start to QA Available": getStartToQA(item, team, projectID)
    }
    
    return data

def getStartToQA(item, team, projectID):
    transitionsUrl = constants.PIVOTAL_STORY_TRANSITIONS_URL(projectID, item["id"])
    historyUrl = constants.PIVOTAL_STORY_HISTORY_URL(projectID, item["id"])
    
    storyTransitions = main.fetchData(transitionsUrl, constants.PIVOTAL_HEADERS, None)
    storyHistory = main.fetchData(historyUrl, constants.PIVOTAL_HEADERS, None)
    
    storyStartTime = getStoryStartTime(storyTransitions)
    storyEndTime = getQATime(storyHistory)
    
    if storyEndTime == None or storyStartTime == None:
        return "nil"
        
    return findTimeTaken(storyStartTime, storyEndTime)

def findTimeTaken(start, end):
    start = start.replace('T', '').replace('-', '').replace(':', '').replace('Z', '')
    start = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
    
    end = end.replace('T', '').replace('-', '').replace(':', '').replace('Z', '')
    end = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')
    
    diff = end - start
    
    seconds = diff.seconds
    
    hours = seconds / 3600
    
    return round(hours, 2)
    
def getQATime(storyHistory):
    for i in storyHistory:
        if i["highlight"] == 'edited':
            for j in i["changes"]:
                if 'name' in j and j["name"] == 'available in qa':
                    return i["occurred_at"]
    
def getStoryStartTime(storyTransitions):
    for i in storyTransitions:
        if i["state"] == "started":
            return i["occurred_at"]
            
def getTag(item):
    # Place longer tag names at the start since appian is in 'appian + ror'
    tags = ['appian + ror', 'ror + appian', 'devops + appian', 'appian + devops', 'ror + devops', 'devops + ror', 'devops', 'appian', 'ror']

    for i in item["labels"]:
        if i["name"] in tags:
            return i["name"]
            break
    
    # Some stories label tags directly within the name
    for i in tags:
        if i in item["name"].lower():
            return i
            
def getSprint(item):
    for i in range(len(item["labels"])):
        lastIndex = len(item["labels"]) - 1
        if item["labels"][lastIndex - i]["name"].startswith('sprint'):
            return item["labels"][lastIndex - i]["name"]
    