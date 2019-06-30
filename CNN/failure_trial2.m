%% First clear the variable

clear all
close all
clc

%% Make the directory for trainData set
datasetPath = fullfile('/MATLAB Drive', 'train/');
%% Reason why we think we failed. (failure meaning very low accuracy on val images)
% we used 300, 300 gray scale pics to train, instead of 400, 400 and we
% believe this makes the result worse.... However by fixing 400 to 300 we
% can make learning faster.
trainData = imageDatastore(datasetPath,...
    'IncludeSubfolders',true,'LabelSource','foldernames', 'ReadFcn',...
    @(loc)imresize(rgb2gray(imread(loc)), [300 300],'method', 'bilinear'));

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

%% trial 2
layers2 = [
    imageInputLayer([300 300])
    
    convolution2dLayer(10,16,'Padding',1, 'stride', 5)
    batchNormalizationLayer
    reluLayer
    
    convolution2dLayer(5,8,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,4,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    fullyConnectedLayer(3)
    softmaxLayer
    classificationLayer];

% we also use adam, lr : 0.0001, not L2 regularization.
options = trainingOptions('adam',...
    'MaxEpochs',5, ...
    'Verbose',true,...
    'Plots','training-progress',...
    'ValidationFrequency',30,...
    'ValidationData',valimageData,...
    'ExecutionEnvironment','cpu',...
    'InitialLearnRate',0.0001,...
    'CheckpointPath','/MATLAB Drive');

net = trainNetwork(trainimageData,layers2,options);