clear;close all;clc;
data = csvread('price_fairdataset.csv');
X = data(2:end,1:end);
#y = data(2:end,1);
figure;
hold on;
hist(X(:,1),100,"facecolor", "r", "edgecolor", "b");
xlabel('Font Size');
ylabel('Number of value');
title('Number of Font-Size value in dataset');

figure;
hold on;
title('Font-Weight');
hist(X(:,2),100,"facecolor", "g", "edgecolor", "b");
xlabel('Weight');
ylabel('Number of Font-Weight value in dataset');
##

##
figure;
hold on;
title('Line-height');
hist(X(:,3),100,"facecolor", "b", "edgecolor", "b");
xlabel('Line height');
ylabel('Number of Line-height value in dataset');
