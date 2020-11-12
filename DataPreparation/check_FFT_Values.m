%%% check FFT values
load('D:\Sharareh\Prostate_Project\Preparation\DataPreparation\data_BK\BK_DS_FFT_val_1_P2_15___20200515-081151.mat')
a1=data_val{1,1};
b1=a1(a1>0);
size1=(length(b1)/200);
b11=reshape(b1,size1,200);
abs_b1=abs(b1);
figure;plot(abs_b1(192,:))
max(max(abs_b1))


for i=1:56
b1(i,:,:)=data_train{1,i};
end
b11=abs(b1);
mb1=max(max(max(b11)));

[ind value]=b1(b1~=0);