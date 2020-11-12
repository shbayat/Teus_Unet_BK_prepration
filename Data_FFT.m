clear all
%%% saving masked FFT with new naming

%%% load freq info
%%% for P1-110
% [ndata, text, alldata] = xlsread('D:\Sharareh\Prostate_Project\Preparation\Patient_info');
% freq=ndata(1:110,5);

%%% for P111-140
[ndata, text, alldata] = xlsread('D:\Sharareh\Prostate_Project\Preparation\Paitient_info_1_140P');
freq=ndata(1:140,5);
minf=min(freq);

%% 1- Calculate FFT
for Patient=133
    Patient
FFT_Whole(Patient,minf,freq)
end
%% 2-endate Masked FFT
% for Patient=133
%     Patient
%     FFT_Whole_masked(Patient)
% end
% figure(2);plot(abs(fft_RF(1000,1:32)))
%%% p115 and 117,121,125 there was error
%% Funcitons
function FFT_Whole(Patient,minf,freq)

data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
dirlist=dir(data_dir);
data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
data_dir2=[data_dir,'\BMode\ROI_Data\Down_Sample\'];
S_RF=dir(strcat(data_dir2,'RF_DS*.*'));
CoreNo=size(S_RF,1);

for CoreID=1:CoreNo
    RF_file= strcat(data_dir2,S_RF(CoreID).name);
    load(RF_file);
    RF_reshaped=reshape(RF_down,35840,200);    %256*140=35840    
   
    RF_FrRate=freq(Patient);
    
    %%% Resampling 
    if RF_FrRate>minf
        [P,Q] = rat(double(RF_FrRate)/minf);
        xnew = resample(RF_reshaped',P,Q);
        xnew=xnew';
    else
        xnew=RF_reshaped;
    end
    
    fft_RF=fft(xnew,200,2);
    
    %%% saving FFT
    fft_RF_file=[data_dir2,strrep(S_RF(CoreID).name,'RF_DS','FFT')];
    fft_RF_file2=strrep(fft_RF_file,'.dat','.mat');
    save(fft_RF_file2,'fft_RF');
end
end

%% MAsked_FFT FFT*Mask
function FFT_Whole_masked(Patient)
names={'00', '01', '02' ,'03','04','05','06','07','08','09'}; % for 8 and 10 cores
names2={'00', '10', '11' ,'01','02','03','04','05','06','07','08','09'}; % for more than 10
names3={'00', '10','01','02','03','04','05','06','07','08','09'}; % for coreNo==10

data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
dirlist=dir(data_dir);
data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
data_dir2=[data_dir,'\BMode\ROI_Data\Down_Sample\'];
FFT_RF=dir(strcat(data_dir2,'FFT_*.*'));

data_dir3=[data_dir,'\BMode\ROI_Data\Down_Sample\'];
Mask_RF=dir(strcat(data_dir3,'Masked_DS*.mat'));
CoreNo=size(FFT_RF,1);

for CoreID=1:CoreNo
    FFT_file= strcat(data_dir2,FFT_RF(CoreID).name);
    fft=load(FFT_file);
    
    mask_file= strcat(data_dir3,Mask_RF(CoreID).name);
    mask=load(mask_file);
    
    FFT_RF2=fft.fft_RF;
    masked_RF2=reshape(mask.masked_RF,35840,200);
    
    
    masekd_FFT=FFT_RF2.*masked_RF2;
   
    
     %%% saving Masked_FFT
%     masked_fft_file=[data_dir2,strrep(FFT_RF(CoreID).name,'FFT','Masked_FFT')];
%     masked_fft_file2=strrep(masked_fft_file,'.dat','.mat');
%     save(masked_fft_file2,'masekd_FFT');
if CoreNo<=10
    masked_fft_file=[data_dir2 'masked_FFT_' names{CoreID}];
elseif CoreNo==11
    masked_fft_file=[data_dir2 'masked_FFT_' names3{CoreID}];
elseif CoreNo>11
    masked_fft_file=[data_dir2 'masked_FFT_' names2{CoreID}];   
end
    save(masked_fft_file,'masekd_FFT');
end
end