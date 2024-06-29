from subprocess_utils import GStreamerProcess
# import time
from os import path
import json

class KinesisProducer(GStreamerProcess):

    def __init__(self, capture_width:int=640, capture_height:int=640, \
                 frame_rate:int=12, **kwargs) -> None:
        
        camera_id = kwargs.get('camera_id',None)
        aws_stream_name = kwargs.get('aws_stream_name', None)
        aws_access_key = kwargs.get('aws_access_key', None)
        aws_secret_key = kwargs.get('aws_secret_key', None)
        aws_region = kwargs.get('aws_region', None)


        
        self.pipeline_str  = f"gst-launch-1.0 -v v4l2src device={camera_id} ! videoconvert ! video/x-raw,width={capture_width},height={capture_height},framerate={frame_rate}/1,format=I420 ! x264enc  bframes=0 key-int-max=45 bitrate=500 tune=zerolatency ! h264parse ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink name=sink stream-name={aws_stream_name} access-key={aws_access_key} secret-key={aws_secret_key} aws-region={aws_region} alsasrc device=hw:0,0 ! audioconvert ! avenc_aac ! queue ! sink."

        print(self.pipeline_str)

        super().__init__(command=self.pipeline_str)


    # # Local method 
    # def start(self):
    #     self.process = subprocess.run(self.pipeline_str, shell=True, check=True)


if __name__ == '__main__':
    
    with open(path.join(path.dirname(__file__), "config.json"), "r") as f:
        config = json.load(f)

    capture_width = config["capture_width"]
    capture_height = config["capture_height"]
    frame_rate = config["frame_rate"]
    camera_id = config["camera_id"]
    aws_stream_name = config["aws_stream_name"]
    aws_access_key = config["aws_access_key"]
    aws_secret_key = config["aws_secret_key"]
    aws_region = config["aws_region"]

    with KinesisProducer(capture_width=capture_width, capture_height=capture_height, frame_rate=frame_rate,camera_id=camera_id, \
                                aws_stream_name=aws_stream_name, aws_access_key=aws_access_key, \
                                aws_secret_key=aws_secret_key, aws_region=aws_region) as kinesis_producer_client:
        kinesis_producer_client.start()
        print("Enter to Stop the streaming")
        input()  # Wait for the user to press Enter
        print("Closing the streaming")
    