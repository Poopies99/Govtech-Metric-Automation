# All Constant Variables
import os
import json
import cloud

# --- PIVOTAL --- #
PIVOTAL_HEADERS = {"X-TrackerToken": os.getenv("PIVOTAL_API_TOKEN")}
def PIVOTAL_SQUAD_DETAILS():
    with open('/tmp/SquadDetails.json', 'r') as file:
        return json.load(file)
def PIVOTAL_STORIES_URL(projectID):
    return f"https://www.pivotaltracker.com/services/v5/projects/{projectID}/iterations?fields=stories(id,name,current_state,story_type,estimate,owners,labels(:default,has_epic),cycle_time_details)&limit=12&offset=-11&scope=done_current"
def PIVOTAL_VELOCITY_URL(projectID):
    return f"https://www.pivotaltracker.com/services/v5/projects/{projectID}?fields=current_velocity,current_volatility,current_standard_deviation"
def PIVOTAL_SPRINTS_URL(projectID):
    return f"https://www.pivotaltracker.com/services/v5/projects/{projectID}/releases?fields=id,name,deadline,points_total,points_accepted,counts_total,counts_accepted,accepted_at,current_state"
def PIVOTAL_COMMITTED_POINTS_URL(projectID, name):
    return f"https://www.pivotaltracker.com/services/v5/projects/{projectID}/search?fields=:default,epics(:default,epics(:default,follower_ids,past_done_story_estimates,past_done_stories_count,past_done_stories_no_point_count,label_id,label(:default,counts),comments(:default,attachments,reactions),pull_requests,branches))&query=label:%22{name}%22%20includedone:true&envelope=true"
def PIVOTAL_STORY_TRANSITIONS_URL(projectID, id):
    return f"https://www.pivotaltracker.com/services/v5/projects/{projectID}/stories/{id}/transitions"
def PIVOTAL_STORY_HISTORY_URL(projectID, id):
    return f"https://www.pivotaltracker.com/services/v5/projects/{projectID}/stories/{id}/activity?envelope=true/data"
    
# --- TEAMCITY --- #
TEAMCITY_BUILD_HEADER = {'Accept': 'application/json'}
def TEAMCITY_BUILD_URL(buildID):
    return f"https://teamcity.gahmen.tech/httpAuth/app/rest/builds/?locator=defaultFilter:false,finishDate:(date:20220401T203446,condition:after),state:finished,buildType:({buildID}),count:50&fields=nextHref,build(id,number,branchName,startDate,finishDate,status)"
def TEAMCITY_BUILD_AUTH():
    return (os.getenv("TEAMCITY_USER"), os.getenv("TEAMCITY_PW"))
def TEAMCITY_BUILD_DETAILS():
    with open('/tmp/BuildInfo.json', 'r') as file:
        return json.load(file)
        
# --- GOOGLE --- #
GOOGLE_BUCKET_NAME = 'bgp_metric'
def GOOGLE_DOWNLOAD_SOURCE_PATH():
    return cloud.filesToDownload()

# --- OS TEMP DIRECTORY --- #
OS_CREDIENTIALS = '/tmp/credientials.json'
OS_CSV_UPLOAD_DESTINATION_PATH = '/tmp/placeholder.csv'
OS_JSON_UPLOAD_DESTINATION_PATH = '/tmp/placeholder.json'
def OS_DOWNLOAD_DESINTATION_PATH():
    res = []
    for i in cloud.filesToDownload():
        res.append('/tmp' + i.replace("Data Files", ""))
    return res
    
# ---- Datetime --- #
DATETIME_DEADLINE_FORMAT = '%Y-%m-%dT%H:%M:%SZ' # Example: 2022-05-04T04:00:00Z
DATETIME_UTC_TO_LOCAL = 12
DATETIME_SPRINT_DURATION = 14 # One Sprint is 14 days
