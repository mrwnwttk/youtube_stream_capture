#!/usr/bin/env python3

import os
import sys
import time
import shutil
import subprocess

if len(sys.argv) < 2:
	print("")

video_thing = sys.argv[1].split('?v=')
print(video_thing)
video_thing = video_thing[1]

x = os.listdir("segments_{}".format(video_thing))
segments = int((len(x) / 2) - 1)

def v1():
	global segments
	global video_thing
	with open("list_{}_audio.txt".format(video_thing), "w") as f:
		for i in range(0, segments + 1):
			f.write("file 'segments_{}/{}_{}_audio.ts'\n".format(video_thing, i, video_thing))

	os.system("ffmpeg -hide_banner -y -f concat -safe 0 -i list_{}_audio.txt -c:a copy \"{}_audio_v1_ffmpeg.m4a\"".format(video_thing, video_thing))

	with open("list_{}_video.txt".format(video_thing), "w") as f:
		for i in range(0, segments + 1):
			f.write("file 'segments_{}/{}_{}_video.ts'\n".format(video_thing, i, video_thing))	

	os.system("ffmpeg -hide_banner -y -f concat -safe 0 -i list_{}_video.txt -c:v copy \"{}_video_v1_ffmpeg.mp4\"".format(video_thing, video_thing))

	os.system("ffmpeg -hide_banner -y -i \"{}_video_v1_ffmpeg.mp4\" -i \"{}_audio_v1_ffmpeg.m4a\" -c:a copy -c:v copy \"{}.mp4\"".format(video_thing, video_thing, video_thing))

	os.remove("list_{}_audio.txt".format(video_thing))
	os.remove("list_{}_video.txt".format(video_thing))
	os.remove("{}_video_v1_ffmpeg.mp4".format(video_thing))
	os.remove("{}_audio_v1_ffmpeg.m4a".format(video_thing))

def v2():
	global segments
	global video_thing
	with open("concat_{}_audio.ts".format(video_thing),"wb") as f:
		for i in range(0,segments + 1):
			with open("segments_{}/{}_{}_audio.ts".format(video_thing, i, video_thing), "rb") as ff:
				shutil.copyfileobj(ff, f)

	os.system("ffmpeg -y -hide_banner -i concat_{}_audio.ts -c copy concat_{}_ffmpeg_audio.m4a".format(video_thing, video_thing))

	with open("concat_{}_video.ts".format(video_thing),"wb") as f:
		for i in range(0,segments + 1):
			with open("segments_{}/{}_{}_video.ts".format(video_thing, i, video_thing), "rb") as ff:
				shutil.copyfileobj(ff, f)

	os.system("ffmpeg -y -hide_banner -loglevel panic -i concat_{}_video.ts -c copy concat_{}_ffmpeg_video.mkv".format(video_thing, video_thing))
	os.system("ffmpeg -y -hide_banner -loglevel panic -i concat_{}_ffmpeg_video.mkv -i concat_{}_ffmpeg_audio.m4a -c copy {}.mkv".format(video_thing,video_thing,video_thing))

	# Delete leftover files
	os.remove("concat_{}_video.ts".format(video_thing))
	os.remove("concat_{}_audio.ts".format(video_thing))
	os.remove("concat_{}_ffmpeg_video.mkv".format(video_thing))
	os.remove("concat_{}_ffmpeg_audio.m4a".format(video_thing))

def v3():
	global segments
	global video_thing
	with open("list_{}_audio.txt".format(video_thing), "w") as f:
		for i in range(0, segments + 1):
			f.write("file 'segments_{}/{}_{}_audio.ts'\n".format(video_thing, i, video_thing))

	os.system("ffmpeg -hide_banner -y -f concat -safe 0 -i \"list_{}_audio.txt\" -c:a copy \"./{}_audio_v1_ffmpeg.m4a\"".format(video_thing, video_thing))

	with open("list_{}_video.txt".format(video_thing), "w") as f:
		for i in range(0, segments + 1):
			f.write("file 'segments_{}/{}_{}_video.ts'\n".format(video_thing, i, video_thing))	

	os.system("ffmpeg -hide_banner -y -f concat -safe 0 -i \"list_{}_video.txt\" -c:v copy \"./{}_video_v1_ffmpeg.mp4\"".format(video_thing, video_thing))

	os.system("ffmpeg -hide_banner -y -i \"{}_video_v1_ffmpeg.mp4\" -i \"{}_audio_v1_ffmpeg.m4a\" -c:a copy -c:v copy \"./{}.mp4\"".format(video_thing, video_thing, video_thing))

	os.remove("list_{}_audio.txt".format(video_thing))
	os.remove("list_{}_video.txt".format(video_thing))
	os.remove("{}_video_v1_ffmpeg.mp4".format(video_thing))
	os.remove("{}_audio_v1_ffmpeg.m4a".format(video_thing))

