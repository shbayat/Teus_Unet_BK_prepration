clear all
%%% saving masked FFT with new naming

%%% load freq info
%%% for P1-110
% [ndata, text, alldata] = xlsread('D:\Sharareh\Prostate_Project\Preparation\Patient_info');
% freq=ndata(1:110,5);

%%% for P1-140
[ndata, text, alldata] = xlsread('D:\Sharareh\Prostate_Project\Preparation\Paitient_info_1_140P');
freq=ndata(1:140,5);
minf=min(freq);

%% 1- Calculate zero padded FFT ---> saves 256x530x32 FFT values
% for Patient=111
%     Patient
% FFT_Whole_Zpad(Patient,minf,freq)
% end

%% 2-Calculate Masked zero padded FFT--> saves 256x530 masks
for Patient=111:140
    Patient
    FFT_masked_zp(Patient)
end


%% Funcitons
function FFT_Whole_Zpad(Patient,minf,freq)

names={'00', '01', '02' ,'03','04','05','06','07','08','09'}; % for 8 and 10 cores
names2={'00', '10', '11' ,'01','02','03','04','05','06','07','08','09'}; % for more than 10
names3={'00', '10','01','02','03','04','05','06','07','08','09'}; % for coreNo==10

data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
dirlist=dir(data_dir);
data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
data_dir2=[data_dir,'\BMode\ROI_Data\Cut_axial\'];
FFT_RF=dir(strcat(data_dir2,'FFTA*.*'));

data_dir3=[data_dir,'\BMode\ROI_Data\Cut_axial\'];
Mask_RF=dir(strcat(data_dir3,'masked1_cut_a_*.mat'));
CoreNo=size(FFT_RF,1);


for CoreID=1:CoreNo
    FFT_file= strcat(data_dir2,FFT_RF(CoreID).name);
    fft=load(FFT_file);
    
    mask_file= strcat(data_dir3,Mask_RF(CoreID).name);
    mask=load(mask_file);
    
    FFT_RF2=fft.fft_RF;
%     masked_RF2=reshape(mask.masked_RF,35840,200);
    
    
%     masekd_FFT=FFT_RF2.*masked_RF2;
    
%% Zero padding

Init=zeros(256,530,32);
Init(:,1:size(FFT_RF2,2),:)=FFT_RF2;
fft_RF=Init;

%% saving zeor-padded FFT
 
if CoreNo<=10
    fft_RF_file=[data_dir2 'FFT_zp_' names{CoreID}];
   
elseif CoreNo==11
   fft_RF_file=[data_dir2 'FFT_zp_' names3{CoreID}];
elseif CoreNo>11
%     fft_RF_file=[data_dir2,strrep(FFT_RF(CoreID).names2,'FFT','FFT_zp_')]; 
    fft_RF_file=[data_dir2 'FFT_zp_' names2{CoreID}];
end
    save(fft_RF_file,'fft_RF');
end    

end


%% MAsked_FFT FFT*Mask
function FFT_masked_zp(Patient)

%% load FFT _ zero padded and cut
data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
dirlist=dir(data_dir);
data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
data_dir2=[data_dir,'\BMode\ROI_Data\Cut_axial\'];
FFT_RF=dir(strcat(data_dir2,'FFT_zp_*.*'));

%% Load cut RF_mask
Mask_RF=dir(strcat(data_dir2,'masked1_cut_a*.mat'));

CoreNo=size(FFT_RF,1);

for CoreID=1:CoreNo
    FFT_file= strcat(data_dir2,FFT_RF(CoreID).name);
    fft=load(FFT_file);
    
if CoreID ==1 || CoreNo==8 || CoreNo==10
    mask_file= strcat(data_dir2,Mask_RF(CoreID).name);

elseif CoreNo==12

        if CoreID>2 && CoreID<=10
            mask_file= strcat(data_dir2,Mask_RF(CoreID+2).name);
            elseif CoreID == 11
            mask_file= strcat(data_dir2,Mask_RF(2).name);
            elseif CoreID == 12
            mask_file= strcat(data_dir2,Mask_RF(3).name);  
        end
end

    mask=load(mask_file);
    
    FFT_RF2=fft.fft_RF;
    masked_RF2=mask.mask_RF_cut;
    
    %% averaging axial maskd RF
    N = floor(size(masked_RF2,1)/6);
    masked_RF3 = zeros(N, size(masked_RF2,2)); 
    k = 1;
    for i = 6:6:size(masked_RF2,1) %1536
    masked_RF3(k, :) = mean(masked_RF2(i-5:i, :), 1); %Mean along 1st dimension
    k = k+1;
    end
   
    %% Zero padding masked RF
    Init=zeros(256,530);
    Init(:,1:size(masked_RF3,2))=masked_RF3;
    masked_RF_zp=Init;
    
%     figure; imagesc(masked_RF_zp); colormap ('gray')
    masked_FFT=FFT_RF2.*masked_RF_zp;
%     figure; imagesc(squeeze(masekd_FFT(:,:,1)));
    
     %%% saving Masked_FFT
    masked_fft_file=strrep(FFT_file,'FFT_zp_','Masked_FFT_');
    save(masked_fft_file,'masked_FFT');

end
end

% bb=masked_FFT/max(masked_FFT(:));
% imshow(abs(bb(:,:,1))*255)