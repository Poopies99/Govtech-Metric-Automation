# Contains methods relevant to get current velocity info
import pivotaltracker
import constants
import cloud

"""
Function loops through all squad details and returns the current velocity, volatility and
standard deviation for each squad
"""
def getVelocityDetails():
    resVelocityData = []
    
    for i in constants.PIVOTAL_SQUAD_DETAILS():
        # Place return value into a list as convertToCSV method takes in a list parameter
        velocityData = [pivotaltracker.getVelocityDetails(i['Squad Name'], i["Pivotal Tracker Project ID"])]
        resVelocityData += velocityData
    
    cloud.uploadToCloud('VelocityInfo.csv', resVelocityData)    
    
    return resVelocityData
    