clc
clear all
close all
%% load high inv data and saves balanced data
%%% val 1 all benign
%%% val 2 1/17
%%% val 3 0/11
%%% val 4 4/4
%% P 1-90 cropped 256x140 images
% path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\';
% Val1='BK_DS_FFT_val_bal_P2_45___20200708-235010';34----8
% Val2='BK_DS_FFT_val_bal_P46_90___20200709-004809'; %21 cores---16
% Train1='BK_DS_FFT_train_bal_P2_30___20200709-010440';88-----44
% Train2='BK_DS_FFT_train_bal_P31_60___20200709-012717';33---12
% Train3='BK_DS_FFT_train_bal_P61_90___20200709-020828';88---76
% 
% Test1='BK_DS_FFT_test_P111_125___20200805-130102';
% Test2='BK_DS_FFT_test_P126_140___20200805-123805';
% load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_val_bal_P2_45___20200708-235010.mat')

 %% P 1-90 resized images 256x256
% path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv\';
% save_path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced\';
% Val1='BK_DS_FFT_res_val_bal_P2_45___20200820-095307';%% 32 -->4
% Val2='BK_DS_FFT_res_val_bal_P46_90___20200820-100958';%39--->26
% Train1='BK_DS_FFT_res_train_bal_P2_30___20200819-202527'; %%77 --->22
% Train2='BK_DS_FFT_res_train_bal_P31_60___20200819-224422';%%  -->6
% Train3='BK_DS_FFT_res_train_bal_P61_90___20200819-230238';%% 69--->38
% 
% % Test1='BK_DS_FFT_test_P111_125___20200805-130102';
% % Test2='BK_DS_FFT_test_P126_140___20200805-123805';

%% P 1-90 resized images 256x256 v2
% path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_v2\';
% save_path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\';
% Val1='BK_DS_FFT_res_val_bal_P2_45___20200824-130728'; %34-->8
% Val2='BK_DS_FFT_res_val_bal_P46_90___20200824-122556';%21--->16
% Train1='BK_DS_FFT_res_train_bal_P2_30___20200824-135409';%88---44
% Train2='BK_DS_FFT_res_train_bal_P31_60___20200824-152546';%33----12
Train3='BK_DS_FFT_res_train_bal_P61_90___20200824-161943';%76----76

%% P 1-90 zero padded data 256x530

path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\';
save_path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\';
% Val1='BK_DS_FFT_zp_val_bal_P2_45___20201002-103435'; %32-->4
% Val2='BK_DS_FFT_zp_val_bal_P46_90___20201002-104645';%17--->8

% Train1='BK_DS_FFT_zp_train_bal_P2_30___20201001-141613';%77---22
% Train2='BK_DS_FFT_zp_train_bal_P31_60___20201001-213351';%30----6
% Train3='BK_DS_FFT_zp_train_bal_P61_90___20201001-235651';%69----38
Train4='BK_DS_FFT_zp_test_P111_125___20201007-080643';%84--->38
% Val3='BK_DS_FFT_zp_test_P126_140___20201007-081802';%69-->32
%% total train= 22+6+38= 66
%% total train= 22+6+38+38=104 after adding p111-125 to train
%% total val= 4+8=12
%%% toal val new= 12+32=44

% % %% Val
% DATA=Val3;
% load([path DATA]);
% label_val=label_test;
% GS_val=GS_test;
% idcore_val=idcore_test;
% PatientId_val=PatientId_test;
% inv_val=inv_test;
% data_val=data_test;

% [val idx]=find(label_val);
% label_val=label_val(1:(2*length(idx)));
% data_val=data_val(1:(2*length(idx)));
% GS_val=GS_val(1:(2*length(idx)));
% idcore_val=idcore_val(1:(2*length(idx)));
% PatientId_val=PatientId_val(1:(2*length(idx)));
% inv_val=inv_val(1:(2*length(idx)));
% save_name=[save_path DATA '_bal'];
% save(save_name,'label_val','GS_val','idcore_val','PatientId_val','inv_val','data_val', "-V7.3");
% 
% 
%% Train
DATA=Train4;
load([path DATA]);


label_train=label_test;
GS_train=GS_test;
idcore_train=idcore_test;
PatientId_train=PatientId_test;
inv_train=inv_test;
data_train=data_test;

[val idx]=find(label_train);
label_train=label_train(1:(2*length(idx)));
data_train=data_train(1:(2*length(idx)));
GS_train=GS_train(1:(2*length(idx)));
idcore_train=idcore_train(1:(2*length(idx)));
PatientId_train=PatientId_train(1:(2*length(idx)));
inv_train=inv_train(1:(2*length(idx)));
% save_name=[save_path DATA '_bal'];
% save(save_name,'label_train','GS_train','idcore_train','PatientId_train','inv_train','data_train', "-V7.3");

 %% Test
% DATA=Test1;
% load([path DATA]);
% [val idx]=find(label_test);
% label_test=label_test(1:(2*length(idx)));
% data_test=data_test(1:(2*length(idx)));
% GS_test=GS_test(1:(2*length(idx)));
% idcore_test=idcore_test(1:(2*length(idx)));
% PatientId_test=PatientId_test(1:(2*length(idx)));
% inv_test=inv_test(1:(2*length(idx)));
% save_name=[save_path DATA '_bal'];
% save(save_name,'label_test','GS_test','idcore_test','PatientId_test','inv_test','data_test', "-V7.3");
% 








%% Test - Generate high inv balanced for patient 111-140
% DATA=Test2;
% load([path DATA]);
% [val idx]=find(label_test);
% 
% label_train=label_test;
% data_train=data_test;
% GS_train=GS_test;
% idcore_train=idcore_test;
% PatientId_train=PatientId_test;
% inv_train=inv_test;
% 
% 
% label_train=label_train(1:(2*length(idx)));
% data_train=data_train(1:(2*length(idx)));
% GS_train=GS_train(1:(2*length(idx)));
% idcore_train=idcore_train(1:(2*length(idx)));
% PatientId_train=PatientId_train(1:(2*length(idx)));
% inv_train=inv_train(1:(2*length(idx)));
% save_name=[path DATA '_bal'];
% save(save_name,'label_train','GS_train','idcore_train','PatientId_train','inv_train','data_train', "-V7.3");
