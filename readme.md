# Cluster rendering for blender ![Generic badge](https://img.shields.io/badge/status-PreAlpha-<COLOR>.svg)

:exclamation::exclamation::exclamation:This Project is **NOT PRODUCTION READY**:exclamation::exclamation::exclamation:

Since blender 2.78 there was no avilable cluster rendering option for individuals, 
that I was aware of. So I decided to write such a solution myself. Right now is more of a proof of concept, 
rather than a complete product, but hey, it works.

## How does it work?

Cluster controller is expected to export a network folder. Once a zipped 
.blend project gets dropped into it, this file get analyzed and frames to render
get split between all configured render devices. Every render device copies the project
to it's own disk space and than renders assigned frames. Once rendering is done every frame 
is sent back to the network exported folder. 

## Compatibility

| Feature       | Compatible?   |
| ------------- | ------------- |
| **CYCLES**        | :heavy_check_mark: |
| **EEVEE**         | :x: |
| **GPU RENDER**    | :heavy_check_mark: |
| **Image Sequence Render** | :heavy_check_mark: |
| **Any Other Output Format**  | :x: |

This project was developed to run on Linux and MacOS hosts, however there's nothing preventing it from running on Windows platform.

## Setup

Setup is divided into two main parts:

[Cluster Controller Setup](#Cluster-Controller-Setup)  
[Device Setup](#Device-Setup)

### Cluster Controller Setup
    1. Set up network exported folder
    2. Download and unpack latest cluster_controller.zip from release tab
    3. Edit configs/cluster_main.json
    listen_path is where you want this program to listen for files to render
    temp_path is folder used for temporary file. Best to leave as /tmp on linux and macOS
    port is the port used for both web dashboard and device communication
    eg.
```json
{
  "listen_path" : "/exports/listen_folder",
  "temp_path": "/tmp",
  "port": 2452
}
```
    4. Edit device files in devices directory. Filenames don't matter as every file in this directory is parsed.
    Evey device needs seperate file in this directory. Set up as following:
    ip - is devices up address
    hwid - is a unique identifier, make sure that corresponding device has same hwid set
    performance - is determining what part of the render this device will recieve (higher is more frames to render)
    port - leave default if you didn't change it in the device
```json
{
  "ip": "172.16.0.22",
  "hwid": "whatever",
  "performance": 1,
  "port": 2540
}
```
    5. Run cluster_main.py
### Device Setup
    1. Mount cluster exported file
    2. Unpack cluster_device from cluster_controller.zip on your device
    3. Install blender
    4. edit config/config.json
    port - port on whitch to operate
    blender_command - command that runs blender, can be full blender path
    hwid - unique id, make sure you set the same on cluster side configuration for this device
    tmp_path - directory for temporary files
    network_mount - path to mounted network folder
    server_address - servers ip address
    server_port - cluster controllers port, set to same as in cluster_main.json
```json
{
  "port": 2540,
  "blender_command": "blender",
  "hwid": "whatever",
  "tmp_path": "/tmp",
  "network_mount": "/exported/by/controller",
  "server_address": "172.16.0.21",
  "server_port": 2452
}
```
    5. run cluster_device.py

Note that if you run both cluster controller and device on one system you need to set up 2 separate tmp folders
    
## Usage
    1. Mount network exported folder on your workstation
    2. Copy zipped blender project to mounted folder
   
## Roadmap
    1. Add EEVEE support
    2. Make everyhong secure (cuz now it's not)
    3. Add support for various output formats
    4. Docker support