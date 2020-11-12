%%% Calc AUC

% An example for binary classification
TP =19;
TN=23;
FN=5;
FP=9;
TPR= TP/(TP+FN);
FPR = FP/(FP+TN);
X = [0;TPR;1];
Y = [0;FPR;1];
AUC = trapz(Y,X) % AUC = 0.
x1=linspace(0,TPR,10);
x2=linspace(0,FPR,10);
plot(x1,x2)
