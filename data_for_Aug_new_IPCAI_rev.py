# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:07:18 2020

@author: Sharareh
"""
import os
import csv
import argparse
from time import time
import numpy as np
import sys
import matplotlib.pyplot as plt
import xlwt
import random
from random import shuffle
from datetime import datetime
import scipy.io as spio



data_aug_old=spio.loadmat('Z:\shared\images\ProstateVGH-2\Data\Dataset\Synthetic\combined.mat');
data_new=spio.loadmat('Z:\shared\images\ProstateVGH-2\Data\Dataset\BK_RF_Train_Test_IPCAIRev.mat');


data_train=np.concatenate((data_new["data_train"][0],data_aug_old["data_train"][0][94:188]))
                     

label_train=np.concatenate((data_new["label_train"][0],data_aug_old["label_train"][0][94:188]))


#inv_train=np.concatenate((data_new["inv_train"],0*data_new["inv_train"],data_aug_old["inv_train"][0][94:141],data_aug_old["inv_train"][0][142:188]))

idcore_train=data_new["idcore_train"][0]
GS_train=data_new["GS_train"]

PatientId_train=data_new["PatientID_Train"][0]
data_test=data_new["data_test"][0]
label_test=data_new["label_test"][0]
GS_test=data_new["GS_test"]
inv_test=data_new["inv_test"]
idcore_test=data_new["idcore_test"][0]
PatientId_test=data_new["PatientID_Test"][0]
RF_freq=data_new["RF_freq"][0]

data_dir="Z:/shared/images/ProstateVGH-2/Data/"
#spio.savemat('combined_new_IPCAIRev.mat',{'data_train':data_train,'label_train':label_train,'GS_train':GS_train,'idcore_train':idcore_train,
                                                                       'PatientID_Train':PatientId_train,'data_test':data_test,'label_test':label_test,'GS_test':GS_test, 'inv_test':inv_test,
                                                                       'idcore_test':idcore_test,'PatientID_Test':PatientId_test,'RF_freq':RF_freq})