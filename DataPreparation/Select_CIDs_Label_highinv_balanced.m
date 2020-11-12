%% save Core IDs
clear all
%% loads all PID and CIS form dataset used for Unet
% path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\Highinv_balanced\';
% load([path 'BK_DS_FFT_train_bal_P2_30___20200709-010440_bal']);
% idcore_train1=idcore_train;
% PID_train1=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_train_bal_P31_60___20200709-012717_bal']);
% idcore_train2=idcore_train;
% PID_train2=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_train_bal_P61_90___20200709-020828_bal']);
% idcore_train3=idcore_train;
% PID_train3=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% 
% idcore_train=[idcore_train1 idcore_train2 idcore_train3];
% PID_train=[PID_train1 PID_train2 PID_train3];
% 
% %%% val
% load([path 'BK_DS_FFT_val_bal_P2_45___20200708-235010_bal']);
% idcore_val1=idcore_val;
% PID_val1=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% load([path 'BK_DS_FFT_val_bal_P46_90___20200709-004809_bal']);
% idcore_val2=idcore_val;
% PID_val2=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% 
% idcore_val=[idcore_val1 idcore_val2];
% PID_val=[PID_val1 PID_val2];
% 
% save('Lable_IDs_Highinv_balanced.mat','idcore_train','PID_train','idcore_val','PID_val');

% Test -data 91-110
% path='D:\Sharareh\Prostate_Project\Preparation\DataPreparation\data_BK\';
% load([path 'BK_DS_FFT_test_6_P91_100___20200529-170113']);
% idcore_test1=idcore_test;
% PID_test1=PatientId_test;
% clear data_test GS_test PatientId_test

% load([path 'BK_DS_FFT_test_6_P101_110___20200515-114746']);
% idcore_test2=idcore_test;
% PID_test2=PatientId_test;
% clear data_test GS_test PatientId_test
% 
% idcore_test=[idcore_test1 idcore_test2];
% PID_test=[PID_test1 PID_test2];
% save('Lable_IDs_test.mat','idcore_test','PID_test');



%% find the corresponding label from dataset and generate the mask
path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\Highinv_balanced\';
Highinv_B_labels='Lable_IDs_Highinv_balanced';
phase=2; % phase: train=1, val=2, test=3

if phase ==1
    load([path Highinv_B_labels])
    cids=idcore_train';
elseif phase ==2
    load([path Highinv_B_labels])
    cids=idcore_val';
elseif phase ==3
    load([path Highinv_B_labels])
    cids=idcore_test';
end
filename = 'dataset'; % data set used for unet
Data=xlsread(filename);
   
PID=Data(:,12);
CID=Data(:,3);
rf_mask=[]; m=0;   
for i=1:length(cids)
    Patient=Data(cids(i),12);
    m=m+1;
    core=Data(cids(i),3);
    disp(['PID=' num2str(Patient) '  core=' num2str(core)] )
    data_dir1=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
    dirlist=dir(data_dir1);
    data_dir = strcat(data_dir1,'\',dirlist(3).name,'\BMode\ROI_Data\Down_Sample\Labels\');
%     load([data_dir 'RFROI_mask_' num2str(core) '.mat']);
    load([data_dir 'RFROI_mask_' num2str(core) '.mat']);
    rf_mask{m}=ROI_mask_down_2;
    size(rf_mask);

end

%%% expanding rf_mask
for i=1:length(rf_mask)
    rf_mask2(i,:,:,:)=rf_mask{i};
end

if phase==1
    save('Labels_masks_train_Highinv_bal.mat','rf_mask2');
elseif phase ==2
    save('Labels_masks_val_Highinv_bal.mat','rf_mask2');
elseif phase ==3
    save('Labels_masks_test_Highinv_bal.mat','rf_mask2');    
end
% save([path save_name,'rf_mask']);


% load('Labels_masks_val.mat','rf_mask');
% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\Labels_masks_test.mat','rf_mask2');

