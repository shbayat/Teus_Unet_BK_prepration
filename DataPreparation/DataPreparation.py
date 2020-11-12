# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:25:42 2019

@author: samadi
"""

from DICOM2DBS import dicom2dbs
from NDLTip import RFROISave
from SaveVideo import SaveVideo
import pymysql
#import matlab.engine

#eng = matlab.engine.start_matlab()

Patient=129

#dicom2dbs(Patient)
#RFWidth,RFHeight=eng.SaveRF(Patient,nargout=2)
#RFWidth=RFWidth/2
#
#config = {'host': '137.82.56.208','user': 'samareh','password': 'samareh','database' : "prostate"}
#
#cnx = pymysql.connect(**config)
#
#cur = cnx.cursor()
#sqlquary = "UPDATE patient SET RFWidth = "+str(RFWidth)+", RFHight = "+ str(RFHeight)+" WHERE ID = " + str(Patient)
#cur.execute(sqlquary)
#cnx.commit()
#cnx.close()
#
#eng.Whole_Prostate_Selection(Patient,nargout=0)
##SaveVideo(Patient)
RFROISave(Patient)
