%% save Core IDs
clear all
%% loads all PID and CIS form dataset used for Unet
% path='D:\Sharareh\Prostate_Project\Preparation\DataPreparation\data_BK\';
% load([path 'BK_DS_FFT_train_1_P2_15___20200515-081151']);
% idcore_train1=idcore_train;
% PID_train1=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_train_2_P16_30___20200515-083413']);
% idcore_train2=idcore_train;
% PID_train2=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_train_3_P31_50___20200515-084635']);
% idcore_train3=idcore_train;
% PID_train3=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_train_4_P51_70___20200515-094734']);
% idcore_train4=idcore_train;
% PID_train4=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% PID_trainload([path 'BK_DS_FFT_train_5_P71_90___20200515-122437']);
% idcore_train5=idcore_train;
% PID_train5=PatientId_train;
% clear data_train GS_trian idcore_val label_train RF_freq idcore_train PatientId_train
% 
% idcore_train=[idcore_train1 idcore_train2 idcore_train3 idcore_train4 idcore_train5];
% PID_train=[PID_train1 PID_train2 PID_train3 PID_train4 PID_train5];
% 
% %%% val
% load([path 'BK_DS_FFT_val_1_P2_15___20200515-081151']);
% idcore_val1=idcore_val;
% PID_val1=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% load([path 'BK_DS_FFT_val_2_P16_30___20200515-083413']);
% idcore_val2=idcore_val;
% PID_val2=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% load([path 'BK_DS_FFT_val_3_P31_50___20200515-084635']);
% idcore_val3=idcore_val;
% PID_val3=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% load([path 'BK_DS_FFT_val_4_P51_70___20200515-094734']);
% idcore_val4=idcore_val;
% PID_val4=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% load([path 'BK_DS_FFT_val_5_P71_90___20200515-122437']);
% idcore_val5=idcore_val;
% PID_val5=PatientId_val;
% clear data_val GS_val idcore_val label_val RF_freq PatientId_val
% 
% idcore_val=[idcore_val1 idcore_val2 idcore_val3 idcore_val4 idcore_val5];
% PID_val=[PID_val1 PID_val2 PID_val3 PID_val4 PID_val5];
% 
% save('Lable_IDs.mat','idcore_train','PID_train','idcore_val','PID_val');

% Test -data
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
%% Train- select the CIDs and save the masks

phase=3; % phase: train=1, val=2, test=3

if phase ==1
    load('Lable_IDs')
    cids=idcore_train';
elseif phase ==2
    load('Lable_IDs')
    cids=idcore_val';
elseif phase ==3
    load('Lable_IDs_test')
    cids=idcore_test';
end
filename = 'dataset'; % data set used for unet
Data=xlsread(filename);
   
PID=Data(:,12);
CID=Data(:,3);
rf_mask=[]; m=0;   
for i=1:length(cids)
    find_coreID=find(Data(:,1)==cids(i));
    Patient=Data(find_coreID,12);  %%% changed this for test data
    m=m+1;
    core=Data(find_coreID,3);
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
    rf_mask2_new=rf_mask2;
    rf_mask2_new(rf_mask2_new~=0) =1;
    rf_mask2_new_S(i,:,:,:)=rf_mask{i}/255;
%     figure(1);imagesc(squeeze(rf_mask2(i,:,:,1)));colormap gray;title('original')
%     figure(2);imagesc(squeeze(rf_mask2_new(i,:,:,1)));colormap gray;title('abs')
%     figure(3);imagesc(squeeze(rf_mask2_new_S(i,:,:,1)));colormap gray;title('scaled')
end

if phase==1
    save('Labels_masks_train_2.mat','rf_mask2');
    save('Labels_masks_train_new.mat','rf_mask2_new');
    save('Labels_masks_train_new_scale.mat','rf_mask2_new_S');
elseif phase ==2
    save('Labels_masks_val_2.mat','rf_mask2');
    save('Labels_masks_val_new.mat','rf_mask2_new');
    save('Labels_masks_val_new_scale.mat','rf_mask2_new_S');
elseif phase ==3
    save('Labels_masks_test.mat','rf_mask2');
    save('Labels_masks_test_new.mat','rf_mask2_new');
    save('Labels_masks_test_new_scale.mat','rf_mask2_new_S'); 
end
 
% load('Labels_masks_val.mat','rf_mask');
% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\Labels_masks_test.mat','rf_mask2');

