clc
clear all

%% 1- Re save test data
% load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P91_100___20200826-114829.mat')

% load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P101_110___20200826-122827.mat')%  
% 
% clear data_test
% 
% %   save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P91_100___20200826-114829_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')
% %  save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P101_110___20200826-122827_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')
% 
% 
% % % 
% % % %% 3- save all CIS and PIds
% % % 
% % % t1=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P111_125___20200805-130102_info.mat');
% % % t2=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P126_140___20200805-123805_info.mat');
% % % 
% % % idcore_test=[t1.idcore_test t2.idcore_test];
% % % PatientId_test=[t1.PatientId_test t2.PatientId_test];
% % % 
% % % save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Lable_IDs_test_P111_140.mat','idcore_test','PatientId_test');

% %% 2-  Re save test data P111=140
% load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P111_125___20200914-000325.mat')%  
% clear data_test
% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P111_125___20200914-000325_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')
% 
% % load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P126_140___20200913-203303.mat')%  
% % clear data_test
% %  save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\DS_res\Highinv_Balanced_v2\BK_DS_FFT_res_test_P126_140___20200913-203303_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')
% 
% 
% % 
% % %% 3- save all CIS and PIds
% % 
% % t1=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P111_125___20200805-130102_info.mat');
% % t2=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\BK_DS_FFT_test_P126_140___20200805-123805_info.mat');
% % 
% % idcore_test=[t1.idcore_test t2.idcore_test];
% % PatientId_test=[t1.PatientId_test t2.PatientId_test];
% % 
% % save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Lable_IDs_test_P111_140.mat','idcore_test','PatientId_test');


%% 1-  Re save test data P111=140 - pz to just save info
load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\BK_DS_FFT_zp_test_P111_125___20201007-080643.mat')%  
% clear data_test
% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\BK_DS_FFT_zp_test_P111_125___20201007-080643_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')
% 
load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\BK_DS_FFT_zp_test_P126_140___20201007-081802.mat')%  
% clear data_test
%  save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\BK_DS_FFT_zp_test_P126_140___20201007-081802_info.mat','GS_test','idcore_test','inv_test','label_test','PatientId_test','RF_freq','-V7.3')

%% 3- save all CIS and PIds

% t1=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\BK_DS_FFT_zp_test_P111_125___20201007-080643_info.mat');
% t2=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\BK_DS_FFT_zp_test_P126_140___20201007-081802_info.mat');
% % % 
% idcore_test=[t1.idcore_test t2.idcore_test];
% PatientId_test=[t1.PatientId_test t2.PatientId_test];
% % 
% % save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Lable_IDs_test_P111_140.mat','idcore_test','PatientId_test');

