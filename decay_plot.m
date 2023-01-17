% Analyse des donnees experience "temps de vie du muon"
% Last release: 17/01/2023 - A. AMY


clear all;

totalTime=11; %Temps maximum d'analyse, en microsecondes

% vDyn=10;  %Dynamique de la tension de sortie, en volts
tacFactor_A= 1.;  % En microsecondes/volt
tacFactor_B= 0.;  % En microsecondes/volt

dataDir='/home/antoine/Documents/LiME/';
cd([dataDir]);

% Open the file for reading
fid = fopen("run_20230117.txt", "r");
vOut = [];
% Read data from the file
while (!feof(fid))
    value = fscanf(fid, "%f", 1);
    vOut = [vOut, value];
endwhile

% Close the file
fclose(fid);

tOut=vOut*tacFactor_A+tacFactor_B;
nbClass=19;  % Nombre de classes de la distribution
[tDis,tClass]=hist(tOut,nbClass);
histo=figure;
hist(tOut,nbClass);
set(gca,'fontsize',16,'linewidth',1.5);
xlabel('Decay time (\mus)','interpreter','tex','fontsize',16);
ylabel(['Decay number (per ' num2str(totalTime*1e3/nbClass) ' ns bins)'],'fontsize',16);
legend([num2str(length(tOut)) ' entries'])
leg=get(legend);
debut=2;
fin=length(tDis)-1;
decay = @(x,xdata)x(1)*exp(x(2)*xdata);
x0 = [100,-1];
x = lsqcurvefit(decay,x0,tClass(debut:fin),tDis(debut:fin));
tau=-1/x(2);
figure(histo); hold('on')
plot(tClass(debut:fin),decay(x,tClass(debut:fin)),'r-')
text(1.05*leg.position(1),0.95*leg.position(2),['\tau = ' num2str(tau) ' \mus'],...
   'interpreter','tex','Units',leg.units,'fontsize',14)