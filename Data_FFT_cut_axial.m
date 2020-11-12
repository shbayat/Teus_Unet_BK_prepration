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
for Patient=111
    Patient
FFT_Whole(Patient,minf,freq)
end

%% Funcitons
function FFT_Whole(Patient,minf,freq)

data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
dirlist=dir(data_dir);
data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
% data_dir2=[data_dir,'\BMode\ROI_Data\Down_Sample\'];
data_dir2=[data_dir,'\BMode\ROI_Data\Cut_axial\'];
S_RF=dir(strcat(data_dir2,'RF_cut_a_*.*'));
CoreNo=size(S_RF,1);

for CoreID=1:CoreNo
    RF_file= strcat(data_dir2,S_RF(CoreID).name);
    load(RF_file);
    d=size(RF_down,1)*size(RF_down,2);
%     RF_reshaped=reshape(RF_down,35840,200);    %256*140=35840
   RF_reshaped=reshape(RF_down,d,200);  
   
    RF_FrRate=freq(Patient);
    
    %%% Resampling 
    if RF_FrRate>minf
        [P,Q] = rat(double(RF_FrRate)/minf);
        xnew = resample(RF_reshaped',P,Q);
        xnew=xnew';
    else
        xnew=RF_reshaped;
    end
    
%     fft_RF1=fft(xnew,200,2);
     fft_RF1=fft(xnew,256,2);
    %%% mean every 6 elements in axial
    fft_RF_resh=reshape(fft_RF1,size(RF_down,1),size(RF_down,2),256);

    N = floor(size(RF_down,1)/6);
%     fft_RF2 = zeros(N, size(RF_down,2), 200); 
    fft_RF2 = zeros(N, size(RF_down,2), 256); 
    k = 1;
    for i = 6:6:size(RF_down,1) %1536
    fft_RF2(k, :, :) = mean(fft_RF_resh(i-5:i, :, :), 1); %Mean along 1st dimension
    k = k+1;
    end

    fft_RF=fft_RF2(:,:,1:32);
    
    %%% saving FFT
    fft_RF_file=[data_dir2,strrep(S_RF(CoreID).name,'RF_cut_a_','FFT')];
    fft_RF_file2=strrep(fft_RF_file,'.dat','.mat');
    save(fft_RF_file2,'fft_RF');
end
end

%% MAsked_FFT FFT*Mask
