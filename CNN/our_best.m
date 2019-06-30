%% First clear the variable

clear all
close all
clc

%% Make the directory for trainData set
datasetPath = fullfile('/MATLAB Drive', 'train/');
% we use 400, 400 gray scale pics to train!
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

%% Define First Network Architecture
% Define the convolutional neural network architecture.
% using the same architecture as we used for CIFAR 10!
% we use 3 cnn blocks
layers = [
    imageInputLayer([400 400])
    
    convolution2dLayer(3,16,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,16,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,16,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    fullyConnectedLayer(3)
    softmaxLayer
    classificationLayer];

% Use a Checkpoint and give large L2 Regularization to prevent overfitting train data
% we use Adam optimizer rather than sgdm and Learing rate as 0.0001
% we currently put maxepoch to 1 because to test the network which has a
% batchnormLayer(Matlab checkpoint does not save batchnorm variable :( ), 
% the network should be trained completely for initializing the
% batchnorm variable...
options = trainingOptions('adam',...
    'MaxEpochs',1, ...
    'Verbose',true,...
    'Plots','training-progress',...
    'ValidationFrequency',30,...
    'ValidationData',valimageData,...
    'ExecutionEnvironment','cpu',...
    'L2Regularization',7,...
    'InitialLearnRate',0.0001,...
    'CheckpointPath','/MATLAB Drive/layer1');
% loading the checkpoint if you want to start to train without checkpoint
% use below code please!
load('layer1/net_checkpoint__102__2019_06_19__11_51_35.mat', 'net');
%net = trainNetwork(trainimageData,layers,options);
% load the network 
net = trainNetwork(trainimageData,net.Layers,options);
%analyzeNetwork(net)
% our training and validation results were almost 80% and 47%, and more
% details you can find it in our ppt!


%% Classify Validation Images and Compute Accuracy
% we divide the test data before we proceed
datasetPath = fullfile('/MATLAB Drive', 'test/');
testData = imageDatastore(datasetPath,...
    'IncludeSubfolders',true,'LabelSource','foldernames', 'ReadFcn',...
    @(loc)imresize(rgb2gray(imread(loc)), [400 400],'method', 'bilinear'));
predictedLabels = classify(net,testData);
testLabels = testData.Labels;
accuracy = sum(predictedLabels == testLabels)/numel(testLabels) 

%% test result was 0.4637!! \ (^. ^) /

%% Visualize the filters
% filter 1 after relu activation
close all
layer = 'relu_1';
channels = 1:16;

I = deepDreamImage(net,layer,channels, ...
    'PyramidLevels',1, ...
    'Verbose',0);

figure
for i = 1:16
    subplot(4,4,i)
    imshow(I(:,:,:,i))
end
saveas(gcf, 'relu1.png');
%% filter 2 after relu activation
close all
layer = 'relu_2';
channels = 1:16;

I = deepDreamImage(net,layer,channels, ...
    'PyramidLevels',1, ...
    'Verbose',0);

figure
for i = 1:16
    subplot(4,4,i)
    imshow(I(:,:,:,i))
end
saveas(gcf, 'relu2.png');
%% filter 3 after relu activation
close all
layer = 'relu_3';
channels = 1:16;

I = deepDreamImage(net,layer,channels, ...
    'PyramidLevels',1, ...
    'Verbose',0);

figure
for i = 1:16
    subplot(4,4,i)
    imshow(I(:,:,:,i))
end
saveas(gcf, 'relu3.png');

%% conclusion 
% According to filters' image(i.e. 'relu1.png) above, it is a bit hard to classify neurons by their
% shape, because their shapes vary even within the same class.
% Although the result of cnn architecture is not as good as we
% expected, we believe that it is worth trying to classify neurons by
% neural networks, pun most definitely intended :)

% Due to computational limitations, we couldn't go deeper or wider.
% We believe if we apply 1 by 1 filters a lot, so-called 'bottleneck'
% architecture to increase the dimension or use a residual network which has a skip connection
% , the results could be more promising.
% Also, if we try with 3D images of neurons, the results could be better