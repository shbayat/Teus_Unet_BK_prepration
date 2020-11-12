%Generate high inv data, inv and PID and GS  for test_data
clear all
close all

path='Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Ds\';

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
    
