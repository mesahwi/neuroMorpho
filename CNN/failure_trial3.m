%% First clear the variable

clear all
close all
clc

%% Make the directory for trainData set
datasetPath = fullfile('/MATLAB Drive', 'train/');
% we used 400, 400 gray scale pics to train!
trainData = imageDatastore(datasetPath,...
    'IncludeSubfolders',true,'LabelSource','foldernames', 'ReadFcn',...
    @(loc)imresize(rgb2gray(imread(loc)), [400 400],'method', 'bilinear'));

%% count the labels
labelCount = countEachLabel(trainData)

%% check the size and image
img = readimage(trainData,1);
size(img)
imshow(img)

%% Specify Training and Validation Sets
% divide train and val set into 2200 : 161
trainNumFiles = 2200;
rng(123);
[trainimageData,valimageData] = splitEachLabel(trainData,trainNumFiles,'randomize');
%% layer 3 we tried to use small filters and reason for failure:
% we believe that the smaller filters could yield better results,
% but we couldn't put large number of filters due to our computational
% limitations. This seems like the main reason for failure.
layers3 = [
    imageInputLayer([400 400])
    
    convolution2dLayer(2, 8,'Padding',1, 'stride', 1, 'WeightsInitializer','he') % we use 8 filters instead of 16 :(
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(4)
    convolution2dLayer(2, 4, 'Padding', 1) % we use 4 filters instead of 16 :(
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(4)
    convolution2dLayer(2, 2, 'Padding', 1) % we use 2 filters.
    batchNormalizationLayer
    reluLayer
    fullyConnectedLayer(64)
    fullyConnectedLayer(3)
    softmaxLayer
    classificationLayer];

% we use adam, lr : 0.0001, l2regularization
options = trainingOptions('adam',...
    'MaxEpochs',5, ...
    'Verbose',true,...
    'Plots','training-progress',...
    'ValidationFrequency',30,...
    'ValidationData',valimageData,...
    'ExecutionEnvironment','cpu',...
    'InitialLearnRate',0.0001,... 
    'L2Regularization',5,...
    'CheckpointPath','/MATLAB Drive');

net = trainNetwork(trainimageData,layers3,options); 


