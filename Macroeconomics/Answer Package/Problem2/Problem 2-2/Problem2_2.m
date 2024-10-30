sheet = 1;

cor = xlsread('Problem 2-2. Capital-ouput ratio (1929-2022).xlsx',sheet); % cor=capital-output ratio

plot(cor)

cor_cycle=hpfiltering(cor');
cor_trend=cor-cor_cycle;

figure;
years = 1929:2022;
plot(years, cor_trend); hold on ; 
plot(years, cor);
title('Hp filtering')
legend('Trend','Capital-output ratio')
xlabel('Year')
ylabel('Capital-output ratio')


