%Generate high inv data  test_data
clear all
close all

path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';
load([path 'BK_DS_FFT_train_5_P71_90___20200515-122437']);

data_train2=data_train;
GS_train2=GS_train;
idcore_train2=idcore_train;
label_train2=label_train;
PatientId_train2=PatientId_train;
PatientId_val2=PatientId_val;
inv_train2=inv_train;
m=1;
clear data_train GS_train idcore_train label_train PatientId_train PatientId_val inv_train

for i=1:length(inv_train2)
    if inv_train2(i)>=0.4 || inv_train2(i)==0
        data_train{m}=data_train2{i};
        GS_train(m)=GS_train2(i);
        idcore_train(m)=idcore_train2(i);
        label_train(m)=label_train2(i);
        PatientId_train(m)=PatientId_train2(i);
%         PatientId_val(m)=PatientId_val2(i);
        inv_train(m)=inv_train2(i);
              
        m=m+1;
    end
end

save([path 'BK_DS_FFT_highinv_train_5_P71_90___20200515-122437.mat'],'data_train','GS_train','idcore_train','label_train','PatientId_train','inv_train','-V7.3')
    
