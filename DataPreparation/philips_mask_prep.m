
%% Read npy mask files 
clc
clear all

%% Read excel file
path='Z:\workspace\Sharareh\Philips_local\data\sheets\';
filename = 'PatientsInfo_All'; 
Data=xlsread([path filename]);
[~ , Fnames] =xlsread('Z:\workspace\Sharareh\Philips_local\data\sheets\PatientsInfo_All' ,'Sheet1','C2:C256');


PID=Data(:,1);
Label=Data(:,3);

%% read mask    
 data_dir='Z:\workspace\Sharareh\Philips_local\data\masks\';
 dirlist=dir(data_dir);
 save_dir='Z:\workspace\Sharareh\Philips_local\data\masks_m\';
 ROI_mask_down_2=zeros(256,256,2);
  
 for i=1:length(dirlist)
     data_temp = strcat(data_dir,dirlist(2+i).name); %mask names

     fname=dirlist(2+i).name;
     temp1 = readNPY( data_temp);
     temp1=temp1(1,:,:);
     temp=reshape(temp1,256,256,1);


     mask_file_name=strrep(fname,'_ROImask.npy','');
    [idx,~]=find(strcmp(Fnames,mask_file_name));
     
    label=Label(idx);
     if label==1
            ROI_mask_down_2(:,:,1)=zeros(256,256);
            ROI_mask_down_2(:,:,2)=temp;

    elseif label==0    
            ROI_mask_down_2(:,:,1)=temp;
            ROI_mask_down_2(:,:,2)=zeros(256,256);
     end
     ROI_mask_file=[save_dir,strrep(fname,'.npy','.mat')];
     save(ROI_mask_file,'ROI_mask_down_2');

 end