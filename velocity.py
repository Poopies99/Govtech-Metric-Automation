# Contains methods relevant to get current velocity info
import pivotaltracker
import constants
import cloud

def getVelocityDetails():
    # Place return value into a list as convertToCSV method has a list parameter
    
    resVelocityData = []
    
    for i in constants.PIVOTAL_SQUAD_DETAILS():
        velocityData = [pivotaltracker.getVelocityDetails(i['Squad Name'], i["Pivotal Tracker Project ID"])]
        resVelocityData += velocityData
    
    cloud.uploadToCloud('VelocityInfo.csv', resVelocityData)    
    
    return resVelocityData
    