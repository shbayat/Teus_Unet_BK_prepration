% %% save Core IDs
clear all
clc
path='Z:\workspace\Sharareh\Philips_local\data\philips\';
data_dir='Z:\workspace\Sharareh\Philips_local\data\masks_m\';
% load([path 'train_pickle']);
load([path 'val_pickle']);
rf_mask=[]; m=0;
phase=2; %val

for i =1:length(unpickled_df_val)
    temp=unpickled_df_val(i,:);
    load([data_dir  temp '_ROImask.mat']);
    rf_mask{i}=ROI_mask_down_2;
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
    save('Labels_masks_train_philips.mat','rf_mask2');
    save('Labels_masks_train_philips_new.mat','rf_mask2_new');
    save( 'Labels_masks_train_philips_new_scal.mat','rf_mask2_new_S');
elseif phase ==2
    save( 'Labels_masks_val_philips.mat','rf_mask2');
    save( 'Labels_masks_val_philips_new.mat','rf_mask2_new');
    save( 'Labels_masks_val_philips_new_scal.mat','rf_mask2_new_S');
end


