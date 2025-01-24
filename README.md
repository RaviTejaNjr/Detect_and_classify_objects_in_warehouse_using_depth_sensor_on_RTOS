# Detect_and_classify_objects_in_warehouse_using_depth_sensor_on_RTOS
 Detect_and_classify_objects_in_warehouse_using_depth_sensor_on_RTOS

# Carton Detector

This Package uses a RealSense Camera to detect cartons for MASON to pick up.

## Structure

1. It starts a RealSense node, which provides the camera frames.
2. It runs a 2D Object Detector (YOLO-Backbone) to detect Cartons in the color Frame. 2D Bounding Boxes are outputted.
3. A `BoundingBox` Object is created.
4. These Bounding Boxes are then Filtered. Due to the low Precision, color filtering needs to applied to filter out the Boxes relevant for MASON.
5. If the Bounding Box is valid, it is appended to the `BoundingBoxManager`. The `BoundingBox` contains a method to create a `Detection` msg.
6. The `BoundingBoxManager` contains methods for visualization and ROS communication via the `DetectionList` msg.
7. The `DetectorNode` runs the OD in an infinite loop. The `DetectionList` is published under /detections/.

## Detailed explanaition

### `DetectorNode`

Subscribes to the Camera and Depth Frame of the RealSense Node. It runs the `Detector` infinitely and publishes its messages under `/detections/`. 

### `scripts/detector_module/`

A Python module that contains all code necessary for the `DetectorNode`. 

#### classes

| Class         | Description |
| :---         | --- |
| `BoundingBox` | Computes the relevant infos of the 2D and, with the Depth Frame, 3D Bounding Box. It performs a PCA to obtain the orientation. The Size is only valid if the Orientation angles (especially the `yaw`) is zero, since the 3D Bounding Box is built by getting the min/max values fromnthe depth frame snippet of the Bounding Box. |
| `BoundingBoxManager` | While running, the `BoundingBoxManager` fills its List of Detections. Note, that it uses a static List of Detections to avoid continuous memory allocations. The Length of the preallocated List can be changed in the `config` with `max_detections`. The classes main purpose is to publish the Detection List. |
|`Detector`| The main module. It runs the `YOLO` model and creates `BoundingBoxes`. It then appends the detections to the `BoundingBoxManager`. This `BoundingBoxmanager` is then returned in the call.

#### models

Contains the pretrained YOLO models.

#### runtime_setup

| file   | Description    |
|---------|----------------|
| `setup_model.py` | Sets the filters by checking `config["filters"]` for the filters ordered and then importing them from `runtime_setup/filters/` with the defined parameters. It then returns a list of callable filters.|
| `setup_logging.py` | **CURRENTLY UNUSED**. Sets up the logging configurations. Although Video Logging is available, it isn´t used in the node due to the infinite process horizon of the node and therefore the risk of flushing the size of the PC. |


#### config

```json
import time
import numpy as np

VISION = {
    "model":"models/Small_CB.pt",
    "filters":
        {
            'RGB':{
                'threshold':0.2,
                'min_filter': np.array([140,140,140]),
            },
            'HSV':{
                'threshold':0.3,
                'min_filter': np.array([0, 0, 130]),
                'max_filter': np.array([179, 90, 255]),
            }            
        },
    "detector":{
        "max_detections": 50
    }
}


#currently not used
ROBOT = {
    "model":"UR10",
    "ip":"192.168.0.4",
    "port":"50002"
}

LOGGING = {
    "status": True,
    "level": "INFO",
    "format": "[%(asctime)s] %(levelname)s: %(message)s",
    "logdir": "logs/",
    "video_log": False
}
```
