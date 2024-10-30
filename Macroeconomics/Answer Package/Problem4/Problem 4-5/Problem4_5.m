sheet = 1;

corY = xlsread('4-5 logY_t.xlsx',sheet);
corA = xlsread('4_5 logA_t.xlsx',sheet);

plot(corY)

corY_cycle=hpfiltering(corY');
corY_trend=corY-corY_cycle;

corA_cycle=hpfiltering(corA');
corA_trend=corA-corA_cycle;

figure;
% Create a vector from 1947 Q1 to 2024 Q1 with a step of 0.25
years = 1947.0:0.25:2024.0;
plot(years, corY_trend); hold on ; 
plot(years, corY);
title('Hp filtering', 'FontSize', 20)
legend('Trend','log Y_t', 'FontSize', 20)
xlabel('Year', 'FontSize', 20)
ylabel('Growth in output', 'FontSize', 20)

figure;
plot(years, corA_cycle);
title('Business cycle component', 'FontSize', 20)
xlabel('Year', 'FontSize', 20)
ylabel('Business cycle component of log A_t', 'FontSize', 20)

figure;
plot(years, corY_cycle);
title('Business cycle component', 'FontSize', 20)
xlabel('Year', 'FontSize', 20)
ylabel('Business cycle component of log Y_t', 'FontSize', 20)