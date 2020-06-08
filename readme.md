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
    1. Download and unpack latest cluster_controller.zip from release tab
    2. Edit configs/cluster_main.json
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
### Device Setup

## Roadmap
    1. Add EEVEE support
    2. Make everyhong secure
    3. Add support for various output formats