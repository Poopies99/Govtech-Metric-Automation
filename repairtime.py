import datetime
import cloud
import constants
import build

def getMeanTimeToRepair():
    data = []
    
    for i in constants.TEAMCITY_BUILD_DETAILS():
        data += getMeanTime(i["ID"], i["Name"])
    
    cloud.uploadToCloud('FixTime.csv', data)

    return data
    
def getMeanTime(buildID, name):
    data = build.getTeamCityData(buildID, name)
    
    data = data[::-1]
    
    res = []
    
    for i in range(len(data)):
        if data[i]["finalStatus"] == "Failure" and notAnotherFailure(data, i):
            indexLimit = len(data) - 1
            # Edge Case where latest build is a failure
            if i >= indexLimit:
                break
            else:
                index = i
                numberOfBuilds = 0
                
                while index < indexLimit and data[index]["finalStatus"] != "Success":
                    index += 1
                    numberOfBuilds += 1
                
                res.append(generateData(data, i, index, numberOfBuilds))
            
    return res
    
def notAnotherFailure(data, index):
    if index == 0:
        return True
    else:
        if data[index - 1]["finalStatus"] == "Failure":
            return False
        else:
            return True
    
def generateData(data, failIndex, successIndex, numberOfBuilds):
    res = {
        "Deployment": data[failIndex]["name"],
        "End Time of Failed Build": data[failIndex]["finishDate"], 
        "End Time of Successful Build": data[successIndex]["finishDate"],
        "Number of Builds Taken to Fix": numberOfBuilds,
        "Sprint": data[failIndex]["sprint"],
        "Build ID": data[failIndex]["id"],
        "Link to Build": f'https://teamcity.gahmen.tech/viewLog.html?buildId={data[failIndex]["id"]}&buildTypeId=bgp_appian_deploy_03bDeployGccQa',
        "Hours Taken": findTimeTaken(data[failIndex]["finishDate"], data[successIndex]["finishDate"])
    }

    return res
    
def findTimeTaken(startTime, endTime):
    startTime = startTime.replace('T', '').replace('+', '')
    startTime = datetime.datetime.strptime(startTime, '%Y%m%d%H%M%S%f')
    
    endTime = endTime.replace('T', '').replace('+', '')
    endTime = datetime.datetime.strptime(endTime, '%Y%m%d%H%M%S%f')
    
    diff = endTime - startTime
    
    seconds = diff.seconds
    
    hours = seconds / 3600
    
    return round(hours, 2)