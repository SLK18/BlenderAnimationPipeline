import subprocess
import time
import os
import json

with open('./config.json', "r") as f:
    config = json.load(f)

BLENDER_EXE_PATH = config['BLENDER_EXE_PATH']
BLEND_FILE_TARGET_PATH = config['BLEND_FILE_TARGET_PATH']
MAX_RETRIES = config['MAX_RETRIES']

restart_counter = 0
while True:
    blender_agent = subprocess.Popen([BLENDER_EXE_PATH, BLEND_FILE_TARGET_PATH, "--python", "blender_agent.py"])
    
    try:
        if blender_agent.wait() != None:
            break
    except:
        print("Error occured")
    
    blender_agent.kill()
    
    restart_counter += 1
    if restart_counter > MAX_RETRIES:
       print("Requires human intervention")
       break
    time.sleep(10)

print("DONE")