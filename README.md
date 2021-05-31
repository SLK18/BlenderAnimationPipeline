# BlenderAnimationPipeline

The dilemna: It is only possible render images or the whole video in blender.
These scripts aim to automate the process so that upon an abrupt crash, it will recover and resume at the crash point.

## Installation

Dependencies:
There are no python dependencies, however, ffmpeg is required to be a command on your machine. There are different flags you can add to ffmpeg that can impact the quality of your output. If you want to add more flags to ffmpeg or change video output type edit blender_agent.py.

## Settings
Edit the config by adding the blend.exe path and the blend file target path. The script will pull FPS and the image extension from blender.

## Running
Place the BlenderAnimationPipeline folder in the same folder as your blend file. Do python main.py to start the process.

## Notes

The script will set skip_img_creation to true every time it completes a batch as a checkpoint mechanism. In order to do a new batch, empty your image output directory and set skip_img_creation to false. Blender might be greyed out when the script runs, so use the command window to track progress. In addition, the script doesn't currently handle timeouts.