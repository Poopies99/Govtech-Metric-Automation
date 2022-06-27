# Contains methods relevant to find cycle by state for each story
import main
import pivotaltracker
import constants
import cloud

"""
Function loops through all squad details and returns the cycle time details
for stories from each squad in this FY
"""
def getCycleTime():
    resStoryData = []
    
    for i in constants.PIVOTAL_SQUAD_DETAILS():
        url = constants.PIVOTAL_STORIES_URL(i["Pivotal Tracker Project ID"])
        storyData = main.fetchData(url, constants.PIVOTAL_HEADERS, None)
        storyData = filterStory(storyData, i["Squad Name"], i["Current FY First Sprint"], i["Pivotal Tracker Project ID"])
        resStoryData += storyData
        
    cloud.uploadToCloud('Stories.csv', resStoryData)
    
    return resStoryData

"""
Function returns an array of filtered stories
Stories are filtered with the following criteria
1. Stories belongs to the sprint in the current FY
2. Stories must have point estimates
3. Stories state must be accepted (Completed)
"""
def filterStory(data, team, sprintID, projectID):
    # An array of all sprint names this FY
    sprintList = pivotaltracker.getSprintList(team, sprintID, projectID)

    res = []
    
    for i in data:
        for j in i["stories"]:
            for k in j["labels"]:
                if k["name"] in sprintList and 'estimate' in j and j['current_state'] == 'accepted':
                    res.append(refine(j, team))
                    # Since some stories belong to multiple labels, we use break to avoid double counting
                    break
    
    return res

"""
Function returns the sprint that the story is completed on by iterating from the back of the label array
where the most recent label is found
"""              
def getSprint(item):
    for i in range(len(item["labels"])):
        lastIndex = len(item["labels"]) - 1
        if item["labels"][lastIndex - i]["name"].startswith('sprint'):
            return item["labels"][lastIndex - i]["name"]
            
def getLabels(item):
    res = []
    
    for i in item["labels"]:
        res.append(i)
    
    return res
    
def getHours(time):
    return time / 3600000

def getTotalCycle(item):
    try:
        return getHours(item["cycle_time_details"]["total_cycle_time"])
    except:
        return 0
        
def refine(item, team):
    data = {
        "Team": team,
        # Story belongs to the sprint that is labeled last
        "Sprint": getSprint(item),
        "State": item["current_state"],
        "Type": item["story_type"],
        "Estimate": item["estimate"],
        "Title": item["name"],
        "ID": item["id"],
        "Labels": getLabels(item),
        "Total Cycle Time(Hours)": getTotalCycle(item),
        "Start Time(Hours)": getHours(item["cycle_time_details"]["started_time"]),
        "Finished Time(Hours)": getHours(item["cycle_time_details"]["finished_time"]),
        "Delivered Time(Hours)": getHours(item["cycle_time_details"]["delivered_time"]),
        "Rejected Time(Hours)": getHours(item["cycle_time_details"]["rejected_time"])
      }
  
    return data
    
