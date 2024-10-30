sheet = 1;

cor = xlsread('Problem 3-2. (Data) Total Factor Productivity.xlsx', sheet); 
plot(cor)

cor_cycle=hpfiltq(cor');
cor_trend=cor-cor_cycle;

figure;
years = 1948:2022
plot(years, cor_trend); hold on ; 
plot(years, cor);
title('Hp filtering')
legend('Trend','Capital-output ratio')
xlabel('Year')
ylabel('Capital-output ratio')


