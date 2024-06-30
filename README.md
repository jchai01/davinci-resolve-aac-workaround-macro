# What does it do?

Ability to convert a particular file with AAC codec to WAV codec (or other compatible formats) with a hotkey. The clip under the playhead position gets converted and imported back into the media pool automatically. This is made possible with the Davinci Resolve scripts API.

# Why

AAC codec isn't supported on Linux due to some licensing nonsense. Before using this, just be aware other solution exist such as:

- ffmpeg script to convert the entire directory to a compatible formats.
- "smart folders" with incron: https://passthroughpo.st/painless-linux-video-production-part-3-organization-and-workflow/#:~:text=Auto%2DTranscode%20Your%20Footage

I just don't think it's the best ultilization of disk space to convert every video as it duplicating the video portion. Extracting every audio file at once makes it hard to keep track which video and audio file goes together. Sometimes I don't need audio from all the clips too.

# Setup/installation

1. Activate Davinci Resolve scripts API, add required environment variables with `sudoedit /etc/profile`.
2.  add the following line at the end of the file:
```bash
export RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```
3. Copy the code in `convert.py` and place it in `/opt/resolve/Fusion/Scripts/Comp`
4. Set the variables in `convert.py` for your working directory, output directory and ffmpeg binary path. Don't forget the trailing `/` at the end for working and output directory.

# Usage

1. Add some clips into your timeline in Davinci Resolve.
2. Bring the playhead to the desired clip.
3. Open the terminal and run `python /opt/resolve/Fusion/Scripts/Comp/convert.sh` to ensure it is working.
4. You can also run the script under `workspaces > Scripts > Comp`, or set a hotkey.

# Notes
- Running external scripts is only available in studio version.
- Tested in Davinci Resolve Studio 19 Beta 3
- Davinci Resolve scripts API unofficial docs: https://deric.github.io/DaVinciResolve-API-Docs/

# Future
- Add checks to see if wav file exist. If exist, highlight/focus in media pool.
- Import and add the clip to timeline too.
