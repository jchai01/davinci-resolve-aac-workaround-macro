#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
import subprocess
import time
import os

# where to store the output audio file, make sure the path exist (in this case, ~/temp)
# by default, this script stores them in: /home/$USER/temp/
outputDir = "/home/" + os.getlogin() + "/temp/"

# location of your ffmpeg installation
ffmpeg = "/usr/bin/ffmpeg"

# get the clipname of the current video, where the playhead is currently resting on
resolve = dvr_script.scriptapp("Resolve")
clipName = (
    resolve.GetProjectManager()
    .GetCurrentProject()
    .GetCurrentTimeline()
    .GetCurrentVideoItem()
    .GetName()
)

# get the absolute file path all the video clips in video track 1
track_items = (
    resolve.GetProjectManager()
    .GetCurrentProject()
    .GetCurrentTimeline()
    .GetItemsInTrack("video", 1)
)
full_file_path = None
for item in track_items.values():
    media_pool_item = item.GetMediaPoolItem()
    if clipName == media_pool_item.GetClipProperty("File Path").split("/")[-1]:
        full_file_path = media_pool_item.GetClipProperty("File Path")
if full_file_path == None:
    print("Unable to get full file path of video")
    exit(1)

outputClipName = None
video_container_list = ["mp4", "mov", "mkv", "m4a", "avi", "webm", "wmv"]
current_video_container = clipName.split(".")[-1].lower()
for i in video_container_list:
    if current_video_container == i:
        outputClipName = clipName.lower().replace(i, "wav")
        break
if outputClipName == None:
    print("Unknown video format")
    exit(1)

mediaPool = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()


def buildFFmpegCommand():
    commands_list = [
        ffmpeg,
        "-i",
        full_file_path,
        outputDir + outputClipName,
        "-n",  # do not overwrite existing files
    ]
    return commands_list


def runFFmpeg(commands):
    if subprocess.run(commands).returncode == 0:
        print("ffmpeg script ran successfully")

        # import converted file to media pool
        time.sleep(2)
        mediaPool.ImportMedia(outputDir + outputClipName)
    else:
        print("Error running ffmpeg script")


runFFmpeg(buildFFmpegCommand())
