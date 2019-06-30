%% First clear the variable

clear all
close all
clc

%% Make the directory for trainData set and reason for failure:
datasetPath = fullfile('/MATLAB Drive', 'train/');
% we use 32, 32 gray scale pics to train! we've tried some new things that
% are related to input size and the results are as we expected.
% Resizing to 32 by 32 made the pics too hard to recognize.
trainData = imageDatastore(datasetPath,...
    'IncludeSubfolders',true,'LabelSource','foldernames', 'ReadFcn',...
    @(loc)imresize(rgb2gray(imread(loc)), [32 32],'method', 'bilinear'));

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


%%
layers4 = [
    imageInputLayer([32 32])
    convolution2dLayer(2,3,'Padding',1, 'WeightsInitializer','he') 
    batchNormalizationLayer
    reluLayer
    fullyConnectedLayer(32)
    fullyConnectedLayer(3)
    softmaxLayer
    classificationLayer];

% we use adam, lr: 0.001
options = trainingOptions('adam',...
    'MaxEpochs',5, ...
    'Verbose',true,...
    'ValidationFrequency',30,...
    'ValidationData',valimageData,...
    'Plots','training-progress',...
    'ExecutionEnvironment','cpu',...
    'InitialLearnRate',0.0001,...
    'CheckpointPath','/MATLAB Drive');

net = trainNetwork(trainimageData,layers4,options); 