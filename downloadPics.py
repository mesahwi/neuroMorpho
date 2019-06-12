#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 20:32:11 2019

@author: allesgut
"""
import sys
import requests
import urllib.request
import csv

def getSavePath(neuronType, isTest):
    savePathTrain = "../gdrive/Team Drives/neuroMorpho/pics/train/"
    savePathTest = "../gdrive/Team Drives/neuroMorpho/pics/test/"

    if isTest:
        if neuronType == 1:
            savePath = savePathTest+'type1/'
        elif neuronType == 2:
            savePath = savePathTest+'type2/'
        elif neuronType== 3:
            savePath = savePathTest+'type3/'
    else:
        if neuronType == 1:
            savePath = savePathTrain+'type1/'
        elif neuronType == 2:
            savePath = savePathTrain+'type2/'
        elif neuronType== 3:
            savePath = savePathTrain+'type3/'    
    return savePath


startPoint = sys.argv[1]
#startPoint = 1
testIdx = []
f = open('../gdrive/Team Drives/neuroMorpho/testIdx.csv','r')
rdr = csv.reader(f)
for line in rdr:
    try:
        testIdx.append(int(line[1]))
    except:
        print('header: '+line[1])
f.close()

for neuronType in range(int(startPoint), 4):
    cell_type = "glutamatergic"
    if neuronType == 1:
        cell_type = "glutamatergic"
        #savePath = savePath+'type1/'
    elif neuronType == 2:
        cell_type = "GABAergic"
        #savePath = savePath+'type2/'
    elif neuronType== 3:
        cell_type = "cholinergic"
        #savePath = savePath+'type3/'
        
        
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"species": ["drosophila melanogaster"], "cell_type": ["'+cell_type+'"], "archive": ["Chiang"]}'
    response = requests.post('http://neuromorpho.org/api/neuron/select', headers=headers, data=data)
    res = response.json()
    dataDict = res['_embedded']['neuronResources']
    pageNum = res['page']['totalPages']
    pageSize = len(dataDict)
    
    idx = 0
    isDone = False
    #take care of page0
    for i in range(0,pageSize):
        if idx >= 3000:
            isDone = True
            idx = 0
            break

        isTest = idx in testIdx
        savePath = getSavePath(neuronType, isTest)
        
        neuronId = dataDict[i]['neuron_id']
        pngUrl = dataDict[i]['png_url']
        name = dataDict[i]['neuron_name']
        urllib.request.urlretrieve(pngUrl,savePath+name+'.png')
        idx = idx+1
        
    print(str(0)+'th page written!')
    
    #retrieve data from pages 1:pageNum
    for i in range(1, pageNum):
        if isDone:
            break
        
        response = requests.post('http://neuromorpho.org/api/neuron/select?page='+str(i), headers=headers, data=data)
        resJson = response.json()
        dataDict = resJson['_embedded']['neuronResources']
        pageSize = len(dataDict)
    
        for j in range(0,pageSize):
            if idx >= 3000:
                isDone = True
                idx = 0
                break
            
            isTest = idx in testIdx
            savePath = getSavePath(neuronType, isTest)
            
            neuronId = dataDict[j]['neuron_id']
            pngUrl = dataDict[j]['png_url']
            name = dataDict[j]['neuron_name']
            urllib.request.urlretrieve(pngUrl,savePath+name+'.png')
            idx = idx+1
            
        print(str(i)+'th page written!')
        
    print('type' + str(neuronType) +  'done!')










