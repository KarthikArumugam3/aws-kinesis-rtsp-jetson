# Amazon KinesisVideoStreams Linux Nvidia Jetson

### 1. In this project first we will setup Amazon Kinesis Video Streams on a Linux system, for following architectures:-
1. x86_64(64 bit arch, ex:- Ubuntu)
2. ARM (Advanced RISC Machines, ex:- Jetson Nano/Orin Nano, Raspberry Pi)

### 2. Setup Guide can be found here  [Kinesis Setup](https://docs.google.com/document/d/1hzinUz4ITGDOXObwDEF3nb8SJuu1cu8gX2HoPBd_os0/edit?usp=sharing). Following is covered in the documentation:-
1. Setting up KVS using CPP producer.
2. Commands for streaming video with voice in realtine from camera a local machine to remote Kinesis server on AWS.


### 3. Setting up python environment :-

##### Setting up and activating conda virtual environment:-
```
conda create --prefix ./envs python=3.x
conda activate ./envs
```

##### Setting up and activating python virtual environment using virtualenv:-
```
sudo apt install python3-virtualenv
virtualenv -p /usr/bin/python3.x <env_name>
source <env_name>/bin/activate
```

##### Setting up and activating environment using venv:-
```
python3.x -m venv <env_name>
source <env_name>/bin/activate
```


##### Installing requirements:-

```
pip install -r requirements.txt
```

#### 4. Streaming & Consuming Realtime feed from AWS to any remote machine using a python client.
1. Once the kinesis has be successfully setup run the following to start the live streaming from a local system:-
Setup the necessary configuration in file called "config.json"
```
python kinesis_producer.py
```
**Note**:- The streaming can be stopped by simply pressing "Enter" key.

2. Run the following to get the live streaming url for consuming the feed from Kinesis:-
Setup the necessary configuration in file called ".env"
```
python get_hls_endpoint.py
```

