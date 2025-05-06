# What does it do?

It transcodes specific footages on the fly while remaining in Resolve. It extracts audio in WAV codec from a particular footage with AAC codec, the .wav file is then imported into the media pool and inserted into the timeline at the playhead position, all with just a hotkey. The clip that is under the playhead gets converted.

# Why?

Somehow AAC codec isn't supported on Linux, even with the Studio version. Before using this, be aware that other solution exist such as:

- FFMPEG scripts to convert the entire directory to a compatible formats.
- "smart folders" with incron: https://passthroughpo.st/painless-linux-video-production-part-3-organization-and-workflow/#:~:text=Auto%2DTranscode%20Your%20Footage

This script is useful for dealing with footages coming from smartphones as they are usually recorded in a mp4 container with H264/AAC codec. I don't think it's the best ultilization of disk space to convert every video as it duplicates the video portion, extracting every audio file at once makes it hard to keep track which video and audio file goes together too. Most of the time, I don't need the audio from all the clips.

# Setup/installation

1. Activate Davinci Resolve scripts API, add required environment variables with `sudoedit /etc/profile`. Add the following line at the end of the file:

```bash
export RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

2. The code in `convert.py` needs to be placed in `/opt/resolve/Fusion/Scripts/Comp`, it can be done using symlinks:

```bash
git clone https://github.com/jchai01/davinci-resolve-aac-workaround-macro.git
cd davinci-resolve-aac-workaround-macro
sudo ln -sf $(pwd)/convert.py /opt/resolve/Fusion/Scripts/Comp/
```

3. Set variables in `convert.py` script if applicable. Default output directory: `~/temp`, default ffmpeg binary path:`/usr/bin/ffmpeg`. Don't forget the trailing `/` at the end for the output directory.

# Usage

1. Add some clips into your timeline in Davinci Resolve.
2. Bring the playhead to the desired clip.
3. Open the terminal and run `python /opt/resolve/Fusion/Scripts/Comp/convert.sh` to ensure it is working.
4. You can also run the script under `workspaces > Scripts > Comp`, or set a hotkey (mine is `ctrl+h`).

# Notes

- Running external scripts is only available in studio version.
- Tested in Davinci Resolve Studio 19 Beta 3
- Davinci Resolve scripts API unofficial docs: https://deric.github.io/DaVinciResolve-API-Docs/

# Known Issues

- Hotkey set in Davinci keyboard shortcut page sometimes does not work during first startup. Run the script once under `workspaces > Scripts > Comp` and hotkey works subsequently, not sure why.

# More Resources

https://jchai01.github.io/posts/davinci-comprehensive-guide-linux/
