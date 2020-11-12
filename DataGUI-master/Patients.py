# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:29:54 2020

@author: samadi
"""

class Patient:
  def __init__(self, no_cores=8, RF_freq=50, date=''):
    self.no_cores = no_cores
    self.RF_freq = RF_freq
    self.date = date
    self.cores=[]

  def init_cores(self, Label, GS, Inv,fname):
    for i in range(self.no_cores):
        self.cores.append(core(Label, GS, Inv,fname))

class core:
  def __init__(self,Cid,CNo, PNo,Label, GS, Inv,fname='',dat='NULL'):
    self.Cid=Cid
    self.CNo=CNo
    self.PNo=PNo
    self.Label = Label
    self.GS = GS
    self.Inv = Inv
    self.fname = fname
    self.data=dat
    
  def getP(self):
    return self.PNo
    