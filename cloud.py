# Contains methods relevant to Google Cloud
from google.cloud import storage
import json
import os
import constants
import csv

def downloadFiles(source_array, destination_array):
    loadCredientials()
        
    storage_client = storage.Client.from_service_account_json(constants.OS_CREDIENTIALS)
    bucket = storage_client.bucket(constants.GOOGLE_BUCKET_NAME)
    
    # Iterate through source and destination array to download into non-persistent disk space
    for i in range(len(source_array)):
        blob = bucket.blob(source_array[i])
        blob.download_to_filename(destination_array[i])
       
# Upload CSV/JSON Files into google cloud 
def uploadToCloud(destinationPath, data):
    sourcePath = formatFile(data, destinationPath)
    destinationPath = getGoogleDestinationPath(destinationPath)

    loadCredientials()
    
    storage_client = storage.Client.from_service_account_json(constants.OS_CREDIENTIALS)
    bucket = storage_client.bucket(constants.GOOGLE_BUCKET_NAME)
    
    blob = bucket.blob(destinationPath)
    blob.upload_from_filename(sourcePath)
    
def loadCredientials():
    crediential_dict = {
        'type': 'service_account',
        'client_id': os.getenv("GOOGLE_CLIENT_ID"),
        'client_email': os.getenv("GOOGLE_CLIENT_EMAIL"),
        'private_key_id': os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        'private_key': os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
        "token_uri": os.getenv("TOKEN_URI"),
    }
    
    with open(constants.OS_CREDIENTIALS, 'w') as file:
        file.write(json.dumps(crediential_dict))

# Function stores file based on the format specified in destination path (Google cloud)
# And returns the correct source path (IMPORTANT)
# Stored within an instance (non-persistent disk space)
def formatFile(data, path):
    # Specified path must be in CSV Format
    if 'csv' in path:
        with open(constants.OS_CSV_UPLOAD_DESTINATION_PATH, 'w') as f:
            writer = csv.DictWriter(f, data[0].keys())
            writer.writeheader()
            
            for i in data:
                writer.writerow(i)
                
        return constants.OS_CSV_UPLOAD_DESTINATION_PATH
        
    else:
        with open(constants.OS_JSON_UPLOAD_DESTINATION_PATH, 'w') as file:
            file.write(json.dumps(data))
            
        return constants.OS_JSON_UPLOAD_DESTINATION_PATH
        
def getGoogleDestinationPath(path):
    if 'csv' in path:
        return 'Metric Files/' + path
    else:
        return 'Data Files/' + path
        
def filesToDownload():
    loadCredientials()
    
    storage_client = storage.Client.from_service_account_json(constants.OS_CREDIENTIALS)
    blobs = storage_client.list_blobs(constants.GOOGLE_BUCKET_NAME)
    
    res = []
    
    for blob in blobs:
        if 'Data Files' in blob.name and 'json' in blob.name: 
            res.append(blob.name)
        
    return res