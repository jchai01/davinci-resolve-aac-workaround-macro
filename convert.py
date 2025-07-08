#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
import subprocess
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
        break
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
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()


def timecode_to_frames(timecode, fps):
    """Convert timecode string to frame count"""
    hours, minutes, seconds, frames = map(int, timecode.split(":"))
    return ((hours * 3600) + (minutes * 60) + seconds) * fps + frames


def add_audio_clip_at_playhead(audio_clip_name, audio_track=1):
    # Get project framerate
    fps = float(project.GetSetting("timelineFrameRate"))

    # Find the audio clip in media pool
    root_folder = mediaPool.GetRootFolder()
    for clip in root_folder.GetClipList():
        if clip.GetClipProperty("Clip Name") == audio_clip_name:

            # Get current playhead position
            playhead_timecode = timeline.GetCurrentTimecode()
            playhead_frames = timecode_to_frames(playhead_timecode, fps)
            duration = clip.GetClipProperty("Duration")

            # Add to audio track (negative track numbers for audio)
            mediaPool.AppendToTimeline(
                [
                    {
                        "mediaPoolItem": clip,
                        "startFrame": 0,  # Start from beginning of clip
                        "endFrame": duration,
                        "trackIndex": -abs(audio_track),
                        "recordFrame": playhead_frames,  # Insert at playhead
                        # "recordFrame": playhead_timecode,  # works for all timeline settings/fps, but does not insert accurately at playhead
                    }
                ]
            )

            # set playhead back to where it was
            timeline.SetCurrentTimecode(playhead_timecode)

            print(
                f"Added audio clip '{audio_clip_name}' to track A{audio_track} at {playhead_timecode}"
            )
            return True

    print(f"Audio clip '{audio_clip_name}' not found in Media Pool")
    return False


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
    else:
        print("Error running ffmpeg script")


# if converted audio file already exist in outputDir, import it
for i in os.listdir(outputDir):
    if outputClipName == i:
        mediaPool.ImportMedia(outputDir + outputClipName)
        add_audio_clip_at_playhead(outputClipName, audio_track=1)
        exit(0)

runFFmpeg(buildFFmpegCommand())
mediaPool.ImportMedia(outputDir + outputClipName)
add_audio_clip_at_playhead(outputClipName, audio_track=1)
