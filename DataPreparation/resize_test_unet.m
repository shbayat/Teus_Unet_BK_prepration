%% resize data_test
clear all

load('D:\Sharareh\Prostate_Project\Preparation\DataPreparation\data_BK\BK_DS_FFT_test_6_P91_100___20200515-113213.mat')
% load('D:\Sharareh\Prostate_Project\Preparation\DataPreparation\data_BK\BK_DS_FFT_test_6_P101_110___20200515-114746.mat')

data_test2=data_test;
GS_test2=GS_test;
inv_test2=inv_test;
PatientId_test2=PatientId_test;
idcore_test2=idcore_test;
%% for part 1
data_test=data_test2(1:27);
GS_test=GS_test2(1:27);
inv_test=inv_test2(1:27);
PatientId_test=PatientId_test2(1:27);
idcore_test=idcore_test2(1:27);

save('BK_DS_FFT_test_6_1_P91_100___20200515-113213.mat','data_test','GS_test','inv_test','PatientId_test','idcore_test','-v7.3')
% save('BK_DS_FFT_test_6_1_P101_110___20200515-114746.mat','data_test','GS_test','inv_test','PatientId_test','idcore_test','-v7.3')
%% for part 2
data_test=data_test2(1:27);
GS_test=GS_test2(1:27);
inv_test=inv_test2(1:27);
PatientId_test=PatientId_test2(1:27);
idcore_test=idcore_test2(1:27);
save('BK_DS_FFT_test_6_2_P91_100___20200515-113213.mat','data_test','GS_test','inv_test','PatientId_test','idcore_test','-v7.3')
% save('BK_DS_FFT_test_6_2_P101_110___20200515-114746.mat','data_test','GS_test','inv_test','PatientId_test','idcore_test','-v7.3')