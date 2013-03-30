# Youtube caption to SRT
This is a script that helps download YouTube caption files and convert them to SRT format.
This is just for my practice of parsing XML files using Python. 

##USAGE
* Go www.youtube.com and watch a movie.
* Copy the video URL.
* Run this script like below.
    ./youtube2srt.py <video url>
* Then you can see the available caption language list.
* Run this script again with the index number of caption language you want to dump.
    ./youtube2srt.py <video url> <lang id> > script.srt
