% %% save Core IDs
clear all
% %% loads all PID and CIS form dataset p1_90 resized images   256x256

path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\';

% load([path 'BK_DS_FFT_res_train_bal_P2_30___20200819-202527_bal']);
load([path 'BK_DS_FFT_res_train_bal_P2_30___20200824-135409_bal']); %v2
idcore_train1=idcore_train;
PID_train1=PatientId_train;
clear data_train GS_trian idcore_train label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_res_train_bal_P31_60___20200819-224422_bal']);
load([path 'BK_DS_FFT_res_train_bal_P31_60___20200824-152546_bal']); % v2
idcore_train2=idcore_train;
PID_train2=PatientId_train;
clear data_train GS_trian idcore_train label_train RF_freq idcore_train PatientId_train
% 
% load([path 'BK_DS_FFT_res_train_bal_P61_90___20200819-230238_bal']);
load([path 'BK_DS_FFT_res_train_bal_P61_90___20200824-161943_bal']);
idcore_train3=idcore_train;
PID_train3=PatientId_train;
clear data_train GS_trian idcore_train label_train RF_freq idcore_train PatientId_train



% 
% 
idcore_train=[idcore_train1 idcore_train2  idcore_train3];
PID_train=[PID_train1 PID_train2 PID_train3] ;
% 
 %%
%%% val
% load([path 'BK_DS_FFT_res_val_bal_P2_45___20200820-095307_bal']);
load([path 'BK_DS_FFT_res_val_bal_P2_45___20200824-130728_bal']);
idcore_val1=idcore_val;
PID_val1=PatientId_val;
clear data_val GS_val idcore_val label_val RF_freq PatientId_val

% load([path 'BK_DS_FFT_res_val_bal_P46_90___20200820-100958_bal']);
load([path 'BK_DS_FFT_res_val_bal_P46_90___20200824-122556_bal']);
idcore_val2=idcore_val;
PID_val2=PatientId_val;
clear data_val GS_val idcore_val label_val RF_freq PatientId_val

% 
% 
idcore_val=[idcore_val1 idcore_val2];
PID_val=[PID_val1 PID_val2];
% 
save('Lable_IDs_Highinv_balanced_P1_90_res.mat','idcore_train','PID_train','idcore_val','PID_val');

%% Test -data
path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\';
load([path 'BK_DS_FFT_res_test_P91_100___20200826-114829']);
idcore_test1=idcore_test;
PID_test1=PatientId_test;
clear data_test GS_test PatientId_test
% % 
load([path 'BK_DS_FFT_res_test_P101_110___20200826-122827']);
idcore_test2=idcore_test;
PID_test2=PatientId_test;
clear data_test GS_test PatientId_test
% % 
idcore_test=[idcore_test1 idcore_test2];
PID_test=[PID_test1 PID_test2];
save('Lable_IDs_test_Highinv_P101_1110_res.mat','idcore_test','PID_test');

%% Test -data P111-140
path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\';
load([path 'BK_DS_FFT_res_test_P111_125___20200914-000325']);
idcore_test1=idcore_test;
PID_test1=PatientId_test;
clear data_test GS_test PatientId_test
% % 
load([path 'BK_DS_FFT_res_test_P126_140___20200913-203303']);
idcore_test2=idcore_test;
PID_test2=PatientId_test;
clear data_test GS_test PatientId_test
% % 
idcore_test=[idcore_test1 idcore_test2];
PID_test=[PID_test1 PID_test2];
save('Lable_IDs_test_Highinv_P110_140_res.mat','idcore_test','PID_test');

%% find the corresponding label from dataset and generate the mask
path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\';
% Highinv_B_labels='Lable_IDs_Highinv_balanced_P1_90_res';
% Highinv_B_labels='Lable_IDs_test_Highinv_P101_1110_res';
Highinv_B_labels='Lable_IDs_test_Highinv_P110_140_res';
phase=3; % phase: train=1, val=2, test=3

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
% filename = 'dataset'; % data set used for unet
% Data=xlsread(filename);

filename = 'dataset_1_140'; % data set used for unet
Data=xlsread(filename);
   

PID=Data(:,12);
CID=Data(:,3);
rf_mask=[]; m=0; 

for i=1:length(cids)

    if cids(i)<=752
        Patient=Data(cids(i),12);
        Score=Data(cids(i),16);
        core=Data(cids(i),3);
    else
        Patient=Data((cids(i)-1),12);
        Score=Data((cids(i)-1),16);
        core=Data((cids(i)-1),3);
    end
    if Score~=3 %% && Patient~=118 && Patient~=138
    m=m+1;
    
%     core=Data(cids(i),3);
    disp(['PID=' num2str(Patient) '  core=' num2str(core)] )
    data_dir1=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
    dirlist=dir(data_dir1);
    data_dir = strcat(data_dir1,'\',dirlist(3).name,'\BMode\ROI_Data\Down_Sample\Labels\res\');
%     load([data_dir 'RFROI_mask_' num2str(core) '.mat']);
    load([data_dir 'RFROI_mask_' num2str(core) '.mat']);
    rf_mask{m}=ROI_mask_down_2;
    size(rf_mask);
    end
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
    save('Labels_masks_train_Highinv_bal_p1_90_res.mat','rf_mask2');
    save('Labels_masks_train_Highinv_bal_p1_90_new_res.mat','rf_mask2_new');
    save('Labels_masks_train_Highinv_bal_p1_90_new_scale_res.mat','rf_mask2_new_S');
elseif phase ==2
    save('Labels_masks_val_Highinv_bal_p1_90_res.mat','rf_mask2');
    save('Labels_masks_val_Highinv_bal_p1_90_new_res.mat','rf_mask2_new');
    save('Labels_masks_val_Highinv_bal_p1_90_new_scale_res.mat','rf_mask2_new_S');
elseif phase ==3
%     save('Labels_masks_test_Highinv_bal_p1_90_res.mat','rf_mask2');
%     save('Labels_masks_test_Highinv_bal_p1_90_new_res.mat','rf_mask2_new');
%     save('Labels_masks_test_Highinv_bal_p1_90_new_scale_res.mat','rf_mask2_new_S');
    save('Labels_masks_test_Highinv_bal_p111_140_res.mat','rf_mask2');
    save('Labels_masks_test_Highinv_bal_p111_140_new_res.mat','rf_mask2_new');
    save('Labels_masks_test_Highinv_bal_p111_140_new_scale_res.mat','rf_mask2_new_S');
end
% save([path save_name,'rf_mask']);


% load('Labels_masks_val.mat','rf_mask');
% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\Labels_masks_test.mat','rf_mask2');

