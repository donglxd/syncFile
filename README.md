# syncFile
1. Introduction: 
This script uses the hash md5 method to divide into small blocks, compare the differences between the source folder and the target folder and synchronize copying. It only supports one-way synchronization from the source folder to the target folder and has written a sub-thread to judge the keyboard exit shortcut key Q to improve the speed of exiting. At the same time, it provides a breakpoint continuation function. After pressing q to exit, a dialog box will pop up to prompt the synchronization interruption position. In the same directory where this script is saved, a txt file that saves the file path at the breakpoint is written for easy recovery from the breakpoint next time. Because it compares and copies in small blocks, it can solve the problem of memory overflow of super-large files and cannot exit in time by pressing shortcut keys. This script is divided into manual and automatic setting of source and destination folder paths. Manually run the script directly and drag the source folder and target folder to the command line or terminal window; if the synchronized folder is the same every time, you can set it to automatic mode, remove the comments at the “automatic synchronization” at the bottom of the script and fill in the source destination folder (source: spath; destination: dpath), but you have to set a new breakpoint continuation path (xpath) or not use the breakpoint continuation function every time.

2.Installation:
python version: 3.9

```
pip3 install tkinter keyboard threading
```

3.User Video
