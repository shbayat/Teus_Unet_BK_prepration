# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:36:31 2019

@author: samadi
"""
import numpy as np
from keras.layers import Input,Dense,Lambda
from keras.models import Model, load_model,Sequential
from keras import backend as K
from keras.utils import plot_model
import scipy.io as spio
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.layers.merge import concatenate
import os
import matplotlib.pyplot as plt
from keras import optimizers
import random
import h5py
import pymysql

import imp


#foo = imp.load_source('data_selection', 'C:/Users/samadi/TeUS/PBG/TeUS/networks/Data_Selection.py')




def data_selection(Dataset_path="Z:/shared/images/ProstateVGH-2/Data/"):
    config = {
            'host': '137.82.56.208',
            'user': 'samareh',
            'password': 'samareh',
            'database' : "prostate"
            }
    
    cnx = pymysql.connect(**config)
    
    #read total number of cores
    cur = cnx.cursor()
#    sql_select_Query = "select count(id) FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND GolaraScore<3)"
#    cur.execute(sql_select_Query)
#    ids = cur.fetchall()
#    noOfcores=ids[0][0]

    #read Label for all cores
#    sql_select_Query = "select TrueLabel FROM core WHERE ((NeedleFrame<>'NULL' OR NeedleFrame=0) AND PatientId<70)"
#    cur.execute(sql_select_Query)
#    AllLabel=np.asarray(sum(cur.fetchall(),()))
#    
#     #read PatientID for all cores
#    sql_select_Query = "select PatientId FROM core WHERE (NeedleFrame<>'NULL' OR NeedleFrame=0) AND PatientId<70)"
#    cur.execute(sql_select_Query)
#    AllPatientId=np.asarray(sum(cur.fetchall(),()))
    
    
#    cancer_cid=np.where(AllLabel!=0)
#    cancer_pid=np.unique(AllPatientId[cancer_cid])
    #benign cores for train
    # benign_patients=set(np.unique(PatientId))-set(cancer_pid )-set([10,12,27,37]) # outliers are removed
#    benign_patients=set(np.unique(AllPatientId))-set(cancer_pid )-set([9,31]) #9th patient is special case
    
    sql_select_Query = "select id FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId<70)"
    cur.execute(sql_select_Query)
    ids = np.asarray(sum(cur.fetchall(), ()))
    # idcores=ids[0]
    
    #read PatientID for all cores
    sql_select_Query = "select PatientId FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId<70)"
    cur.execute(sql_select_Query)
    PatientId=np.asarray(sum(cur.fetchall(),()))
    
    #read Core ID for all cores
    sql_select_Query = "select CoreId FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId<70)"
    cur.execute(sql_select_Query)
    CoreId=np.asarray(sum(cur.fetchall(),()))
    
    #read Label for all cores
    sql_select_Query = "select TrueLabel FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId<70)"
    cur.execute(sql_select_Query)
    Label=np.asarray(sum(cur.fetchall(),()))

    # read Freq for all cores
    sql_select_Query = "select Freq FROM patient"
    cur.execute(sql_select_Query)
    RF_freq = np.asarray(sum(cur.fetchall(), ()))

    #read involvement (percentage of cancerous tissue) for all cores
#    sql_select_Query = "select Involvement FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND GolaraScore<3)"
#    cur.execute(sql_select_Query)
#    Involvement=np.asarray(sum(cur.fetchall(),()))
#
#    sql_select_Query = "select TumorInCoreLength FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND GolaraScore<3)"
#    cur.execute(sql_select_Query)
#    TumorLength=np.asarray(sum(cur.fetchall(),()))

    sql_select_Query = "select CalculatedInvolvement FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId<70)"
    cur.execute(sql_select_Query)
    Inv = np.asarray(sum(cur.fetchall(), ()))

    sql_select_Query = "select PrimarySecondary FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId<70)"
    cur.execute(sql_select_Query)
    GS=np.asarray(sum(cur.fetchall(),()))
    
    
    #train Cancer patients=[3, 6, 8, 11, 16, 20, 22, 23, 28, 38, 44] phase1
    train_cancer=[]
    train_cancer_patients = [3,5,6,7, 8, 11, 15, 16, 18, 20, 26, 28, 38,41, 44, 45, 52, 53, 57, 58, 59, 61,62, 63, 64]
    for i in train_cancer_patients:
      train_cancer.append(np.where(np.logical_and(PatientId==i,Label==1)))
    train_cancer=np.concatenate(train_cancer,axis=1)

    #    train_cancer = np.delete(train_cancer[0], np.where(train_cancer[0] == 75))
#    train_cancer = np.delete(train_cancer, np.where(train_cancer == 71))
    

    # ind_P8 = np.where(np.logical_or(ids==72,ids==76)) #to keep data balance
    # train_cancer = set(np.unique(train_cancer)) - set(np.unique(ind_P8))

    data_train_cancer=[]
    GS_train = GS[list(train_cancer[0])]
    inv_train = np.asarray(Inv[list(train_cancer[0])],dtype=float)
    

    #read data from files 
    for i in train_cancer[0]:
        folderp=Dataset_path+'Patient'+str(PatientId[i])+ '/'
        subfolders = os.listdir(folderp)
        ROI_Path = folderp + subfolders[0]+'/BMode/ROI_Data/OutProstate/RF_ROI_Data_'+str(CoreId[i]).zfill(2)+'.mat'
        data=spio.loadmat(ROI_Path)
        data_train_cancer.append(data["RFROI"]["data"][0][0])
        
#    mm=np.mean(data_train_cancer[0],axis=0)
#    plt.plot(np.transpose(data_train_cancer[0]))
#    plt.show()
    #test Cancer patients=[5,7,18,19]
    test_cancer=[]
    test_cancer_patients=[19,22,23,42]
    for i in test_cancer_patients:
      test_cancer.append(np.where(np.logical_and(PatientId==i,Label==1)))
    test_cancer=np.concatenate(test_cancer,axis=1)
      
    GS_test_temp = GS[test_cancer[0]]
    
    test_cancer = np.delete(test_cancer[0], np.where(GS_test_temp == '5+4'))
    GS_test = GS[test_cancer]
    inv_test = np.asarray(Inv[test_cancer], dtype=float)
    
    data_test_cancer=[]
    #read data from files 
    for i in test_cancer:
        folderp=Dataset_path+'Patient'+str(PatientId[i])+ '/'
        subfolders = os.listdir(folderp)
        ROI_Path = folderp + subfolders[0]+'/BMode/ROI_Data/OutProstate/RF_ROI_Data_'+str(CoreId[i]).zfill(2)+'.mat'
        data=spio.loadmat(ROI_Path)
        data_test_cancer.append(data["RFROI"]["data"][0][0])
    
    #find benign cores from all benign patients

    random.seed(4)
#    benign_patients_train=random.sample(benign_patients,15)# used to be 10 paitents
    benign_patients_train=[43,27,60,2,48,4,37,65,14,24,39,47,46]
    benign_cores_train=[]
    for i in benign_patients_train:
        benign_cores_train.append(np.where(PatientId[:]==i))
    benign_cores_train=np.concatenate(benign_cores_train,axis=1)
    bcores_train=set(benign_cores_train[0])-set([91,112,138,221,224,226,235,272,336])
    # bcores_train1 = set(benign_cores_train[0]) #to be checked
    random.seed(7)
    #benign_train_cid=random.sample(bcores_train,int(len(train_cancer)/2))
    benign_train_cid=random.sample(bcores_train,47)

    print(benign_patients_train)
    print(benign_train_cid)

    data_train_benign=[]
    #read data from files 
    for i in benign_train_cid:
        folderp=Dataset_path+'Patient'+str(PatientId[i])+ '/'
        subfolders = os.listdir(folderp)
        ROI_Path = folderp + subfolders[0]+'/BMode/ROI_Data/OutProstate/RF_ROI_Data_'+str(CoreId[i]).zfill(2)+'.mat'
        data=spio.loadmat(ROI_Path)
        data_train_benign.append(data["RFROI"]["data"][0][0])
        
    #benign cores for train
#    benign_patients_test=benign_patients-set(benign_patients_train)
    benign_patients_test=[21,25,10,30,12]
    benign_cores_test=[]
    for i in benign_patients_test:
        benign_cores_test.append(np.where(PatientId[:]==i))
    benign_cores_test=np.concatenate(benign_cores_test,axis=1)
    
    random.seed(8)
    benign_test_cid=random.sample(set(benign_cores_test[0]),14)

    print(benign_patients_test)
    print(benign_test_cid)

    data_test_benign=[]
    #read data from files 
    for i in benign_test_cid:
        folderp=Dataset_path+'Patient'+str(PatientId[i])+ '/'
        subfolders = os.listdir(folderp)
        ROI_Path = folderp + subfolders[0]+'/BMode/ROI_Data/OutProstate/RF_ROI_Data_'+str(CoreId[i]).zfill(2)+'.mat'
        data=spio.loadmat(ROI_Path)
        data_test_benign.append(data["RFROI"]["data"][0][0])
      
    #Build train data
    data_train=data_train_cancer+data_train_benign
    label_train=np.zeros(len(data_train))
    ind3=np.where(GS_train!='3+3')
    label_train[ind3]=1
    ind4=np.where(GS_train=='3+3')
    label_train[ind4]=2
   
    #Build test data
    data_test=data_test_cancer+data_test_benign
    
    label_test=np.zeros(len(data_test))
    ind3=np.where(GS_test!='3+3')
    label_test[ind3]=1
    ind4=np.where(GS_test=='3+3')
    label_test[ind4]=2
    
    # Core id for train and test
    #Train
    idcore_train=np.concatenate((ids[train_cancer[0]],ids[benign_train_cid]))
    idcore_test=np.concatenate((ids[test_cancer],ids[benign_test_cid]))
    
    PatientId_train=np.concatenate((PatientId[train_cancer[0]],PatientId[benign_train_cid]))
    PatientId_test=np.concatenate((PatientId[test_cancer],PatientId[benign_test_cid]))

    return data_train,label_train, GS_train,inv_train,idcore_train, PatientId_train,data_test,label_test,GS_test, inv_test,idcore_test,PatientId_test, RF_freq



if __name__ == "__main__":

   
    # Create save directory if not exists

        
    Balance=True
    augm=True
    Multi=False

    # Load data
    data_dir="Z:/shared/images/ProstateVGH-2/Data/"
    
    data_train,label_train, GS_train,inv_train,idcore_train, PatientId_train,data_test,label_test,GS_test, inv_test,idcore_test,PatientId_test, RF_freq = data_selection(Dataset_path=data_dir)
    if ~Multi:
        indx_4=np.where(label_train==1)
        indx_B=np.where(label_train==0)
        
        indx=np.append(indx_4[0],indx_B[0])
        data_train_4B=np.take(data_train,indx)
        label_train_4B=label_train[indx]
        GS_train_4=GS_train[indx_4]
        inv_train_4=inv_train[indx_4]
        idcore_train_4B=idcore_train[indx]
        PatientId_train_4B=PatientId_train[indx]
        
        indx_4=np.where(label_test==1)
        indx_B=np.where(label_test==0)
        
        indx=np.append(indx_4[0],indx_B[0])
        data_test_4B=np.take(data_test,indx)
        label_test_4B=label_test[indx]
        GS_test_4=GS_test[indx_4]
        inv_test_4=inv_test[indx_4]
        idcore_test_4B=idcore_test[indx]
        PatientId_test_4B=PatientId_test[indx]

        spio.savemat(data_dir+'Dataset/'+'BK_RF_Train_Test_IPCAIRev.mat',{'data_train':data_train_4B,'label_train':label_train_4B,'GS_train':GS_train_4,'inv_train':inv_train_4,'idcore_train':idcore_train_4B,'PatientID_Train':PatientId_train_4B,
                                                                         'data_test':data_test_4B,'label_test':label_test_4B,'GS_test':GS_test_4, 'inv_test':inv_test_4,'idcore_test':idcore_test_4B,'PatientID_Test':PatientId_test_4B,
                                                                         'RF_freq':RF_freq})

#    spio.savemat(data_dir+'Dataset/'+'BK_RF_Train_Test_IPCAIRev.mat',{'data_train':data_train,'label_train':label_train,'GS_train':GS_train,'inv_train':inv_train,'idcore_train':idcore_train, 'PatientID_Train':PatientId_train,
#                                                                         'data_test':data_test,'label_test':label_test,'GS_test':GS_test, 'inv_test':inv_test,'idcore_test':idcore_test, 'PatientID_Test':PatientId_test,
#                                                                         'RF_freq':RF_freq})
           