#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:43:09 2020

@author: sharareh
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
from sklearn.metrics import roc_auc_score,accuracy_score
from datetime import datetime
import scipy.io as spio
import hdf5storage

# Keras
from keras.models import Model
from keras.layers import Input, Layer, Dropout, merge, multiply, Conv1D, BatchNormalization, Activation, Dense, Reshape, UpSampling2D, Conv2DTranspose, GlobalAveragePooling1D, Softmax
from keras.losses import kullback_leibler_divergence
import keras.backend as K
from keras.utils.vis_utils import plot_model
from keras.optimizers import SGD, Adam
from keras.regularizers import l2
from keras.layers import Lambda

# ### For plotting model
# import pydot as pyd
# #from IPython.display import SVG
# from keras.utils.vis_utils import model_to_dot
# from keras.utils import plot_model
# #Visualize Model

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

val1=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_val_1_P2_15___20200515-081151.mat') 
val2=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_val_2_P16_30___20200515-083413.mat') 
val3=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_val_3_P31_50___20200515-084635.mat') 
val4=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_val_4_P51_70___20200515-094734.mat') 
val5=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_val_5_P71_90___20200515-122437.mat') 

train1=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_train_1_P2_15___20200515-081151.mat') 
train2=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_train_2_P16_30___20200515-083413.mat') 

train3=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_train_3_P31_50___20200515-084635.mat') 
train4=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_train_4_P51_70___20200515-094734.mat') 
train5=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_train_5_P71_90___20200515-122437.mat') 
#train5_2=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/data_train5.mat',variable_names=['data_train']) 
#train5=hdf5storage.loadmat('C:/Users/Sharareh/Desktop/data/BK_DS_FFT_train_5_P71_90___20200515-122437.mat')
#                           ,variable_names=['data_train','GS_train','Label_train','PatientId_train'
#                                           'RF_freq']) 

### Train
data_train1=train1["data_train"]
data_train2=train2["data_train"]
data_train3=train3["data_train"]
data_train4=train4["data_train"]
data_train5=train5["data_train"]

label_train1=train1["label_train"]
label_train2=train2["label_train"]
label_train3=train3["label_train"]
label_train4=train4["label_train"]
label_train5=train5["label_train"]

GS_train1=train1["GS_train"]
GS_train2=train2["GS_train"]
GS_train3=train3["GS_train"]
GS_train4=train4["GS_train"]
GS_train5=train5["GS_train"]

GS_train=GS_train1+GS_train2+GS_train3+GS_train4+GS_train5
data_train=data_train1+data_train2+data_train3+data_train4+data_train5
label_train=np.concatenate((label_train1, label_train2,label_train3, label_train4,label_train5), axis=None)
#np.savez('Data_train.npz', **{'data_train':data_train[0:20]})


### Val
data_val1=val1["data_val"]
data_val2=val2["data_val"]
data_val3=val3["data_val"]
data_val4=val4["data_val"]
data_val5=val5["data_val"]

label_val1=val1["label_val"]
label_val2=val2["label_val"]
label_val3=val3["label_val"]
label_val4=val4["label_val"]
label_val5=val5["label_val"]

GS_val1=val1["GS_val"]
GS_val2=val2["GS_val"]
GS_val3=val3["GS_val"]
GS_val4=val4["GS_val"]
GS_val5=val5["GS_val"]

GS_val=GS_val1+GS_val2+GS_val3+GS_val4+GS_val5
data_val=data_val1+data_val2+data_val3+data_val4+data_val5
label_val=np.concatenate((label_val1, label_val2,label_val3, label_val4,label_val5), axis=None)

#np.savez('Data_val.npz', **{'GS_val': GS_val,'data_val':data_val, 'label_val':label_val})

#np.savez('Data.npz', **{'GS_train': GS_train,'data_train':data_train, 'label_train':label_train,
#        'GS_val': GS_val,'data_val':data_val, 'label_val':label_val})