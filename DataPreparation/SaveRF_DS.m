clc
clear all
close all

for Patient=110
    Patient
Down_sample(Patient)
end


% 
% function [width,height]=SaveRF(Patient)
% 
% data_dir=strcat('z:\\shared\images\ProstateVGH-2\Data\Patient',num2str(Patient));
% dirlist=dir(data_dir);
% data_dir = strcat(data_dir,'\',dirlist(3).name,'\');
% S = dir(strcat(data_dir,'IQ*.*'));
% CoreNo=size(S,1);
% for i=1:CoreNo
%         oldfile= strcat(data_dir,S(i).name);
%         newIQfile= strrep(oldfile,'IQ_','RF_');
%            
% 
%         %Find RF Dimension
%         fid_iq = fopen(oldfile,'rt');
%         headerstr=fgetl(fid_iq);
%         fclose(fid_iq);
%         
%         iq =   regexp(headerstr,',');
%         dims(1) = str2num(headerstr(1:iq(1)));% 496;% %hight (h)
%         iq_height=str2num(headerstr(iq(1):iq(2)));
%         if iq_height>999
%             start_ch=12;
%         else
%             start_ch=11;
%         end
%         dims(2) = 2*iq_height;%884;% %width (w)
%                  
% 
%         %read IQ data
%         fid_iq = fopen(oldfile);
%         iq =   fread(fid_iq,inf,'uint8');
%         fclose(fid_iq);
%         
%         
%         iq_noheader = iq(start_ch:end,:); %take out the header - the first 11 chars are the W and H of the image and size
%         [r1,r2]= size(iq_noheader);
%          
% 
%         l =length(iq_noheader);
%         dims(3) = l/(dims(1)*dims(2)*2); %Number of the frames (N)
%         count=1;
%         IQ_int16=zeros(l/2,1);
%         for j = 1:2:l
%             temp = uint8(iq_noheader(j:(j+1))');
%             IQ_int16(count) = typecast(temp , 'int16');%fliplr
%             count=count+1;
%         end
% 
%         %IQ -> RF
%         fs=30000000; %RF frequency
%         
%         RF= zeros(l/2,r2);
%         
%         RF(:,r2) = iq2rf(double(IQ_int16), 2, fs/4, fs); %convert IQ to RF
%         
%         % reshape into a matrix with shape {w,h,N}
%         frames = reshape(RF,[dims(2),dims(1),dims(3)]);
% %        figure,imagesc(log10(1+abs(squeeze(frames(:,:,1))))),colormap('gray')
%         RFmatfile= strrep(newIQfile,'.dat','.mat');
% %         save(RFmatfile,'frames')
%         fid_rf = fopen(newIQfile,'wb');
%         fwrite(fid_rf,RF,'int16');
%         fclose(fid_rf);
% end
% width=int16(dims(2));
% height=int16(dims(1));
% 
% 
% 
% 
