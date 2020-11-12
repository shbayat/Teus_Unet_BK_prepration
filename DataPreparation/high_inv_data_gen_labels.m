clear all
close all

%%% load train inv all
path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';

%% train
% load([path 'BK_DS_FFT_train_all.mat'],'inv_train');
% 
% load([path 'Labels_masks_train.mat']);
% rf_mask2_new_S2=rf_mask2_new_S;
% clear rf_mask2_new_S
% 
% m=1;
% for i=1:length(inv_train) % 273
%     if inv_train(i)>=0.4 || inv_train(i)==0
%         rf_mask2_new_S(m,:,:,:)=rf_mask2_new_S2(i,:,:,:);
%         m=m+1;
%     end
% end
% 
% save([path 'Labels_masks_train_highinv.mat'],'rf_mask2_new_S');

% %% val
% load([path 'BK_DS_FFT_val_all.mat'],'inv_val');
% 
% load([path 'Labels_masks_val.mat']);
% rf_mask2_new_S2=rf_mask2_new_S;
% clear rf_mask2_new_S
% 
% m=1;
% for i=1:length(inv_val) % 273
%     if inv_val(i)>=0.4 || inv_val(i)==0
%         rf_mask2_new_S(m,:,:,:)=rf_mask2_new_S2(i,:,:,:);
%         m=m+1;
%     end
% end
% 
% save([path 'Labels_masks_val_highinv.mat'],'rf_mask2_new_S');

%% test
load([path 'BK_DS_FFT_test_all.mat'],'inv_test');

load([path 'Labels_masks_test.mat']);
rf_mask2_new_S2=rf_mask2_new_S;
clear rf_mask2_new_S

m=1;
for i=1:length(inv_test) % 273
    if inv_test(i)>=0.4 || inv_test(i)==0
        rf_mask2_new_S(m,:,:,:)=rf_mask2_new_S2(i,:,:,:);
        m=m+1;
    end
end

save([path 'Labels_masks_test_highinv.mat'],'rf_mask2_new_S');