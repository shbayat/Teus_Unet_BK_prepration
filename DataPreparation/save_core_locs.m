%%% reads all the core locs and saves the core locs for p1-90 and 111-140
clear  all

cores1_90=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\CoreLocs_P1_90.mat');
cores111_140=load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\CoreLocs_P111_140.mat');


core_locs_all=[cores1_90.CoreLoc;cores111_140.CoreLoc];
id_all=[cores1_90.id';cores111_140.id'];

load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\Lable_IDs_Highinv_balanced_P1_90_111_140_zp.mat');

Cores_train=zeros(length(idcore_train),8);


    for i=1:length(idcore_train)
        for j=1:length(id_all)
            if idcore_train(i)==id_all(j)
                Cores_train(i,:)=core_locs_all(j,:);
            end
        end
    end

% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\Core_locs_train_P1_90_111_140.mat','Cores_train','idcore_train')
Cores_train_f=zeros(104,256,528,8);
for i=1:length(Cores_train)
    for j=1:size(Cores_train,2)
        if Cores_train(i,j)==0
        Cores_train_f(i,:,:,j)=zeros(256,528);
        else
        Cores_train_f(i,:,:,j)=ones(256,528);
        end
    end
end

% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\Core_locs_train_f_P1_90_111_140.mat','Cores_train_f','idcore_train')
% 


%%% val

Cores_val=zeros(length(idcore_val),8);


    for i=1:length(idcore_val)
        for j=1:length(id_all)
            if idcore_val(i)==id_all(j)
                Cores_val(i,:)=core_locs_all(j,:);
            end
        end
    end

% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\Core_locs_val_P1_90_111_140.mat','Cores_val','idcore_val')

Cores_val_f=zeros(length(idcore_val),256,528,8);
for i=1:length(Cores_val)
    for j=1:size(Cores_val,2)
        if Cores_val(i,j)==0
        Cores_val_f(i,:,:,j)=zeros(256,528);
        else
        Cores_val_f(i,:,:,j)=ones(256,528);
        end
    end
end

% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\Core_locs_val_f_P1_90_111_140.mat','Cores_val_f','idcore_val')


%% test

idcore_test_original=[997,  999, 1000, 1001, 1002, 1003, 1005,  907,  906,  908,  909,...
            910,  998,  911,  912,  913,  914,  916,  917,  918,  919,  922,...
            927,  928,  929,  930,  941,  942,  943,  945,  946,  947,  948,...
            949,  950,  952,  953,  954,  956,  957,  959,  961,  973,  975,...
             976,  978,  979,  980,  981,  982,  983,  984,  986,  988,  989,...
            990,  991,  992,  993,  995,  996, 1011, 1089, 1091, 1092, 1054,...
            1008, 1009, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1037,...
            1039, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1071, 1072, 1073,...
            1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084,...
            1087, 1090, 1094, 1095, 1096, 1098];
        
idcore_test=zeros(1,105);        
load('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\CoreLocs_P91_110.mat')

[idx_cores,idxA] = find(bsxfun(@eq,idcore_test_original,id.'));

for i=1:numel(idxA)
    idcore_test(i)=id(idx_cores(i));
    CoreLoc_test(i,:)=CoreLoc(idx_cores(i),:);
end


Cores_test_f=zeros(length(idcore_test),256,528,8);
for i=1:length(CoreLoc_test)
    for j=1:size(CoreLoc_test,2)
        if CoreLoc_test(i,j)==0
        Cores_test_f(i,:,:,j)=zeros(256,528);
        else
        Cores_test_f(i,:,:,j)=ones(256,528);
        end
    end
end

% save('Z:\shared\images\ProstateVGH-2\Data\Dataset\InProstate\Zero-pad\Core_locs_test_f_P1_91_110.mat','Cores_test_f','idcore_test')
