# Author: donglxd
# CSDN blog: https://blog.csdn.net/donglxd?spm=1010.2135.3001.5421
# GitHub: https://github.com/donglxd?tab=repositories

import os
import hashlib
import tkinter as tk
from tkinter import messagebox
import time
import sys
import keyboard
import threading

errmsg = ""
dfilename = ""
gotoBreak = False
stop_copying = False
finishexit = False

def chunked_file_Next_reader(file, block_size=1024 * 8):  # Read the compared file in segments
    while True:
        global gotoBreak
        if gotoBreak:
            break
        yield file.read(block_size)

def copy_file(src, dst):  # Copy files in segments, can be interrupted at any time (controlled by the stop_copying variable)
    global stop_copying
    with open(src, 'rb') as fs:
        with open(dst, 'wb') as fd:
            if stop_copying:
                print("stopped")
            while not stop_copying:
                buf = fs.read(1024)
                if not buf:
                    break
                fd.write(buf)
            fd.close()
        fs.close()

def md5_diff(sfile, dfile):  # Comparison function
    oldtime = time.time()
    count = 0
    scount = 0
    k = True
    with open(sfile, 'rb') as sf:
        with open(dfile, 'rb') as df:
            sdata = chunked_file_Next_reader(sf)
            fdata = chunked_file_Next_reader(df)
            while k:
                s_nxtdata = next(sdata)
                d_nxtdata = next(fdata)
                count += 1
                if s_nxtdata == b'':
                    if d_nxtdata == b'':
                        k = False
                    else:
                        count += 1
                        break
                else:
                    s_md5 = hashlib.md5(s_nxtdata).hexdigest()  # Compare the hash value of each segment in segments
                    d_md5 = hashlib.md5(d_nxtdata).hexdigest()
                    if s_md5 == d_md5:
                        scount += 1        
                    else:
                        # Determine that the files are different
                        sf.close()
                        df.close()
                        return 0
            if (count - 1) == scount:
                # Determine that the files are the same
                sf.close()
                df.close()
                return 1
            else:
                # Determine that the files are different
                sf.close()
                df.close()
                return 0

def check_keyborad():  # Sub-thread to determine exit operation (press q to exit)
    while True:
        if keyboard.is_pressed("q"):
            global errmsg
            global gotoBreak
            global stop_copying
            gotoBreak = True  # Set to exit comparison function
            stop_copying = True  # Set to exit copy function
            if errmsg == "":
                errmsg = dfilename + " interrupted at this point!"  # Set the prompt information for breakpoint continuation 
                print("error:" + errmsg)
            with open(sys.path[0] + "/breakpoint.txt", 'w') as log:  # Write the position of breakpoint continuation to "breakpoint.txt" in the same directory as this script 
                log.write(errmsg)
                log.close()
            messagebox.showinfo("Prompt", errmsg)  # Pop up a window with prompt information for breakpoint continuation 
            sys.exit(0)
        time.sleep(0.2)
        if finishexit:
            break

def copyFile(spath, dpath):  # Judgment copy main program 
    global dfilename
    for filename in os.listdir(spath):
        if gotoBreak:
            print("----------Interrupted-----------")
            break

        sfilename = spath + os.sep + filename
        dfilename = dpath + os.sep + filename
        dfilename = dfilename.replace('"', "")  # Replace the quotation marks in the dragged target directory string 
        sfilename = sfilename.replace('"', "")  # Replace the quotation marks in the dragged source directory string 

        if os.path.isdir(sfilename):
            if not os.path.exists(dfilename):
                os.mkdir(dfilename)
            copyFile(sfilename, dfilename)
        else:
            global k

            if dfilename == xpath and k == False:  # Determine whether the entered directory is empty and enter the breakpoint continuation program 
                k = True
                print("Breakpoint continuation start position:" + dfilename)
            if xpath == "" and k == False:  # Enter a brand new synchronization process 
                k = True
                print("New start:")
            if k == True:
                if os.path.exists(dfilename):
                    ret = md5_diff(sfilename, dfilename)
                    if ret == 1:
                        errmsg = dfilename + " interrupted at this point!"
                        #print('{} file already exists!'.format(dfilename))
                    else:
                        copy_file(sfilename, dfilename)
                        print('{} file has been updated!'.format(dfilename))
                else:
                    print('{0} copied to {1}'.format(sfilename, dfilename))
                    copy_file(sfilename, dfilename)

if __name__ == "__main__":

    # ---------Initialize the directory to be synchronized-----------
    # Source directory 
    spath = input("Please enter the source directory (such as: E:\work):")
    # spath = spath.replace('"', "")
    
    # Target directory 
    dpath = input("Please enter the target directory (such as: Z:\\):")
    # spath = spath.replace('"', "")
    
    # Assign a value to the xpath variable at the breakpoint continuation position or xpath = "" to start again 
    xpath = input("Please enter the path of the previously interrupted file (such as: X:\\1.txt), press Enter directly without using breakpoint continuation by default:")

    # --------------Automatic synchronization---------------
    # If the source directory/target directory does not change, you can set the following values and comment out the above input code.
    # spath = r"E:\work"
    # dpath = "Z:\\"
    # xpath = ""


    oldtime = time.time()
    k = False
    errmsg = ""

    # Run main program 
    t = threading.Thread(target=check_keyborad)  # Start an exit keyboard sub-thread 
    t.start()

    copyFile(spath, dpath)  # Judgment copy file main program 

    root = tk.Tk()
    root.withdraw()  # Hide the main window 
    
    newtime = time.time()
    if newtime - oldtime < 60:
        messagebox.showinfo("Prompt", "Folder synchronization successful! Total time: " + str(newtime - oldtime) + " seconds!")
    else:
        messagebox.showinfo("Prompt", "Folder synchronization successful! Total time: " + str((newtime - oldtime) / 60) + " minutes!")
    finishexit = True#Exit sub-thread flag bit

    t.join()#Wait for the sub-thread to end
