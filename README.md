# youtube_stream_capture
Record YouTube livestreams from start to finish, that includes the ability to rewind up to 12 hours regardless of whether the actual YouTube player allows it or not.

## Installation
Requires `python3`, `aria2c`, `ffmpeg` as well as `ffprobe` (usually bundled with ffmpeg) to be installed and on your systems' PATH.
Example using Ubuntu:
```
# Install FFmpeg
$ sudo apt-get install ffmpeg
$ sudo apt-get install aria2
# Install required python modules
$ python3 -m pip install requests
```

## Usage
Starting the livestream capture:
```
$ python3 youtube_stream_capture.py [Link to the livestream] [optional: start segment]
```

Merging all the segments after the stream has ended:
```
$ python3 merge_v1.py [Link to the livestream]
```
or 
```
$ python3 merge_v2.py [Link to the livestream]
```
Disclaimer: Despite all livestreams seemingly being of the same file type, some livestream segments refuse to merge properly using v1 or v2, with ffmpeg producing files that are seemingly thousands of hours in length. Use the other merge script in that case. I have yet to find the root cause of this issue.

The `cookie` field inside of `youtube_stream_capture.py` has intentionally been left empty. If you run into any 429 errors (Too many requests), filling in the cookie with one from the Chrome inspect tool can help.

## Support
Livestreams that have been running for multiple days (such as the 24/7 music livestreams) are not supported. youtube_stream_capture attempts to go back to the very first segment of a livestream by design. The first segments of those livestreams have long been deleted at this point, so the script just fails.

Support for VP9 livestreams has been added, but is highly experimental at this point and therefore commented out. Use at your own risk and don't bother opening up any issues if something breaks or the video goes out of sync. I don't want to deal with it.