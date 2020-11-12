# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:29:27 2020

@author: samadi
"""
from tkinter import *
from tkinter import ttk
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
import hdf5storage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from Patients import core
import re
from datetime import datetime

#foo = imp.load_source('data_selection', 'C:/Users/samadi/TeUS/PBG/TeUS/networks/Data_Selection.py')

#val_id = [5, 6, 18, 45, 37, 30, 12, 14, 24, 46, 52, 58, 79, 71]
#test_id=P91:110
#
#train_cancer=[7,57,59,42,64,38,66,3,26,8,11,19,22,23,80,81,82,85,22,89,90]
#Validaiton_cancer=[18,45,5,52,58,71,6]
####validaiton_b_c=5, 6, 18, 45, 37, 30, 12, 14, 24, 46, 52, 58, 79, 71]
#test_cancer=[91,93,94,96,100,101,106,107,109,110]

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

class FilterWin:
    def __init__(self,master):
#        tk.Tk.__init__(self)
        self.master=master
        self.filtered_GS=[]
        self.filtered_Inv=[]
        self.filtered_Pid=[]
        self.filtered_cid=[]
        self.TrainP=[]
        self.ValP=[]
        self.TestP=[]
        self.balance=0 # used to be 0, if 1=balanced
        self.save_CancerBenign=0 #0
        self.temp=[]
        self.benign_patients=[]
        self.RF_freq=[]
        self.allPids=[]
        self.CoreId=[]
        self.allCids=[]

        wind.geometry('560x200')
        FontSize=14
        self.frame = LabelFrame(master,text = 'Filter', font=("Arial", FontSize))
        self.frame.grid (row = 0, column = 0)
    
        Label (self.frame, text = 'Patient>=', font=("Arial", FontSize)).grid(row = 1, column = 0)
        self.minP = Entry (self.frame)
        self.minP.grid(row = 1, column = 1)
        
    
        Label (self.frame, text = 'Patient<=', font=("Arial", FontSize)).grid(row = 1, column = 2)
        self.maxP = Entry (self.frame)
        self.maxP.grid(row = 1, column = 3)
    
        Label(self.frame, text = 'Inv>', font=("Arial", FontSize)).grid (row = 2, column = 0)
        self.minInv = Entry(self.frame)
        self.minInv.grid(row = 2, column = 1)
    
        Label(self.frame, text = 'Inv<=', font=("Arial", FontSize)).grid (row = 2, column = 2)
        self.maxInv = Entry(self.frame)
        self.maxInv.grid(row = 2, column = 3)
        
        Label(self.frame, text = 'GS:', font=("Arial", FontSize)).grid (row = 3, column = 0)
        self.gs33 = IntVar()
        Checkbutton(self.frame, text="3+3", variable=self.gs33).grid(row=3, column = 1)
        self.gs34 = IntVar()
        Checkbutton(self.frame, text="3+4", variable=self.gs34).grid(row=3, column = 2)
        self.gs43 = IntVar()
        Checkbutton(self.frame, text="4+3", variable=self.gs43).grid(row=3, column = 3)
        self.gs44 = IntVar()
        Checkbutton(self.frame, text="4+4", variable=self.gs44).grid(row=3, column = 4)
        self.gs45 = IntVar()
        Checkbutton(self.frame, text="4+5", variable=self.gs45).grid(row=4, column = 0)
        self.gs54 = IntVar()
        Checkbutton(self.frame, text="5+4", variable=self.gs54).grid(row=4, column = 1)
        self.gs55 = IntVar()
        Checkbutton(self.frame, text="5+5", variable=self.gs55).grid(row=4, column = 2)
        self.gs35 = IntVar()
        Checkbutton(self.frame, text="3+5", variable=self.gs35).grid(row=4, column = 3)
        self.gs53 = IntVar()
        Checkbutton(self.frame, text="5+3", variable=self.gs53).grid(row=4, column = 4)
        
        
        ttk.Button (self.frame, text = 'Apply Filter', command = self.applyfilter).grid(row = 5, column = 0)
        ttk.Button (self.frame, text = 'Plot', command = self.plotinformation).grid(row = 5, column = 1)
        ttk.Button (self.frame, text = 'Plot Patients', command = self.plotPatients).grid(row = 5, column = 2)
        ttk.Button (self.frame, text = 'Patients', command = self.PartitionWin).grid(row = 5, column = 3)
        

    def applyfilter(self,Dataset_path="Z:/shared/images/ProstateVGH-2/Data/"):
        config = {
                'host': '137.82.56.208',
                'user': 'samareh',
                'password': 'samareh',
                'database' : "prostate"
                }
        gs=[self.gs33.get(),self.gs34.get(),self.gs35.get(),self.gs43.get(),self.gs44.get(),self.gs45.get(),self.gs53.get(),self.gs54.get(),self.gs55.get()]
        InvD=[float(self.minInv.get()),float(self.maxInv.get())]
        P_I=[self.minP.get(),self.maxP.get()]
        cnx = pymysql.connect(**config)
        cur = cnx.cursor()
                   
        sql_select_Query = "select id FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId>="+P_I[0]+" AND PatientId<="+P_I[1]+")"
        cur.execute(sql_select_Query)
        ids = np.asarray(sum(cur.fetchall(), ()))
        
        #read PatientID for all cores
        sql_select_Query = "select PatientId FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId>="+P_I[0]+" AND PatientId<="+P_I[1]+")"
        cur.execute(sql_select_Query)
        PatientId=np.asarray(sum(cur.fetchall(),()))
        
        #read Core ID for all cores
        sql_select_Query = "select CoreId FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId>="+P_I[0]+" AND PatientId<="+P_I[1]+")"
        cur.execute(sql_select_Query)
        CoreId=np.asarray(sum(cur.fetchall(),()))
        
        #read Label for all cores
        sql_select_Query = "select TrueLabel FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId>="+P_I[0]+" AND PatientId<="+P_I[1]+")"
        cur.execute(sql_select_Query)
        Label=np.asarray(sum(cur.fetchall(),()))

        cancer_cid=np.where(Label!=0)
        cancer_pid=np.unique(PatientId[cancer_cid])
        #benign cores for train
        benign_patients=set(np.unique(PatientId))-set(cancer_pid )-set([9,31]) #9th patient is special case
    
        # read Freq for all cores
        sql_select_Query = "select Freq FROM patient"
        cur.execute(sql_select_Query)
        RF_freq = np.asarray(sum(cur.fetchall(), ()))
    
        #read involvement (percentage of cancerous tissue) for all cores
        sql_select_Query = "select CalculatedInvolvement FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId>="+P_I[0]+" AND PatientId<="+P_I[1]+")"
        cur.execute(sql_select_Query)
        Inv = np.asarray(sum(cur.fetchall(), ()))
    
        sql_select_Query = "select PrimarySecondary FROM core WHERE (NeedleFrame>0 AND SamarScore<3 AND PatientId>="+P_I[0]+" AND PatientId<="+P_I[1]+")"
        cur.execute(sql_select_Query)
        GS=np.asarray(sum(cur.fetchall(),()))
        
        cnx.commit() 
        cnx.close()

        Inv=[float(Inv[i]) for i in  range(len(Inv))]
        Inv=np.array(Inv)
        #Build output information
        GS_Types=['3+3','3+4','3+5','4+3','4+4','4+5','5+3','5+4','5+5']
        for i in range(len(GS_Types)):
            if gs[i]==1:
                ind=np.where(GS==GS_Types[i])[0]
                self.filtered_GS.append(GS[ind])
                self.filtered_Inv.append(Inv[ind])
                self.filtered_Pid.append(PatientId[ind])
                self.filtered_cid.append(ids[ind])
        
        for i in range(len(self.filtered_Inv)):
            indx=np.where((self.filtered_Inv[i]>InvD[0]) & (self.filtered_Inv[i]<=InvD[1]))
            self.filtered_GS[i]=np.take(self.filtered_GS[i],indx)[0]
            self.filtered_Inv[i]=np.take(self.filtered_Inv[i],indx)[0]
            self.filtered_Pid[i]=np.take(self.filtered_Pid[i],indx)[0]
            self.filtered_cid[i]=np.take(self.filtered_cid[i],indx)[0]
            
        self.benign_patients=list(benign_patients)
        self.RF_freq=RF_freq
        self.allPids=PatientId
        self.CoreId=CoreId
        self.allCids=ids
        self.allLabel=Label
        
        
        

    def plotinformation(self):

        nofsets=len(self.filtered_Inv)
        fig2, ax2 = plt.subplots()
        ax2.set_title('Involvement')
        ax2.boxplot(self.filtered_Inv, notch=True)
        
        xt_l=np.tile(['   '],nofsets)
        for i in range(nofsets):
            xt_l[i]=self.filtered_GS[i][0]
        plt.xticks(np.arange(1,nofsets+1),xt_l)
        top = Toplevel(self.master)
        frame2 = LabelFrame(top, text="Involvemnet Thu GS")
        invplot = FigureCanvasTkAgg(fig2, top) 
        invplot.draw()
        invplot.get_tk_widget().pack()

        fig3, ax3 = plt.subplots()
        ax3.set_title('GS')
        
        GSCount=np.zeros((nofsets,1))
        xt_l=np.tile(['   '],nofsets)
        for i in range(nofsets):
            xt_l[i]=self.filtered_GS[i][0]
            GSCount[i,0]=len(self.filtered_GS[i])
        ax3.bar(np.arange(1,nofsets+1),np.concatenate(GSCount))
        plt.xticks(np.arange(1,nofsets+1),xt_l)

        top2 = Toplevel(self.master)
        frame3 = LabelFrame(top2, text="GS hidtogram")
        invplot = FigureCanvasTkAgg(fig3, top2) 
        invplot.draw()
        invplot.get_tk_widget().pack()

    def plotPatients(self):
#        dictGS={'3+3':0,'3+4':1,'3+5':2,'4+3':3,'4+4':4,'4+5':5,'5+3':6,'5+4':7,'5+5':8}
#        y=[dictGS[i] for i in np.concatenate(self.filtered_GS)]
#        plt.scatter(np.concatenate(self.filtered_Pid),y,s=np.concatenate(self.filtered_Inv)*100)
#        plt.show()
        ptnts=np.concatenate(self.filtered_Pid)
        patients=np.unique(ptnts);
        Invs=np.concatenate(self.filtered_Inv)*100
        gs=np.concatenate(self.filtered_GS)
        indx=[]
        maxc=0
        for ip in patients:
            temp=np.where(ptnts==ip)[0]
            indx.append(temp)            
            maxc=max(maxc,len(temp))


        inv=np.zeros((len(patients),maxc),dtype=float)
        label=[]

        for ip in range(len(patients)):
            indxip=indx[ip]
            inv[ip,:len(indxip)]=Invs[indxip]
            label.append(gs[indxip]);
            
        
            
        fig4, ax4 = plt.subplots()
        fig4.set_size_inches(18.5, 10.5)
        barbase = np.cumsum(np.concatenate((np.zeros((inv.shape[0],1)),inv[:,0:-1]),axis=1),1)
        
#        colors = plt.cm.BuPu(np.linspace(0.5, 1, len(patients)+1))
        theta = 2 * np.pi * np.random.rand(100)
        cmap=['r','g','b','c']
        for i in range(maxc):
            ax4.bar(np.arange(len(patients)),inv[:,i].tolist(),0.7,bottom=barbase[:,i],color= cmap[i%4 ])
        plt.xticks(np.arange(len(patients)), patients)
        plt.xlabel('Patinet No.')
        
        joblblpos = inv/2 + barbase
        for k1 in range(inv.shape[0]):
            for k2 in range(inv.shape[1]):
                plt.text(k1, joblblpos[k1,k2], label[k1][k2] if inv[k1,k2]!=0 else '')
        top3 = Toplevel(self.master)
        frame3 = LabelFrame(top3, text="GS hidtogram")
        invplot = FigureCanvasTkAgg(fig4, top3) 
        invplot.draw()
        invplot.get_tk_widget().pack()
        
    def PartitionWin(self):
        top4 = Toplevel(self.master)
        top4.geometry('720x220')
        FontSize=14
        self.frame1 = LabelFrame(top4,text = 'Prtition', font=("Arial", FontSize))
        self.frame1.grid (row = 0, column = 0)
    
        ptnts=np.concatenate(self.filtered_Pid)
        patients=np.unique(ptnts)

        Label (self.frame1, text = 'Train Patients', font=("Arial", FontSize)).grid(row = 1, column = 0)
        self.TrP = Entry (self.frame1,width=90)
        self.TrP.grid(row = 1, column = 1)
        
    
        Label (self.frame1, text = 'Test Patients', font=("Arial", FontSize)).grid(row = 3, column = 0)
        self.TeP = Entry (self.frame1,width=90)
        self.TeP.grid(row = 3, column = 1)
    
        Label(self.frame1, text = 'Validation Patients', font=("Arial", FontSize)).grid (row = 5, column = 0)
        self.VaP = Entry(self.frame1,width=90)
        self.VaP.grid(row = 5, column = 1)

        self.bal = IntVar()
        Checkbutton(self.frame1, text="Balance", variable=self.bal).grid(row=6, column = 0)
        self.save_CB = IntVar()
        Checkbutton(self.frame1, text="Save_BenignCancers", variable=self.save_CB).grid(row=6, column = 1)
        self.RFflag = IntVar()
        Checkbutton(self.frame1, text="RF", variable=self.RFflag).grid(row=7, column = 0)
        self.MeanFFTflag = IntVar()
        Checkbutton(self.frame1, text="MeanFFT", variable=self.MeanFFTflag).grid(row=7, column = 1)
        self.MeanFFTNoMeanflag = IntVar()
        Checkbutton(self.frame1, text="MeanFFTNoMean", variable=self.MeanFFTNoMeanflag).grid(row=8, column = 0)

        self.DSflag = IntVar()
        Checkbutton(self.frame1, text="DS_FFT", variable=self.DSflag).grid(row=8, column = 1)

        ttk.Button (self.frame1, text = 'Save', command = self.Save).grid(row = 9, column = 0)

    def selectBenign(self,BPids,Dataset_path,inside_dir,file_pre):
            BCids=[]
            for i in BPids:
                    folderp=Dataset_path+'Patient'+str(i)+ '/'
                    subfolders = os.listdir(folderp)
                    indx=np.where(self.allPids==i)[0]
                    coreid=self.CoreId[indx]
                    
                    for j in range(len(coreid)):
                        if self.allLabel[indx[j]]==0:
                            fname=folderp + subfolders[0]+inside_dir+file_pre+str(coreid[j]).zfill(2)+'.mat'
                            BCids.append(core(self.allCids[indx[j]],coreid[j],i,0,'-',0,fname))
            return BCids

    def selectCancer(self,CPids,Dataset_path,inside_dir,file_pre):
            CCids=[]
            for i in range(len(self.filtered_cid)): 
                for j in range(len(self.filtered_cid[i])):
                    if self.filtered_Pid[i][j] in CPids:
                        folderp=Dataset_path+'Patient'+str(self.filtered_Pid[i][j])+ '/'
                        subfolders = os.listdir(folderp)
                        coreid=self.CoreId[np.where(self.allCids==self.filtered_cid[i][j])][0]
                        fname=folderp + subfolders[0]+inside_dir+file_pre+str(coreid).zfill(2)+'.mat'
                        CCids.append(core(self.filtered_cid[i][j],coreid,self.filtered_Pid[i][j],1,self.filtered_GS[i][j],self.filtered_Inv[i][j],fname))
            return CCids

    def Save(self):
        ptnts=np.concatenate(self.filtered_Pid)
        patients=np.unique(ptnts)        
        CancerTrP_text=self.TrP.get()
        CancerTeP_text=self.TeP.get()
        CancerValP_text=self.VaP.get()
        self.balance=self.bal.get()
        self.save_CancerBenign=self.save_CB.get()
        self.RF=self.RFflag.get()
        self.MeanFFT=self.MeanFFTflag.get()
        self.MeanFFTNoMean=self.MeanFFTNoMeanflag.get()
        self.DS=self.DSflag.get()

              
        self.TrainCP = [int(i) for i in re.findall('\d+', CancerTrP_text)]
        self.TestCP = [int(i) for i in re.findall('\d+', CancerTeP_text)]
        self.ValCP = [int(i) for i in re.findall('\d+', CancerValP_text)]
        

        Dataset_path="Z:/shared/images/ProstateVGH-2/Data/"
        inside_dir='/BMode/ROI_Data/' #OutProstate/
        inside_dir_DS='/BMode/ROI_Data/Down_Sample/' #Downsample/
        Benign_Cids=[]
 

        if self.MeanFFTNoMean:
            file_pre='MeanRF_mean_removed_ROI_Data_'
        elif self.MeanFFT:
            file_pre='MeanRF_FFT_ROI_Data_'
        elif self.RF:
            file_pre='RF_ROI_Data_'
        elif self.DS:
            file_pre='masked_FFT_' 
            inside_dir=inside_dir_DS
                
        #Select Cancer Cores
        #Trian
        Train_CCids=self.selectCancer(self.TrainCP,Dataset_path,inside_dir,file_pre)

        #Test
        Test_CCids=self.selectCancer(self.TestCP,Dataset_path,inside_dir,file_pre)

        #Test
        Val_CCids=self.selectCancer(self.ValCP,Dataset_path,inside_dir,file_pre)

        #Select Benign Patients
        if self.balance:
            NoBTr=len(self.TrainCP)
            NoBTe=len(self.TestCP)
            NoBVa=len(self.ValCP)
        else:
            NoCTr=len(self.TrainCP)
            NoCTe=len(self.TestCP)
            NoCVa=len(self.ValCP)
            sumC=NoCTr+NoCTe+NoCVa
            NoBTr=int(np.floor(NoCTr*len(self.benign_patients)/sumC))
            NoBTe=int(np.floor(NoCTe*len(self.benign_patients)/sumC))
            NoBVa=len(self.benign_patients)-NoBTe-NoBTr#int(np.floor(NoCVa*len(self.benign_patients)/sumC))
                
#        Train_BPids,Test_BPids,Val_BPids=splitBenign(self.benign_patients,NoBTr,NoBTe,NoBVa)
#        Test_BPids=[37, 24, 30, 12, 14, 46, 79]
#        Train_BPids=remove_patients(self.benign_patients,Test_BPids)
#        Train_BPids=[4,70,69,76,25,65,29,13,50,21,27,68,39,74,40,43,48,55,47,72,51,87,2,10,60]
##        Val_BPids=[]
#        Val_BPids=[14,24,12,30,37,46,79]
#        Test_BPids=[92,93,95,96,98,99,101,103,104,105,108,109,110]
#        Train_BPids=[4,2,10,25,29,21,27] #Part 1 train
#        Train_BPids=[50,39,40] #Part 2 train
        Train_BPids=[68,69,72,74,76,77,70] #Part 3 train
        Val_BPids=[]
#        Val_BPids=[14,24,30,37] # part 1
#        Val_BPids=[46,61] # part 2
#        Test_BPids=[92,93,95,96,98,99,101,103,104,105,108,109,110]

#        ############for p111-125
        Test_BPids=[112,114,117,118,119,120,121,122,124,125]  
        #Select Benign Cores
        if self.save_CancerBenign:
            #Trian
            Train_BCids=self.selectBenign(Train_BPids+self.TrainCP,Dataset_path,inside_dir,file_pre)
            
            #Test
            Test_BCids=self.selectBenign(Test_BPids+self.TestCP,Dataset_path,inside_dir,file_pre)
    
            #Val
            Val_BCids=self.selectBenign(Val_BPids+self.ValCP,Dataset_path,inside_dir,file_pre)
        else:
            #Trian
            Train_BCids=self.selectBenign(Train_BPids,Dataset_path,inside_dir,file_pre)
            
            #Test
            Test_BCids=self.selectBenign(Test_BPids,Dataset_path,inside_dir,file_pre)
    
            #Test
            Val_BCids=self.selectBenign(Val_BPids,Dataset_path,inside_dir,file_pre)

        if self.balance:
            Train_BCids=random.sample(Train_BCids,len(Train_CCids))
            Test_BCids=random.sample(Test_BCids,len(Test_CCids))
            Val_BCids=random.sample(Val_BCids,len(Val_CCids))
            
        #load data
        #Train
#        train_set=[]
#        train_set.append(saveData(Train_CCids,self.RF))
#        train_set.append(saveData(Train_BCids,self.RF))
#
#        #Test
#        test_set=[]
#        test_set.append(saveData(Test_CCids,self.RF))
#        test_set.append(saveData(Test_BCids,self.RF))
#
#        #Validation
#        val_set=[]
#        val_set.append(saveData(Val_CCids,self.RF))
#        val_set.append(saveData(Val_BCids,self.RF))
        
        train_set=[]
        train_set.append(saveData(Train_CCids,self.DS))
        train_set.append(saveData(Train_BCids,self.DS))

        #Test
        test_set=[]
        test_set.append(saveData(Test_CCids,self.DS))
        test_set.append(saveData(Test_BCids,self.DS))

        #Validation
        val_set=[]
        val_set.append(saveData(Val_CCids,self.DS))
        val_set.append(saveData(Val_BCids,self.DS))
        
        if self.balance:
            s1='balance'
        else:
            s1=''

        if self.save_CancerBenign:
            s2='withCancerBenign'
        else:
            s2=''

        data_train=[]
        label_train=[]
        inv_train=[]
        GS_train=[]
        PatientId_train=[]
        idcore_train=[]
        for i in range(len(train_set)):
            for j in range(len(train_set[i])):
              data_train.append(train_set[i][j].data)
              label_train.append(train_set[i][j].Label)
              inv_train.append(train_set[i][j].Inv)
              GS_train.append(train_set[i][j].GS)
              PatientId_train.append(train_set[i][j].PNo)
              idcore_train.append(train_set[i][j].Cid)

        data_val=[]
        label_val=[]
        inv_val=[]
        GS_val=[]
        PatientId_val=[]
        idcore_val=[]
        for i in range(len(val_set)):
            for j in range(len(val_set[i])):
              data_val.append(val_set[i][j].data)
              label_val.append(val_set[i][j].Label)
              inv_val.append(val_set[i][j].Inv)
              GS_val.append(val_set[i][j].GS)
              PatientId_val.append(val_set[i][j].PNo)
              idcore_val.append(val_set[i][j].Cid)

        data_test=[]
        label_test=[]
        inv_test=[]
        GS_test=[]
        PatientId_test=[]
        idcore_test=[]
        for i in range(len(test_set)):
            for j in range(len(test_set[i])):
              data_test.append(test_set[i][j].data)
              label_test.append(test_set[i][j].Label)
              inv_test.append(test_set[i][j].Inv)
              GS_test.append(test_set[i][j].GS)
              PatientId_test.append(test_set[i][j].PNo)
              idcore_test.append(test_set[i][j].Cid)
            
        timestr = datetime.now().strftime("%Y%m%d-%H%M%S")

        if self.MeanFFTNoMean:
                    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_MeanFFTNoMean_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
                                        'data_train':data_train,'label_train':np.asarray(label_train,dtype=float),'inv_train':np.asarray(inv_train,dtype=float),'GS_train':GS_train,'PatientId_train':np.asarray(PatientId_train,dtype=int),'idcore_train':np.asarray(idcore_train,dtype=int),
                                        'data_test':data_test,'label_test':np.asarray(label_test,dtype=float),'inv_test':np.asarray(inv_test,dtype=float),'GS_test':GS_test,'PatientId_test':np.asarray(PatientId_test,dtype=int),'idcore_test':np.asarray(idcore_test,dtype=int),
                                        'data_val':data_val,'label_val':np.asarray(label_val,dtype=float),'inv_val':np.asarray(inv_val,dtype=float),'GS_val':GS_val,'PatientId_val':np.asarray(PatientId_val,dtype=int),'idcore_val':np.asarray(idcore_val,dtype=int),
                                        'RF_freq':self.RF_freq})
                    print('Data is saved at:Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_MeanFFTNoMean_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr))
        elif self.MeanFFT:
                    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_MeanFFT_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
                                        'data_train':data_train,'label_train':np.asarray(label_train,dtype=float),'inv_train':np.asarray(inv_train,dtype=float),'GS_train':GS_train,'PatientId_train':np.asarray(PatientId_train,dtype=int),'idcore_train':np.asarray(idcore_train,dtype=int),
                                        'data_test':data_test,'label_test':np.asarray(label_test,dtype=float),'inv_test':np.asarray(inv_test,dtype=float),'GS_test':GS_test,'PatientId_test':np.asarray(PatientId_test,dtype=int),'idcore_test':np.asarray(idcore_test,dtype=int),
                                        'data_val':data_val,'label_val':np.asarray(label_val,dtype=float),'inv_val':np.asarray(inv_val,dtype=float),'GS_val':GS_val,'PatientId_val':np.asarray(PatientId_val,dtype=int),'idcore_val':np.asarray(idcore_val,dtype=int),
                                        'RF_freq':self.RF_freq})

                    print('Data is saved at:Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_MeanFFT_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr))
        elif self.RF:
                    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_RF_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
                                        'data_train':data_train,'label_train':np.asarray(label_train,dtype=float),'inv_train':np.asarray(inv_train,dtype=float),'GS_train':GS_train,'PatientId_train':np.asarray(PatientId_train,dtype=int),'idcore_train':np.asarray(idcore_train,dtype=int),
                                        'data_test':data_test,'label_test':np.asarray(label_test,dtype=float),'inv_test':np.asarray(inv_test,dtype=float),'GS_test':GS_test,'PatientId_test':np.asarray(PatientId_test,dtype=int),'idcore_test':np.asarray(idcore_test,dtype=int),
                                        'data_val':data_val,'label_val':np.asarray(label_val,dtype=float),'inv_val':np.asarray(inv_val,dtype=float),'GS_val':GS_val,'PatientId_val':np.asarray(PatientId_val,dtype=int),'idcore_val':np.asarray(idcore_val,dtype=int),
                                        'RF_freq':self.RF_freq})

                    print('Data is saved at:Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_RF_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr))

        elif self.DS:
#                    ## Train data-saving
#                    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_train_bal_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
#                                        'data_train':data_train,'label_train':np.asarray(label_train,dtype=float),'inv_train':np.asarray(inv_train,dtype=float),'GS_train':GS_train,'PatientId_train':np.asarray(PatientId_train,dtype=int),'idcore_train':np.asarray(idcore_train,dtype=int),
#                                        'PatientId_val':np.asarray(PatientId_val,dtype=int),'idcore_val':np.asarray(idcore_val,dtype=int),
#                                        'RF_freq':self.RF_freq})
#
#                    print('Train Data is saved at:Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_train_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr))
#                            
#                    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_val_bal_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
#                                        'data_val':data_val,'label_val':np.asarray(label_val,dtype=float),'inv_val':np.asarray(inv_val,dtype=float),'GS_val':GS_val,'PatientId_val':np.asarray(PatientId_val,dtype=int),'idcore_val':np.asarray(idcore_val,dtype=int),
#                                        'RF_freq':self.RF_freq})
##                    np.savez('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_val_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
##                                        'data_val':data_val,'label_val':np.asarray(label_val,dtype=float),'inv_val':np.asarray(inv_val,dtype=float),'GS_val':GS_val,'PatientId_val':np.asarray(PatientId_val,dtype=int),'idcore_val':np.asarray(idcore_val,dtype=int),
##                                        'RF_freq':self.RF_freq})
#
#                    print('Val Data is saved at:Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_val_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr))

                    ## Test data-saving
                    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_test_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr),{
                                       'data_test':data_test,'label_test':np.asarray(label_test,dtype=float),'inv_test':np.asarray(inv_test,dtype=float),'GS_test':GS_test,'PatientId_test':np.asarray(PatientId_test,dtype=int),'idcore_test':np.asarray(idcore_test,dtype=int),
                                        'RF_freq':self.RF_freq})

                    print('Test Data is saved at:Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_DS_FFT_test_P%s_%s_%s_%s_%s.mat' %(self.minP.get(),self.maxP.get(),s1,s2,timestr))
#                                                           


def remove_patients(Cids,Pids):
    Cids_Ex=[]
    for i in range(len(Cids)):
        if not (Cids[i] in Pids):
            Cids_Ex.append(Cids[i])
    return Cids_Ex

def splitBenign(Benign_Pids,NoBTr,NoBTe,NoBVa):
    Train_BPids=random.sample(Benign_Pids,NoBTr)
    Train_BPids=np.unique(Train_BPids)
    
    Benign_Pids_ExTr=remove_patients(Benign_Pids,Train_BPids)
    Test_BPids=random.sample(Benign_Pids_ExTr,NoBTe)
    Test_BPids=np.unique(Test_BPids)
    Benign_Pids_ExTrTe=remove_patients(Benign_Pids_ExTr,Test_BPids)
    if NoBVa>len(Benign_Pids_ExTrTe):
        Val_BPids=np.unique(Benign_Pids_ExTrTe)
    else:
        Val_BPids=np.unique(random.sample(Benign_Pids_ExTrTe,NoBVa))
    
    
    return Train_BPids,Test_BPids,Val_BPids

#def saveData(CCids,RF):
#   
#   for i in range(len(CCids)):
#        data=spio.loadmat(CCids[i].fname)
#        
#        if RF:
#            CCids[i].data=data["RFROI"]["data"][0][0]
#        else:
#            CCids[i].data=data["meanRF"]
#   return CCids
def saveData(CCids,DS):
   
   for i in range(len(CCids)):
        data=spio.loadmat(CCids[i].fname)
        
        if DS:
            CCids[i].data=data["masekd_FFT"]
        else:
            CCids[i].data=data["meanRF"]            
   return CCids



if __name__ == "__main__":

   
    # Create save directory if not exists

        
    Balance=True
    augm=True
    Multi=False

    # data dir
    data_dir="Z:/shared/images/ProstateVGH-2/Data/"
    
    #filtering queries
    wind = Tk()
    selection=FilterWin(wind)
    wind.mainloop()
    
        

            
#    hdf5storage.savemat('Z:/shared/images/ProstateVGH-2/Data/Dataset/InProstate/BK_MeanFFT_NoMean_RF_P91_110.mat',{'data':data_4B,'label':label_4B,'GS':GS_4,'inv':inv_4,'idcore_train':idcore_4B,'RF_freq':RF_freq})

