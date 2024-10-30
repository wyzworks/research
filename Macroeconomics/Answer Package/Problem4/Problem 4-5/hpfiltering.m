function [xhp]=hpfiltq(xxx)
% If x is a column vector of length LENGTH
% xtr=HP_mat\x; delivers the HP-trend and
% xhp=x-xtr; delivers the HP-filtered series
% This program computes HP_mat, given the length of
% some given column vector x
% I will use HP_LAMBDA = 100, unless you assign a different value beforehand.
    

LENGTH = max(size(xxx));

HP_LAMBDA = 1600;

% The following piece is due to Gerard A. Pfann

   HPmat = [1+HP_LAMBDA, -2*HP_LAMBDA, HP_LAMBDA,              zeros(1,LENGTH-3);
             -2*HP_LAMBDA,1+5*HP_LAMBDA,-4*HP_LAMBDA,HP_LAMBDA, zeros(1,LENGTH-4);
                           zeros(LENGTH-4,LENGTH);
              zeros(1,LENGTH-4),HP_LAMBDA,-4*HP_LAMBDA,1+5*HP_LAMBDA,-2*HP_LAMBDA;     
              zeros(1,LENGTH-3),          HP_LAMBDA,   -2*HP_LAMBDA, 1+HP_LAMBDA  ];
   for iiiii=3:LENGTH-2;
     HPmat(iiiii,iiiii-2)=HP_LAMBDA;
     HPmat(iiiii,iiiii-1)=-4*HP_LAMBDA;
     HPmat(iiiii,iiiii)=1+6*HP_LAMBDA;
     HPmat(iiiii,iiiii+1)=-4*HP_LAMBDA;
     HPmat(iiiii,iiiii+2)=HP_LAMBDA;
   end;
xtr=HPmat \ xxx';
xhp=xxx'-xtr; 

      
      
      