def v4():
	global segments
	global video_thing
	folder_suffix = sys.argv[1].split('?v=')
	folder_suffix = folder_suffix[1]

	if not os.path.isdir('segments_{}_audio'.format(folder_suffix)):
		print("Creating folder for audio: segments_{}_audio".format(folder_suffix))
		os.mkdir('segments_{}_audio'.format(folder_suffix))
	if os.path.isdir('segments_{}_audio'.format(folder_suffix)):
		print("Folder for audio already exists!")

	print("Creating new audio files...")
	for i in range(0, segments + 1):
		print("\033[K\r", "Progress - Audio: [{} / {}]".format(i + 1, segments + 1), "\r", end='')
		os.system("ffmpeg -y -hide_banner -loglevel warning -advanced_editlist 0 -map_metadata -1 -i segments_{}/{}_{}_audio.ts -c:a copy segments_{}_audio/{}_{}_audio.m4a".format(video_thing, i, video_thing, video_thing, i, video_thing))
	#p.wait()
	print("", end='') # For the last \r
	#os.system("killall -9 ffmpeg")

	print("Creating list of audio segments...")
	with open("list_{}_audio.txt".format(video_thing), "w") as f:
		for i in range(0, segments + 1):
			f.write("file 'segments_{}_audio/{}_{}_audio.m4a'\n".format(video_thing, i, video_thing))

	print("Merging audio segments into a single file...")
	os.system("ffmpeg -hide_banner -y -loglevel warning -f concat -safe 0 -i list_{}_audio.txt -c:a copy {}_audio_v1_ffmpeg.m4a".format(video_thing, video_thing))
	#p.wait()
	#os.system("killall -9 ffmpeg")

	print("Removing file: list_{}_audio.txt".format(video_thing))
	os.remove("list_{}_audio.txt".format(video_thing))

	if not os.path.isdir('segments_{}_video'.format(folder_suffix)):
		print("Creating folder for video: segments_{}_video".format(folder_suffix))
		os.mkdir('segments_{}_video'.format(folder_suffix))
	if os.path.isdir('segments_{}_video'.format(folder_suffix)):
		print("Folder for video already exists!")

	print("Creating new video files...")
	for i in range(0, segments + 1):
		print("\033[K\r", "ffmpeg - Video: [{} / {}]".format(i + 1, segments + 1), "\r", end='')
		os.system("ffmpeg -y -hide_banner -loglevel warning -y -i segments_{}/{}_{}_video.ts -c:v copy segments_{}_video/{}_{}_video.mkv".format(video_thing, i, video_thing, video_thing, i, video_thing))
	print("", end='') # For the last \r

	print("Creating list of video segments...")
	with open("list_{}_video.txt".format(video_thing), "w") as f:
		for i in range(0, segments + 1):
			f.write("file 'segments_{}_video/{}_{}_video.mkv'\n".format(video_thing, i, video_thing))

	print("Merging video segments into a single file...")
	os.system("ffmpeg -hide_banner -y -loglevel warning -f concat -safe 0 -i list_{}_video.txt -c:v copy {}_video_v1_ffmpeg.mkv".format(video_thing, video_thing))

	print("Removing file: list_{}_audio.txt".format(video_thing))
	os.remove("list_{}_video.txt".format(video_thing))

	print("Merging audio and video files...")
	os.system("ffmpeg -hide_banner -y -loglevel panic -i {}_video_v1_ffmpeg.mkv -i {}_audio_v1_ffmpeg.m4a -c:a copy -c:v copy {}.mp4".format(video_thing, video_thing, video_thing))

	print("Deleting leftover files...")
	os.remove("{}_video_v1_ffmpeg.mkv".format(video_thing))
	os.remove("{}_audio_v1_ffmpeg.m4a".format(video_thing))

x = os.popen("ffprobe -v quiet -hide_banner -show_streams segments_{}/0_{}_video.ts".format(video_thing, video_thing)).read().split("\n")
print(x)
for i in x:
	if 'codec_tag_string' in i:
		codec_tag_string = i.split("=")[1]
	if 'codec_name' in i:
		codec_name = i.split("=")[1]
	if 'r_frame_rate' in i:
		r_frame_rate = i.split("=")[1]
	if 'height=' in i:
		height = i.split("=")[1]

if codec_tag_string == "avc1":
	if r_frame_rate == "60/1":
		print("avc1 - 60fps - v2")
		v2()
	if r_frame_rate == "30/1":
		print("avc1 - 30fps - v3")
		v2()
elif codec_name == "vp9":
	print(f"vp9 - {height}p - v4")
	v4()
else:
	print(x)