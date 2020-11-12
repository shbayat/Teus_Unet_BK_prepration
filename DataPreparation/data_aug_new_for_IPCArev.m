%%data_augmentaiton new for IPCAI- Revision
%%% Combinaiton of new data (mix of 30+9 data and test in previous ipca, and the augmented data'

clear all
close all

data_aug_old=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\Synthetic\combined.mat');

data_new=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\BK_RF_Train_Test_IPCAIRev.mat');

data_train=cell(1,188);
label_train=cell(1,188);
inv_train=cell(1,188);


data_train=[data_new.data_train(1:end) data_aug_old.data_train(95:end)];
label_train=[data_new.label_train(1:end) data_aug_old.label_train(95:end)];
inv_train=[data_new.inv_train(1:end) data_aug_old.inv_train(95:end)];

idcore_train=data_new.idcore_train;
GS_train=data_new.GS_train;


data_test=data_new.data_test;
label_test=data_new.label_test;
GS_test=data_new.GS_test;
inv_test=data_new.inv_test;
idcore_test=data_new.idcore_test;
PatientID_Test=data_new.PatientID_Test;
RF_freq=data_new.RF_freq;

save('Z:\shared\images\ProstateVGH-2\Data\Dataset\Synthetic\combined_new_IPCAIRev.mat','data_train','label_train','inv_train','data_test','label_test','GS_test','inv_test','idcore_test','PatientID_Test','RF_freq', '-v7.3')