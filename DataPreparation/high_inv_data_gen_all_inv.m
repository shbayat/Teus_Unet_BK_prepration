%Generate high inv data,  test_data
clear all
close all

%% import all val data
% path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';
% data1='BK_DS_FFT_val_1_P2_15___20200515-081151';
% data2='BK_DS_FFT_val_2_P16_30___20200515-083413';
% data3='BK_DS_FFT_val_3_P31_50___20200515-084635';
% data4='BK_DS_FFT_val_4_P51_70___20200515-094734';
% data5='BK_DS_FFT_val_5_P71_90___20200515-122437';
% load([path data1]);
% 
% inv_1=inv_val;
% clear data_val GS_val idcore_val label_val PatientId_val PatientId_val inv_val
% 
% load([path data2]);
% inv_2=inv_val;
% clear data_val GS_val idcore_val label_val PatientId_val PatientId_val inv_val
% 
% load([path data3]);
% inv_3=inv_val;
% clear data_val GS_val idcore_val label_val PatientId_val PatientId_val inv_val
% 
% load([path data4]);
% inv_4=inv_val;
% clear data_val GS_val idcore_val label_val PatientId_val PatientId_val inv_va
% 
% load([path data5]);
% inv_5=inv_val;
% clear data_val GS_val idcore_val label_val PatientId_val PatientId_val inv_val
% 
% inv_val=[inv_1 inv_2 inv_3 inv_4 inv_5];
% save([path 'BK_DS_FFT_val_all.mat'],'inv_val')
   
%% import all train data

% path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';
% data1='BK_DS_FFT_train_1_P2_15___20200515-081151';
% data2='BK_DS_FFT_train_2_P16_30___20200515-083413';
% data3='BK_DS_FFT_train_3_P31_50___20200515-084635';
% data4='BK_DS_FFT_train_4_P51_70___20200515-094734';
% data5='BK_DS_FFT_train_5_P71_90___20200515-122437';
% 
% load([path data1]);
% inv_1=inv_train;
% clear data_train GS_train idcore_train label_train PatientId_train PatientId_train inv_train
% 
% load([path data2]);
% inv_2=inv_train;
% clear data_train GS_train idcore_train label_train PatientId_train PatientId_train inv_train
% 
% load([path data3]);
% inv_3=inv_train;
% clear data_train GS_train idcore_train label_train PatientId_train PatientId_train inv_train
% 
% load([path data4]);
% inv_4=inv_train;
% clear data_train GS_train idcore_train label_train PatientId_train PatientId_train inv_va
% 
% load([path data5]);
% inv_5=inv_train;
% clear data_train GS_train idcore_train label_train PatientId_train PatientId_train inv_train
% 
% inv_train=[inv_1 inv_2 inv_3 inv_4 inv_5];
% save([path 'BK_DS_FFT_train_all.mat'],'inv_train')

%% import all test data
path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';
data1='BK_DS_FFT_test_6_P91_100___20200529-170113';
data2='BK_DS_FFT_test_6_P101_110___20200515-114746';

load([path data1]);
inv_1=inv_test;
clear  inv_test

load([path data2]);
inv_2=inv_test;
clear inv_test


inv_test=[inv_1 inv_2];
%save([path 'BK_DS_FFT_test_all.mat'],'inv_test')

