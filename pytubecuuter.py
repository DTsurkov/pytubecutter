import sys
import pytube
import csv
import os
from moviepy.editor import *

videoList = "video.list"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#GET DATA FROM LIST:
toDownload = []
with open(videoList, newline='') as csvfile:
    lineReader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
    for row in lineReader:
        toDownload.append(row)

#Download all movies:
#for toD in toDownload:
for i in range(len(toDownload)):
    print(bcolors.OKBLUE + "Downloading video: "+ toDownload[i][0] + bcolors.ENDC)
    try:
    	yt = pytube.YouTube(toDownload[i][0])
    except:
        print(bcolors.FAIL + "Can't connect to YouTube link: " + toDownload[i][0] + bcolors.ENDC)
    video = yt.streams.get_highest_resolution()
    try:
    	out_file = video.download()
    except:
    	print(bcolors.FAIL + "Can't download video: " + toDownload[i][0] + bcolors.ENDC)
    os.rename(out_file, video.default_filename)
    toDownload[i].append(video.default_filename)

def getSeconds(string):
    h, m, s = string.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

#Cut movies:
for i in range(len(toDownload)):
    startTime = getSeconds(toDownload[i][1])
    endTime = getSeconds(toDownload[i][2])
    inputFile = toDownload[i][3]
    outFile = "Cut_" + toDownload[i][3]
    print (bcolors.OKBLUE + "Trim from " + str(startTime) + "s to " + str(endTime) + "s" + bcolors.ENDC)
    clip = VideoFileClip(inputFile)
    newClip = clip.subclip(startTime, endTime)
    newClip.write_videofile(outFile, audio_codec="aac")
    newClip.close()
    clip.close()
