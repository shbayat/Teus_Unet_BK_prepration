clc
clear all

%% 1- Re save test data
% load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P126_140___20200805-123805_v1.mat')

% load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P111_125___20200805-130102_v1.mat')
% 
% m=1;
% for i=1:length(inv_test)    
%         data_test2{m}=data_test{i};
%         m=m+1;
% end
% 
% clear data_test
% data_test=data_test2;
% 
%  save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P111_125___20200805-130102.mat','data_test','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')
%% 2- save data info
% 
%  save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P111_125___20200805-130102_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')


%% 3- save all CIS and PIds

t1=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P111_125___20200805-130102_info.mat');
t2=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P126_140___20200805-123805_info.mat');

idcore_test=[t1.idcore_test t2.idcore_test];
PatientId_test=[t1.PatientId_test t2.PatientId_test];

save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Lable_IDs_test_P111_140.mat','idcore_test','PatientId_test');