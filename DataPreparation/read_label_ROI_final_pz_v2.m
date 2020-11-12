function read_label_ROI_pz(Patient)
    close all; 
    
%     filename = 'dataset'; %% for P:1-91
    filename = 'dataset_1_140'; %% For all P
    Data=xlsread(filename);
   
    PID=Data(:,12);
    CID=Data(:,3);

    d_rate=6; DS_L=2;
    data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
    dirlist=dir(data_dir);
    disp(data_dir)
    data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
    data_dir2=strcat(data_dir,'BMode\ROI_Data\TestImages\');
    RF_ROI=dir(strcat(data_dir2,'RFROI_mask_*.bmp'))
    flag=0;    
    CoreNo=size(RF_ROI,1);
    if CoreNo==0
        RF_ROI=dir(strcat(data_dir2,'RFROI_mask_*.jpg'));
        CoreNo=size(RF_ROI,1);
        flag=1;
    end
    save_dir=[data_dir,'\BMode\ROI_Data\Cut_axial\Labels\'];
    
%     S_mask=dir(strcat(data_dir2,'PR_mask_A*.*'));
    
    if ~isfolder(save_dir)
        mkdir(save_dir)
    end
    
    for CoreID=1:CoreNo
        CoreID
        %%% read masked_ROI
        ROI_file= strcat(data_dir2,RF_ROI(CoreID).name);
        ROI_mask=imread(ROI_file);

 %% averaging axial maskd RF
    ROI_mask=ROI_mask(1:1536,:);
    N = floor(size(ROI_mask,1)/6);
    masked_RF3 = zeros(N, size(ROI_mask,2)); 
    k = 1;
    for i = 6:6:size(ROI_mask,1) %1536
    masked_RF3(k, :) = mean(ROI_mask(i-5:i, :), 1); %Mean along 1st dimension
    k = k+1;
    end
   
    %% Zero padding masked RF
    Init=zeros(256,530);
    Init(:,1:size(masked_RF3,2))=masked_RF3;
    masked_RF_zp=Init;
       
        
%         ROI_mask_c=ROI_mask(1:1536,:,:);
% %         rf_AllFrames_c=rf_AllFrames(1:(size(rf_AllFrames,1)/2),:,:);
% %         figure(2);imagesc(ROI_mask_c);
%         ROI_mask_c_res=imresize(ROI_mask_c,[256,256]);
%         ROI_mask_down = ROI_mask_c_res;

     ROI_mask_down =masked_RF_zp;

     
        %%% label finding
%         

     fname=dir(strcat(data_dir2,'RFROI_test_*.bmp'));   
     core=str2double(fname(CoreID).name(12));
%%%% for saving     
        names=[0,1,2,3,4,5,6,7,8,9]; % for 8 - 9 cores
        names2=[0,1,10,2,3,4,5,6,7,8,9]; % for coreNo==11
        names3=[0,1,10,11,2,3,4,5,6,7,8,9]; % for more than 12
       
        if CoreNo<=10
            core_save=names(CoreID);
        elseif CoreNo==11
            core_save=names2(CoreID);
        elseif CoreNo>=11
            core_save=names3(CoreID);
        end
        
        ind=PID==Patient & CID==core+1;
        [row,~]=find(ind==1);
        label=Data(row,5);
        
% % %    all black for benigns
%       if label==0
%             ROI_mask_down_2 =zeros(size(ROI_mask_down,1),size(ROI_mask_down,2));
%             ROI_mask_down=ROI_mask_down_2;
%         end
% %%%   Inverse to cancer
    ROI_mask_down_2=zeros(size(ROI_mask_down,1),size(ROI_mask_down,2),2);
        if label==1
            ROI_mask_down_2(:,:,1)=zeros(size(ROI_mask_down,1),size(ROI_mask_down,2));
            ROI_mask_down_2(:,:,2)=ROI_mask_down;
%             imshow(squeeze(ROI_mask_down_2(:,:,1)));title('label=1')
        elseif label==0    
            ROI_mask_down_2(:,:,1)=ROI_mask_down;
            ROI_mask_down_2(:,:,2)=zeros(size(ROI_mask_down,1),size(ROI_mask_down,2));
%             imshow(squeeze(ROI_mask_down_2(:,:,1)));title('label=0')
        end
        
        %%% saving DS RF_ROI mask
        if flag==0
            ROI_mask_DS_file=[save_dir,strrep(RF_ROI(CoreID).name,'.bmp','.mat')];
%             ROI_mask_DS_file_2=[save_dir,strrep(RF_ROI(CoreID).name,'.bmp','.mat')];
        else
            ROI_mask_DS_file=[save_dir,strrep(RF_ROI(CoreID).name,'.jpg','.mat')];
%             ROI_mask_DS_file_2=[save_dir,strrep(RF_ROI(CoreID).name,'.jpg','.mat')];
        end
%         save(ROI_mask_DS_file,'ROI_mask_down');
%         ROI_mask_DS_file2=strrep(ROI_mask_DS_file,'.mat','.bmp');
%         imwrite(ROI_mask_down,ROI_mask_DS_file2,'bmp');
%%% for new savings
        save(ROI_mask_DS_file,'ROI_mask_down_2');
        ROI_mask_DS_file=strrep(ROI_mask_DS_file,'.mat','.bmp');
        imwrite(squeeze(ROI_mask_down_2(:,:,1)),ROI_mask_DS_file,'bmp');

    end
end
        

   