import boto3
import os
from os import path
import json
import time

### Read the environment variables 
from dotenv import load_dotenv
load_dotenv()

def generate_streaming_url():
       
    # Initialize the Kinesis Video client
    kvs = boto3.client('kinesisvideo', region_name=os.getenv("REGION_NAME"),
                                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    
    # Grab the endpoint from GetDataEndpoint
    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=os.getenv("STREAM_NAME")
    )['DataEndpoint']

    # Grab the HLS Stream URL from the endpoint
    kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint,region_name=os.getenv("REGION_NAME"),
                                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    
    url = kvam.get_hls_streaming_session_url(
        StreamARN = os.getenv("STREAM_ARN"),
        PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']
    
    # print(url)

    return url


def main():

    print("Generating HLS URL for Kinesis Video Streams")

    while True:
        try:
            stream_url = generate_streaming_url()
            # print(stream_url)
            if stream_url is not None:
                break
        except Exception as e:
            print(e)
        
        # Timer to wait before trying again incase the stream url has not been generated
        time.sleep(int(os.getenv("HLS_WAIT_TIMER")))
        
    print("#################################################################################################################")
    print("Stream started: ",stream_url)


###   
main()
