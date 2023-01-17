% Analyse des donnees experience "temps de vie du muon"
% Last release: 09/11/2018 - R. Dallier

runDir='run_20230117/';

totalTime=11; %Temps maximum d'analyse, en microsecondes
% vDyn=10;  %Dynamique de la tension de sortie, en volts
%tacFactor=totalTime/vDyn; %En microsecondes/volt
%tacFactor= 1.0338;
tacFactor_A= 1.3159;  % En microsecondes/volt
tacFactor_B= 0.0811;  % En microsecondes/volt
trgPos=0.25;  %Position relative (sur 1) de l'instant de trigger
dataDir='/home/m2rps/data/ACQ_15/';
currentDir=pwd;
cd([dataDir]);
fileList=dir('*.bin');
for i=1:length(fileList)
    [s,h]=readBFOctave(fileList(i).name);
    bias(i)=mean(filtreOctave(s(:,2),s(:,1),0,1,0,0));
    vOut(i);
end;
tOut=vOut*tacFactor_A+tacFactor_B;
nbClass=10;  % Nombre de classes de la distribution
[tDis,tClass]=hist(tOut,nbClass);
histo=figure;
hist(tOut,nbClass);
set(gca,'fontsize',16,'linewidth',1.5);
xlabel('Decay time (\mus)','interpreter','tex','fontsize',16);
ylabel(['Decay number (per ' num2str(totalTime*1e3/nbClass) ' ns bins)'],'fontsize',16);
legend([num2str(length(tOut)) ' entries'])
leg=get(legend);
debut=1;
fin=length(tDis)-1;
decay = @(x,xdata)x(1)*exp(x(2)*xdata);
x0 = [100,-1];
x = lsqcurvefit(decay,x0,tClass(debut:fin),tDis(debut:fin));
tau=-1/x(2);
figure(histo); hold('on')
plot(tClass(debut:fin),decay(x,tClass(debut:fin)),'r-')
text(1.05*leg.position(1),0.95*leg.position(2),['\tau = ' num2str(tau) ' \mus'],...
   'interpreter','tex','Units',leg.units,'fontsize',14);
cd(currentDir);