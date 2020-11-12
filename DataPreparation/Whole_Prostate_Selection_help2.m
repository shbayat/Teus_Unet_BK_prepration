clc
clear all
close all

for Patient=115
Whole_Prostate_Selection(Patient)
end

function Whole_Prostate_Selection(Patient)

    data_dir=strcat('\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
    dirlist=dir(data_dir);
    disp(data_dir)
    data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
%      data_dir = '\\smbhome\rcl\shared\images\ProstateVGH-2\Data\Patient76\\2019-10-9-13-57';
    S_IQ=dir(strcat(data_dir,'IQ*.*'));
    CoreNo=size(S_IQ,1);
    save_dir=[data_dir,'\BMode\ROI_Data\']
    
    if ~isfolder(save_dir)
        mkdir(save_dir)
    end
    save_dir=[data_dir,'\BMode\ROI_Data\WholeProstate\'];
    if ~isfolder(save_dir)
        mkdir(save_dir)
    end
    
    for CoreID=1:CoreNo
        %Find RF Dimension
        IQ_file= strcat(data_dir,S_IQ(CoreID).name);
        fid_iq = fopen(IQ_file,'rt');
        headerstr=fgetl(fid_iq);
        fclose(fid_iq);
        
        iq =   regexp(headerstr,',');
        dims(1) = str2num(headerstr(1:iq(1)));% 496;% %hight (h)
        iq_height=str2num(headerstr(iq(1):iq(2)));
        dims(2) = 2*iq_height;%884;% %width (w)

        RF_file= strrep(IQ_file,'IQ','RF');%strcat(data_dir,S(CoreID).name);
        fid_iq = fopen(RF_file);
        RF_Data =   fread(fid_iq,inf,'int16');
        fclose(fid_iq);
        
        rf_AllFrames=reshape(RF_Data,[dims(2) dims(1) 200]);
        s = size(rf_AllFrames);
        h=imagesc(log10(1+abs(squeeze(rf_AllFrames(:,:,1)))));colormap('gray');
        title([num2str(Patient),' +++  ',num2str(CoreID)])
       
        finished = 'NO';
        i = 1;
        while strcmpi(finished,'NO')
          hFH(i) = imfreehand();
          finished = questdlg('Finished?', ...
              'confirmation', ...
              'YES', 'NO', 'UNDO', 'NO');
          if strcmpi(finished, 'UNDO')
              delete(hFH(i))
              finished = 'NO';
          else
              mask{i}  = hFH(i).createMask(h);
              i = i + 1;
          end
        end
        xy_mask = cell2mat(mask);
        indx=find(xy_mask);
        RF_Prostate=rf_AllFrames.*xy_mask;
        h=imagesc(log10(1+abs(squeeze(RF_Prostate(:,:,50)))));colormap('gray');
        
        RF_PR_file=[save_dir,strrep(S_IQ(CoreID).name,'IQ','PR_img')];
        RF_PR_file=strrep(RF_PR_file,'.dat','.mat');
        save(RF_PR_file,'RF_Prostate');
        
        RF_Prostate_2D=reshape(RF_Prostate,[dims(1)*dims(2),200]);
        RF_PR_2D=RF_Prostate_2D(indx,:);
%         test=zeros([dims(1)*dims(2),200]);
%         test(indx,:)=RF_PR_2D;
%         tes_img=reshape(test,[dims(2) dims(1) 200]);
%         imagesc(log10(1+abs(squeeze(tes_img(:,:,50)))));colormap('gray');
%         ind=[indx_i ,indx_j ,[1:200]];
%         for k=1:size(indx_i,1)
%             RF_PR_2D(k,:)=rf_AllFrames(indx_i(k),indx_j(k),:);
%         end
        
        RF_PR_file=[save_dir,strrep(S_IQ(CoreID).name,'IQ','PR_2D')];
        RF_PR_file=strrep(RF_PR_file,'.dat','.mat');
        save(RF_PR_file,'RF_PR_2D')
        
        RF_mask_file=[save_dir,strrep(S_IQ(CoreID).name,'IQ','PR_mask')];
        RF_mask_file=strrep(RF_mask_file,'.dat','.bmp');
        imwrite(xy_mask,RF_mask_file,'jpg')
%         fid_rf = fopen(RF_PR_file,'wb');
%         fwrite(fid_rf,RF_Prostate,'int16');
%         fclose(fid_rf);
        clearvars -except Patient data_dir S S_IQ CoreNo save_dir
        close all
    end   
end
   