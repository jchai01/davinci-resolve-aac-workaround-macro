#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
import subprocess

# this is where ffmpeg looks for your videos
workingDir = "/home/user/videos/"

# where to store the output file, make sure the path exist
outputDir = "/home/user/temp/"

# location of your ffmpeg installation
ffmpeg = "/usr/bin/ffmpeg"

resolve = dvr_script.scriptapp("Resolve")
clipName = (
    resolve.GetProjectManager()
    .GetCurrentProject()
    .GetCurrentTimeline()
    .GetCurrentVideoItem()
    .GetName()
)
mediaPool = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()
outputClipName = clipName.replace(".mp4", ".wav")


def buildFFmpegCommand():
    commands_list = [
        ffmpeg,
        "-i",
        workingDir + clipName,
        outputDir + outputClipName,
        "-n",  # do not overwrite existing files
    ]
    return commands_list


def runFFmpeg(commands):
    if subprocess.run(commands).returncode == 0:
        print("ffmpeg script ran successfully")

        # import converted file to media pool
        mediaPool.ImportMedia(outputDir + outputClipName)
    else:
        print("Error running ffmpeg script")


runFFmpeg(buildFFmpegCommand())
