%% Closing figures, clearing command window, and clearing variables
clear all
close all
clc

dir = '/Users/allesgut/Desktop/Main/1.courses/2019-1/Eng_Math/Project/';  % directory

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Training - preprocess and train

%Read train data for type1,2,3, and add a column - Var1 (to be changed
%to 'cell_type')
type1Train = readtable(strcat(dir,'train/type1.csv'));
len = size(type1Train,1);
category = cell(len,1);
category(:) = {'type1'};
type1Train = [category, type1Train];

type2Train = readtable(strcat(dir,'train/type2.csv'));
category(:) = {'type2'};
type2Train = [category, type2Train];

type3Train = readtable(strcat(dir,'train/type3.csv'));
category(:) = {'type3'};
type3Train = [category, type3Train];


% create one big table consisting of [type1Train;type2Train;type3Train]
trainData = [type1Train;type2Train;type3Train];
clear type1Train; clear type2Train; clear type3Train; clear category; clear len;
trainData.Properties.VariableNames{'Var1'} = 'cell_type'; 

% throw away variables not to be used
trainData(:,'neuron_name') = [];
trainData(:,'neuron_id') = [];


% Method of Imputation : mean substitution
nrow = size(trainData,1);
ncol = size(trainData,2);
for i=2:ncol
    arr  = table2array(trainData(:,i));
    nanArr = isnan(arr);  %indeces for instances with NaN values
    existsNAN = sum(nanArr) > 0;
    if existsNAN
        arr(nanArr) = nanmean(arr);  %imputation with mean values
        trainData(:,i) = array2table(arr);  %update table trainData
    end
end


y = categorical(table2array(trainData(:,'cell_type')));  %extract y
data = trainData{:,2:end};  %'X' for training
dataNorm = normalize(data);  %normalize data

% discard obviously useless variables (NaN after normalization probably
% means that the standard deviation is 0, meaning it is useless)
dataNorm(:,19) = [];  %'nstems' is 1 for all instances
dataNorm(:,8) = [];  %'diameter' is 1 for all instances

% run pca to fully avoid collinearity
[wcoeff,score,latent,~,explained] = pca(dataNorm);  % take the first 16 because the last 3 are useless
refinedData = score(:, 1:16);

% plots to have a rough understanding of what the training data looks like
% PC plot
figure(1);
gscatter(score(:,2),score(:,3),y);
title('Training Data PC1 and PC2 plot'); 
xlabel('PC1');
ylabel('PC2');
% Looking at the plot, it seems like analyzing the data won't be too easy


% Train using multinomial logistic regression
[B,dev,stats] = mnrfit(refinedData, y);

%% Training - train data performance
trainNrow = size(dataNorm,1);
pihat = zeros(trainNrow,3);  % pihat(i,j) : probability of instance i being of type j
for i = 1:trainNrow
    scorex = score(i,1:16);
    pihat(i,:) = mnrval(B,scorex);
end
maxArr = max(pihat,[],2);

class = pihat(:,:) == maxArr;
correctCnt = 0;
for i = 1:trainNrow
    if ((y(i)=='type1') && class(i,1)==1) || ((y(i)=='type2') && class(i,2)==1)...
            || ((y(i)=='type3') && class(i,3)==1)
        correctCnt = correctCnt + 1;
    end
end
wrongCnt = trainNrow - correctCnt;
fprintf('---With Training Data in the model, we have---\n');
fprintf('%d out of %d correctly classified\nRate : %f\n', correctCnt, trainNrow, correctCnt/trainNrow);
fprintf('%d out of %d wrongly classified\nRate : %f\n\n', wrongCnt, trainNrow, wrongCnt/trainNrow);


% We can see 4155 out of 7083 were classified correctly using the training
% data. Accuracy = 0.586616.
% Although it is not very good, it is still better than chance (1/3 = 0.3333)
% So we can see that our model learns from our data.
% Now we go into testing with data not used for training.


%%%%%%%%%%%%%%%%%%%%%%%
%% Testing - Preprocess

%Read test data for type1,2,3, and add a column - Var1 (to be changed
%to 'cell_type')
type1Test = readtable(strcat(dir,'test/type1.csv'));
len = size(type1Test,1);
category = cell(len,1);
category(:) = {'type1'};
type1Test = [category, type1Test];

type2Test = readtable(strcat(dir,'test/type2.csv'));
category(:) = {'type2'};
type2Test = [category, type2Test];

type3Test = readtable(strcat(dir,'test/type3.csv'));
category(:) = {'type3'};
type3Test = [category, type3Test];

testData = [type1Test;type2Test;type3Test];
clear type1Test; clear type2Test; clear type3Test; clear category; clear len;
testData.Properties.VariableNames{'Var1'} = 'cell_type';


% throw away variables not to be used
testData(:,'neuron_name') = [];
testData(:,'neuron_id') = [];


% Method of Imputation : mean substitution
nrow = size(testData,1);
ncol = size(testData,2);
for i=2:ncol
    arr  = table2array(testData(:,i));
    nanArr = isnan(arr);  %indeces for instances with NaN values
    existsNAN = sum(nanArr) > 0;
    if existsNAN
        arr(nanArr) = nanmean(arr);  %imputation with mean values
        testData(:,i) = array2table(arr);  %update table trainData
    end
end


y = categorical(table2array(testData(:,'cell_type')));  %extract y
data = testData{:,2:end};  %'X' for testing
dataNorm = normalize(data);  %normalize data

% discard obviously useless variables (NaN after normalization probably
% means that the standard deviation is 0, meaning it is useless)
dataNorm(:,19) = [];  %'nstems' is 1 for all instances
dataNorm(:,8) = [];  %'diameter' is 1 for all instances

score2 = dataNorm*wcoeff;

% plots to have a rough understanding of what the testing data looks like
% PC plot
figure(2);
gscatter(score2(:,2),score2(:,3),y);
title('Testing Data PC1 and PC2 plot'); 
xlabel('PC1');
ylabel('PC2');
% We can see that the testing data is very much like the training data

%% Testing - test data performance

testNrow = size(dataNorm,1);
pihat = zeros(testNrow,3);  % pihat(i,j) : probability of instance i being of type j
for i = 1:testNrow
    scorex = score2(i,1:16);
    pihat(i,:) = mnrval(B,scorex);
end
maxArr = max(pihat,[],2);
 
class = pihat(:,:) == maxArr;
correctCnt = 0;
for i = 1:testNrow
    if ((y(i)=='type1') && class(i,1)==1) || ((y(i)=='type2') && class(i,2)==1)...
            || ((y(i)=='type3') && class(i,3)==1)
        correctCnt = correctCnt + 1;
    end
end
wrongCnt = testNrow - correctCnt;

fprintf('---With Testing Data in the model, we have---\n');
fprintf('%d out of %d correctly classified\nRate : %f\n', correctCnt, testNrow, correctCnt/testNrow);
fprintf('%d out of %d wrongly classified\nRate : %f\n\n', wrongCnt, testNrow, wrongCnt/testNrow);

% Using the test dataset, 1115 out of 1917 instances were correctly
% classified. Accuracy = 0.581638
% It seems as the accuracy didn't drop drastically compared to the training
% dataset. We believe the reason to be because logistic regression is a
% rather a simple model, easy to generalize.

