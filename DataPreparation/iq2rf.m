%IQ2RF Convert IQ data to RF data. 
%
%USAGE : [rf] = iq2rf(iq, upfactor, fmix, fs)
%
%INPUTS:  iq - I&Q signal. One column per channel.
%              Can be either complex or real. If complex, then 
%                        iq = I + j*Q
%              If real, then the order is:
%                        [I1, Q1, I2, Q2, ...]'
%
%         upfactor - Factor to upscale. In ProFocus, this should be 2
%         fmix - Mixing frequency. In ProFocus this is fs/4
%         fs - Sampling frequency. Can be obtained from BFRcvParams in an 
%              use case
%
%OUTPUT: rf - RF data. Real numbers (not complex)
%
%CREATED: 20 Mar 2009, Svetoslav Nikolov
%
%


function [rf] = iq2rf(iq, upfactor, fmix, fs)

j=sqrt(-1);

if(sum(imag(iq))==0)  % Assuming real data in the format I1,Q1,I2,Q2 ...
    iq = double(iq(1:2:end-1,:)) + j*double(iq(2:2:end,:)); 
end

no_samples = upfactor*size(iq,1);

t = [0:no_samples-1]'/fs;
e = exp(j*2*pi*fmix*t);


for i = 1:size(iq,2)
    rf(1:no_samples,i) = real(interp(iq(:,i),upfactor).*e);
end

%    fmix= fs/ 4   and upfactor=2








