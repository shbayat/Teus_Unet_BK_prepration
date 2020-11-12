%% reads AE log files and plots
% data_path='C:\Users\Sharareh\Desktop\train';
close all
data_path='C:\Users\Sharareh\Desktop\trained_models';
dirlist=dir (data_path);
for i=170:190
data_dir = strcat(data_path,'\',dirlist(i).name,'\')
logfile=readtable([data_dir 'log.csv']);


train_loss=logfile(:,2);
Epochs=logfile(1,:);
figure;plot(logfile.loss)
hold on
plot(logfile.val_loss);%title(["AE loss -" num2str(dirlist(i).name)])
xlabel("Epoch"); ylabel("Loss");legend ('Train','Val')
end