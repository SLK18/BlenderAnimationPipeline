import bpy
import time
import subprocess
import os
import json

old_start_keyframe = bpy.context.scene.frame_start
old_end_keyframe = bpy.context.scene.frame_end
TOTAL_FRAMES = (old_end_keyframe-old_start_keyframe)

IMG_EXT = '.' + bpy.context.scene.render.image_settings.file_format.lower()

with open('./config.json', "r") as f:
    config = json.load(f)

OUTPUT_DIR = bpy.context.scene.render.filepath
FPS = str(bpy.context.scene.render.fps)
skip_img_creation = config['skip_img_creation']

print("\nOUTPUT_DIR: ", OUTPUT_DIR)
print("GIVING BLENDER TIME TO INIT...")
time.sleep(2)

if not skip_img_creation:
    #Find potential crash point and then subtract 2 corrupt frames
    crash_position = old_start_keyframe
    
    flist = os.listdir(OUTPUT_DIR)
    file_batch_size = len(flist)
    
    if file_batch_size <= 2:
        for fname in flist:
            os.remove(OUTPUT_DIR+fname)
            crash_position -= 1
    else:
        for fname in flist:
            print(fname, crash_position)
            crash_position += 1
        #Push the start position two positions back past the crash point
        #and get rid of corrupt frames
        crash_position -= 2
        os.remove(OUTPUT_DIR+flist.pop())
        os.remove(OUTPUT_DIR+flist.pop())
        bpy.context.scene.frame_start = crash_position
    
    print("\nWORKING ON IMAGE SERIES...")
    bpy.ops.render.render(animation=True)
    print("DONE WITH IMAGE SERIES")
    
    #Export skipping image creation
    config['skip_img_creation'] = True
    with open("config.json", "w") as outfile: 
        json.dump(config, outfile)
else:
    print("SKIPPING TO VIDEO CREATION")

video_creator = subprocess.Popen(['ffmpeg', '-framerate', FPS, '-i', OUTPUT_DIR+'%04d'+IMG_EXT, '-crf', '2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'output.mp4'])

flist = os.listdir(OUTPUT_DIR)

#Cleanup
if video_creator.wait() == 0 and config['DEL_IMGS_ON_COMPLETE']:
    for fname in flist:
        os.remove(OUTPUT_DIR+fname)

quit()