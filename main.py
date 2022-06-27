import requests
import json
import pending
import constants
import build
import repairtime
import cycletime
import velocity
import sprintpoints
import cloud

def runAutomation(event, context):
    cloud.downloadFiles(constants.GOOGLE_DOWNLOAD_SOURCE_PATH(), constants.OS_DOWNLOAD_DESINTATION_PATH())
    
    # Cycle Time by State Metric
    cycletime.getCycleTime()
    
    # Current Velocity Metric
    velocity.getVelocityDetails()
    
    # Sprint Points Breakdown Metric
    sprintpoints.getSprintPoints()   
    
    # Time in Pending State Metric
    pending.generateTimeToQAReady()
    
    # Mean Time To Repair Metric 
    repairtime.getMeanTimeToRepair()
    
    # CI/QA Deployment Metric
    return build.getBuilds()

# Returns Unserialized Content
def fetchData(queryUrl, header, auth):
    data = requests.get(queryUrl, headers=header, auth=auth)
    
    return json.loads(data.text)