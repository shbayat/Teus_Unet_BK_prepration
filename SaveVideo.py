# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:12:57 2019

@author: samadi
"""

import cv2
import numpy as np
import pymysql
import glob
import os
from BMode import *
import subprocess




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Transfer ROI from BMode  to RF@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Extract Params From Database@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def SaveVideo(PatientNo):

    config = {
         'host': '137.82.56.208',
         'user': 'samareh',
         'password': 'samareh',
         'database' : "prostate"
    }
    
    cnx = pymysql.connect(**config)
    
    cur = cnx.cursor()
    
    sql_select_Query = "select Suspicious FROM patient WHERE ID="+str(PatientNo)
    cur.execute(sql_select_Query)
    Suspicious = cur.fetchall()
    print(Suspicious)
    print(PatientNo)
    
    folderp = 'Z:\\shared\\images\\ProstateVGH-2\\Data\\Patient' + str(PatientNo) + '\\'
    subfolders = os.listdir(folderp)
    Data_Path = folderp + subfolders[0]
    sql_select_Query = "select NumberOfCores FROM patient WHERE ID="+str(PatientNo)
    cur.execute(sql_select_Query)
    NCores = cur.fetchall()
    BM = BMode(Data_Path, NCores[0][0])
    BM.BM_Movie_Maker()
    if BM.NofCores == 8:
            CoreLabels = ["RB", "RML", "RMM", "RA", "LB", "LML", "LMM", "LA"]
    else:
            if BM.NofCores == 10:
                CoreLabels = ["RBL", "RBM", "RML", "RMM", "RA", "LBL", "LBM", "LML", "LMM", "LA"]
            else:
                CoreLabels = ["RBL", "RBM", "RML", "RMM", "RAL", "RAM", "LBL", "LBM", "LML", "LMM", "LAL", "LAM"]

    for i in range(BM.NofCores):
        b=BM.dir+"\BMode\movie\movie"+str(i)+".mp4"
        p = subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe",b])
        #User should detect the frame number with the needle
        print("Enter the frame number for core %d: "%i)
        text = input()
        needleframe = int(text)
        print("Enter the score for core %d. 1=excelent, 2=needle is not clear, 3=hand move" %i)
        text = input()
        score = int(text)
        print("Enter the Revert for core %d. Set 0 for needle on the right of image" %i)
        text = input()
        Revert = int(text)
        sqlquary = "INSERT INTO core(PatientId,CoreId,NeedleFrame,SamarScore,Revert,CoreName) VALUES ("+str(PatientNo)+","+str(i)+","+str(needleframe)+","+str(score)+","+str(Revert)+",\""+CoreLabels[i]+"\")"
#        sqlquary = "UPDATE core SET SamarScore = "+str(score)+", NeedleFrame = "+ str(needleframe)+", Revert = "+str(Revert)+" WHERE (PatientId = " + str(PatientNo) + " and CoreId =" +str(i) + " )"
        print(sqlquary)
        cur.execute(sqlquary)
        cnx.commit()
        
    
    cnx.close()

    BM.FreeMemory()

