import main
import constants
import pivotaltracker
import json
import cloud

"""
Function returns the actual and committed story points for all sprints this FY 
"""
def getSprintPoints():
    res = []
    
    for i in constants.PIVOTAL_SQUAD_DETAILS():
        # Get sprint info (actual story points) based on the specified sprint ID
        sprintPoints = pivotaltracker.getSprintData(i["Squad Name"], i["Current FY First Sprint"], i["Pivotal Tracker Project ID"])
        
        committedPoints, refineCommittedPoints  = [], []
        
        # For each sprint this FY fetch the committed story points
        for j in sprintPoints:
            url = constants.PIVOTAL_COMMITTED_POINTS_URL(i["Pivotal Tracker Project ID"], j["name"])
            data = main.fetchData(url, constants.PIVOTAL_HEADERS, None)
            committedPoints.append(data)
        
        # Append into a new list JSON data detailing the actual and committed story points for each sprint
        for k in range(len(committedPoints)):
            refineCommittedPoints.append(refine(sprintPoints[k], committedPoints[k]))
            
        res += refineCommittedPoints
        
    # CSV File is a Metric File, JSON file is for Data File
    cloud.uploadToCloud('SprintPoints.csv', res)
    cloud.uploadToCloud('SprintPoints.json', res)
    
    return res
    
"""
Function returns JSON value of a sprint with the actual and committed story points included.
sprintPoints has the actual storyPoints while committedPoints has the committed story points
"""
def refine(item1, item2):
    data = {
        "Sprint": item1["name"],
        "Team": item1["team"],
        "Status": item1["current_state"],
        "Committed Story Points": item2["data"]["stories"]["total_points"],
        "Actual Story Points": item1["points_accepted"],
        "Start Time": item1["start_time"],
        "End Time": item1["end_time"]
    }
    
    return data 