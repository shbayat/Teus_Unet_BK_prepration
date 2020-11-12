function Down_sample(Patient)
    close all; 
    d_rate=6; DS_L=2;
    data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
    dirlist=dir(data_dir);
    disp(data_dir)
    data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
    data_dir2=strcat(data_dir,'\Bmode\ROI_Data\');
    data_dir3=strcat(data_dir,'\Bmode\ROI_Data\WholeProstate\');
%      data_dir = '\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient76\\2019-10-9-13-57';
%     S_RF_ROI=dir(strcat(data_dir,'\Bmode\ROI_Data\RF_ROI_Data_*.*'));
%     S_IQ=dir(strcat(data_dir,'IQ*.*'));
    S_IQ=dir(strcat(data_dir2,'RF_ROI_Data_*.*'));
   %%% sorting file names
%    S_IQ1=dir(strcat(data_dir,'IQ*.*'));
%     C = {S_IQ1.name};
%     if size(C,2)<=8
%         S_IQ=sort(C);
%     elseif 10<=size(C,2)<=11
%         D{1}=C{1}
%         for j=3:11
%             D{j-1}=C{j}
%         end
%         D{11}=C{2}
%         S_IQ=D';
%     end
%     
        
    CoreNo=size(S_IQ,1);
    save_dir=[data_dir,'\BMode\ROI_Data\Down_Sample\'];
    
    S_mask=dir(strcat(data_dir3,'PR_mask_A*.*'));
    
    if ~isfolder(save_dir)
        mkdir(save_dir)
    end
    
    for CoreID=1:CoreNo
        CoreID
        %%% read IQ
        IQ_file= strcat(data_dir,S_IQ(CoreID).name);
        fid_iq = fopen(IQ_file,'rt');
        headerstr=fgetl(fid_iq);
        fclose(fid_iq);
        
        iq =   regexp(headerstr,',');
        dims(1) = str2num(headerstr(1:iq(1)));% 496;% %hight (h)
        iq_height=str2num(headerstr(iq(1):iq(2)));
        dims(2) = 2*iq_height;%884;% %width (w)
        
        %%% read RF
        RF_file= strrep(IQ_file,'IQ','RF');%strcat(data_dir,S(CoreID).name);
        fid_iq = fopen(RF_file);
        RF_Data =   fread(fid_iq,inf,'int16');
        fclose(fid_iq);
        %Find RF Dimension and downsample
        rf_AllFrames=reshape(RF_Data,[dims(2) dims(1) 200]);
        s = size(rf_AllFrames);
%         figure(1);imagesc(log10(1+abs(squeeze(rf_AllFrames(:,:,1)))));colormap('gray');
        
        if size(rf_AllFrames,2)==282 %reach 280
            left_c=2;right_c=1;
        elseif size(rf_AllFrames,2)==392 %reach 280
            left_c=57;right_c=56;
        elseif size(rf_AllFrames,2)==372 %reach 280
            left_c=47;right_c=46;
        elseif size(rf_AllFrames,2)==414 %reach 280
            left_c=68;right_c=67; 
        elseif size(rf_AllFrames,2)==438 %reach 420
            left_c=10;right_c=9; DS_L=3;
        elseif size(rf_AllFrames,2)==496 %reach 420
            left_c=39;right_c=38; DS_L=3;
        elseif size(rf_AllFrames,2)==466 %reach 420
            left_c=24;right_c=23; DS_L=3;
        elseif size(rf_AllFrames,2)==530 %reach 420
            left_c=56;right_c=55; DS_L=3; 
%             left_c=150;right_c=99;
        elseif size(rf_AllFrames,2)==560 % reach 420
            left_c=71;right_c=70; DS_L=3;
        end
%         rf_AllFrames_c1=rf_AllFrames(1:1536,:,:);
        rf_AllFrames_c=rf_AllFrames(1:1536,left_c:(end-right_c),:);
%         rf_AllFrames_c=rf_AllFrames(1:(size(rf_AllFrames,1)/2),:,:);
%         figure(2);imagesc(log10(1+abs(squeeze(rf_AllFrames_c1(:,:,1)))));colormap('gray');
%         figure(3);imagesc(log10(1+abs(squeeze(rf_AllFrames_c(:,:,1)))));colormap('gray');
        RF_down = rf_AllFrames_c(1:d_rate:end,1:DS_L:end,:);
%         figure(4);imagesc(log10(1+abs(squeeze(RF_down(:,:,1)))));colormap('gray');
        
        %%% read mask
        mask_file= strcat(data_dir3,S_mask(CoreID).name);
        mask=imread(mask_file);
%         figure(5);imagesc(mask(:,:));colormap('gray');
        mask_c= mask(1:1536,left_c:(end-right_c));
%         figure(6);imagesc(mask_c(:,:));colormap('gray');
        mask_down= mask_c(1:d_rate:end,1:DS_L:end,:);
%         figure(7);imagesc(mask_down(:,:));colormap('gray');
        for j=1:200
            masked_RF(:,:,j)= double(mask_down).*squeeze(RF_down(:,:,j));
        end
%         figure(8);imagesc(log10(1+abs(squeeze(masked_RF(:,:,1)))));colormap('gray');
        
        %%% saving DS RF
        RF_DSfile=[save_dir,strrep(S_IQ(CoreID).name,'IQ','RF_DS')];
        RF_DSfile2=strrep(RF_DSfile,'.dat','.mat');
        save(RF_DSfile2,'RF_down');
        
        %%% saving DS mask
        masked_DSfile=[save_dir,strrep(S_IQ(CoreID).name,'IQ','masked_DS')];
        masked_DSfile2=strrep(masked_DSfile,'.dat','.mat');
        save(masked_DSfile2,'masked_RF');
        masked_DSfile3=strrep(masked_DSfile,'.dat','.jpg');
        imwrite(squeeze(masked_RF(:,:,1)),masked_DSfile3,'jpg')
    end
end
        

   