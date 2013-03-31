# Youtube caption to SRT
This is a script that allows you to download YouTube captions and convert them into SRT format.
This is just for my practice of parsing XML files using Python. 

## USAGE

* Go www.youtube.com and watch a movie.

* Copy the video URL.
 
* Run this script to show available caption language list.

        ./youtube2srt.py <video url>

* Run this script again with the index number of the caption language that you want to dump:

        ./youtube2srt.py <video url> <lang id> > script.srt
