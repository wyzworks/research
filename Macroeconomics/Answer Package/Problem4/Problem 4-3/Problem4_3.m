sheet = 1;

cor = xlsread('4_3 logA_t.xlsx',sheet);

plot(cor)

cor_cycle=hpfiltering(cor');
cor_trend=cor-cor_cycle;

figure;
% Create a vector from 1947 Q1 to 2024 Q1 with a step of 0.25
years = 1947.0:0.25:2024.0;
plot(years, cor_trend); hold on ; 
plot(years, cor);
title('Hp filtering')
legend('Trend','Total Factor Productivity')
xlabel('Year')
ylabel('Total Factor Productivity')