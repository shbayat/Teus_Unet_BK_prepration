%Generate high inv data  for val and test_data
clear all
close all

path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';
% load([path 'BK_DS_FFT_val_2_P16_30___20200515-083413']);
% 
% data_val2=data_val;
% GS_val2=GS_val;
% idcore_val2=idcore_val;
% label_val2=label_val;
% PatientId_val2=PatientId_val;
% inv_val2=inv_val;
% m=1;
% clear data_val GS_val idcore_val label_val PatientId_val PatientId_val inv_val
% 
% for i=1:length(inv_val2)
%     if inv_val2(i)>=0.4 || inv_val2(i)==0
%         data_val{m}=data_val2{i};
%         GS_val(m)=GS_val2(i);
%         idcore_val(m)=idcore_val2(i);
%         label_val(m)=label_val2(i);
%         PatientId_val(m)=PatientId_val2(i);
% %         PatientId_val(m)=PatientId_val2(i);
%         inv_val(m)=inv_val2(i);
%               
%         m=m+1;
%     end
% end
% 
% save([path 'BK_DS_FFT_highinv_val_2_P16_30___20200515-083413.mat'],'data_val','GS_val','idcore_val','label_val','PatientId_val','inv_val','-V7.3')
%  
%% test
load([path 'BK_DS_FFT_test_6_P101_110___20200515-114746']);

data_test2=data_test;
GS_test2=GS_test;
idcore_test2=idcore_test;
label_test2=label_test;
PatientId_test2=PatientId_test;
inv_test2=inv_test;
m=1;
clear data_test GS_test idcore_test label_test PatientId_test PatientId_test inv_test

for i=1:length(inv_test2)
    if inv_test2(i)>=0.4 || inv_test2(i)==0
        data_test{m}=data_test2{i};
        GS_test(m)=GS_test2(i);
        idcore_test(m)=idcore_test2(i);
        label_test(m)=label_test2(i);
        PatientId_test(m)=PatientId_test2(i);
%         PatientId_test(m)=PatientId_test2(i);
        inv_test(m)=inv_test2(i);
              
        m=m+1;
    end
end

save([path 'BK_DS_FFT_highinv_test_6_P101_110___20200515-114746.mat'],'data_test','GS_test','idcore_test','label_test','PatientId_test','inv_test','-V7.3')
    
