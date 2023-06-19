#作者:donglxd
#csdn博客:https://blog.csdn.net/donglxd?spm=1010.2135.3001.5421
#github:https://github.com/donglxd?tab=repositories

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

def chunked_file_Next_reader(file,block_size=1024 * 8):#分段读取比较的文件
    while True:
        global gotoBreak
        if gotoBreak:
            break
        yield file.read(block_size)

def copy_file(src, dst):#分段复制文件,可随时中断(stop_copying变量控制)
    global stop_copying
    with open(src, 'rb') as fs:
        with open(dst, 'wb') as fd:
            if stop_copying:
                print("stoped")
            while not stop_copying:
                buf = fs.read(1024)
                if not buf:
                    break
                fd.write(buf)
            fd.close()
        fs.close()

def md5_diff(sfile,dfile):#比较函数
    oldtime = time.time()
    count = 0
    scount = 0
    k = True
    with open(sfile,'rb') as sf:
        with open(dfile,'rb') as df:
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
                    s_md5 = hashlib.md5(s_nxtdata).hexdigest()#分段比较每段的hash值
                    d_md5 = hashlib.md5(d_nxtdata).hexdigest()
                    if s_md5 == d_md5:
                        scount += 1        
                    else:
                        #判断文件不一样
                        sf.close()
                        df.close()
                        return 0
            if (count - 1) == scount:
                #判断文件一样
                sf.close()
                df.close()
                return 1
            else:
                #判断文件不一样
                sf.close()
                df.close()
                return 0

def check_keyborad():#子线程判断退出操作(按q退出)
    while True:
        if keyboard.is_pressed("q"):
            global errmsg
            global gotoBreak
            global stop_copying
            gotoBreak = True#设置退出比较函数
            stop_copying = True#设置退出复制函数
            if errmsg == "":
                errmsg = dfilename + " 处中断!"#设置断点断续的提示信息
                print("error:" + errmsg)
            with open(sys.path[0] + "\断点断续.txt",'w') as log:#把断点断续的位置写入与此脚本相同目录的"断点断续.txt"
                log.write(errmsg)
                log.close
            messagebox.showinfo("提示",errmsg)#t弹出断点断续的提示信息窗口
            sys.exit(0)
        time.sleep(0.2)
        if finishexit:
            break



def copyFile(spath,dpath):#判断复制主程序
    global dfilename
    for filename in os.listdir(spath):
        if gotoBreak:
            print("----------已中断-----------")
            break

        sfilename = spath + os.sep + filename
        dfilename = dpath + os.sep + filename
        dfilename = dfilename.replace('"',"")#替换掉拖到目标目录字符串中的引号
        sfilename = sfilename.replace('"',"")#替换掉拖到源目录字符串中的引号
    
        if os.path.isdir(sfilename):
            if not os.path.exists(dfilename):
                os.mkdir(dfilename)
            copyFile(sfilename,dfilename)
        else:
            global k

            if dfilename == xpath and k == False:#判断输入的目录是否为空,进入断点断续程序
                k = True
                print("断点断续开始位置:" + dfilename)
            if xpath == "" and k == False:#进入全新的同步进程
                k = True
                print("新开始:")    
            if k == True:
                if os.path.exists(dfilename):
                    ret = md5_diff(sfilename,dfilename)
                    if ret == 1:
                        errmsg = dfilename + " 处中断!"
                        #print('{} 文件已存在!'.format(dfilename))
                    else:
                        copy_file(sfilename,dfilename)
                        print('{} 文件已更新!'.format(dfilename))
                else:
                    print('{0} 复制到 {1}'.format(sfilename,dfilename))
                    copy_file(sfilename,dfilename)

def start():#主程序
    oldtime = time.time()
    t = threading.Thread(target=check_keyborad)#开启一个退出键盘子线程
    t.start()
    copyFile(spath,dpath)#判断复制文件主程序
    root = tk.Tk()
    root.withdraw()#隐藏主窗体
    newtime = time.time()
    if newtime - oldtime < 60:
        messagebox.showinfo("提示","文件夹已同步成功! 共用时: " + str(newtime - oldtime) + "秒!")    
    else:
        messagebox.showinfo("提示","文件夹已同步成功! 共用时: " + str((newtime - oldtime)/60) + "分钟!")
    global finishexit
    finishexit = True
    t.join()

if __name__ == "__main__":

    #---------初始化需同步的目录-----------
    #源目录
    spath = input("请输入源目录(如:E:\工作开发):")
    #spath = spath.replace('"',"")
    
    #目标目录
    dpath = input("请输入目标目录(如:Z:\\):")
    #spath = spath.replace('"',"")
    
    #断点断续位置给xpath变量赋值或xpath = ""赋空值来重新开始
    xpath = input("请输入之前中断的文件路径(如:X:\\1.txt),默认不使用断点断续直接按回车:")

    #--------------自动同步---------------
    #如需源目录\目标目录不变可以设定下面的值,并把上面的input代码注释掉.
    #spath = r"E:\工作开发"
    #dpath = "Z:\\"
    #xpath = ""
    
    k = False
    errmsg = ""

    #运行主程序
    start()
