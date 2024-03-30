# Loopadrine - a looping audio solution
<p align="center">
    <a href="https://www.paypal.me/Struggleton/">
        <img src="https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg" width="155" alt="">
    </a>
    <a href="https://www.patreon.com/Struggleton">
        <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="150" alt="">
    </a>
 <a href="https://ko-fi.com/Struggleton">
        <img src="https://uploads-ssl.webflow.com/5c14e387dab576fe667689cf/61e11d430afb112ea33c3aa5_Button-1-p-500.png" width="235" alt="">
    </a>
</p>

**Loopadrine** is a script written in Python in order to automate generating looped audio playlists with minimal effort. *Loopadrine utilizes various modules in order to allow for the downloading, looping and conversion of YouTube videos/playlists to Nintendo's BRSTM's format, which can be inserted into a number of games.* 

The motivation for this project initially was speed up the process of adding new music to Super Smash Bros. Ultimate. I initially wrote this in the C# language, but switched to Python because of its ease of manipulating files and calling on other Python modules/CLIs. 

## Usage
Loopadrine is a script written in the Python language. In order to use it you will need the following dependencies installed on your machine:

 - [Python (64-bit)](https://www.python.org/downloads/)  >= 3.9
 - [PyMusicLooper](https://github.com/arkrow/PyMusicLooper) >= 3.0
	 - This includes PyMusicLooper's dependencies for full usage of its features so [FFMPEG](https://ffmpeg.org/download.html) as well.

Use the script by firstly adding a list of YouTube URLs to the `songs.txt` file. If this file does not exist, create it and add YouTube URLs to it (*one line per link.*)

Run the script using Python from the command line: `python Loopadrine.py`. There are flags that Loopadrine can accept for different operation modes:

    -r, --redo - Takes a BRSTM file(s) from the ~redo directory and its corresponding audio file from the ~processed directory and restarts the loop conversion process. 
    -s, --skip - Skips the loop generation portion of the conversion process.

Loopadrine (if the --skip/--redo flags aren't set) will then download and extract the audio from all of the links listed in the songs.txt file. Loopadrine will then ask which looping mode you'd like to use for the batch:

 - interactive (**inter**) - Use PyMusicLooper to generate a list of potential loop pairs. You can test each loop pair by entering the loop index you want to preview and adding 'p' at the end (e.g 0p.) Once a desirable loop pair is found, select it by entering the index and pressing enter.
 - automatic (**auto**) - PyMusicLooper will automatically choose the best discovered loop point based on its selection algorithm.

Once finished generating the looping file, the script will then convert the audio file to a BRSTM using the LoopingAudioConverter.

## Credits
Large thanks go out to the creators of these projects:

 - The [yt-dlp](https://github.com/yt-dlp)/[ytdl-org](https://github.com/ytdl-org) teams for creating the [yt-dlp](https://github.com/yt-dlp/yt-dlp) / [youtube-dl](https://github.com/ytdl-org/youtube-dl) projects
 - [Hazem "arkrow" Nabil](https://github.com/arkrow) for creating the [PyMusicLooper](https://github.com/arkrow/PyMusicLooper) project
- [Libertyernie](https://github.com/libertyernie/) and all of its contributors for creating the [LoopingAudioConverter](https://github.com/libertyernie/LoopingAudioConverter) project.

## Contributing
Please feel free to fork this project and submit a pull request under this repository. Any improvements/bugfixes/additions are welcome!