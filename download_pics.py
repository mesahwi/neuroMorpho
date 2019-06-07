#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 20:32:11 2019

@author: allesgut
"""
import requests
import urllib.request



for neuronType in range(1, 4):
    savePath = "../gdrive/Team Drives/neuroMorpho/pics/"
    cell_type = "glutamatergic"
    if neuronType == 1:
        cell_type = "glutamatergic"
        savePath = savePath+'type1/'
    elif neuronType == 2:
        cell_type = "GABAergic"
        savePath = savePath+'type2/'
    elif neuronType== 3:
        cell_type = "cholinergic"
        savePath = savePath+'type3/'
        
        
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"species": ["drosophila melanogaster"], "cell_type": ["'+cell_type+'"], "archive": ["Chiang"]}'
    response = requests.post('http://neuromorpho.org/api/neuron/select', headers=headers, data=data)
    res = response.json()
    dataDict = res['_embedded']['neuronResources']
    pageNum = res['page']['totalPages']
    pageSize = len(dataDict)
    
    
    #take care of page0
    for i in range(0,pageSize):
        neuronId = dataDict[i]['neuron_id']
        pngUrl = dataDict[i]['png_url']
        name = dataDict[i]['neuron_name']
        urllib.request.urlretrieve(pngUrl,savePath+name+'.png')
            
    print(str(0)+'th page written!')
    
    #retrieve data from pages 1:pageNum
    for i in range(1, pageNum):
        response = requests.post('http://neuromorpho.org/api/neuron/select?page='+str(i), headers=headers, data=data)
        resJson = response.json()
        dataDict = resJson['_embedded']['neuronResources']
        pageSize = len(dataDict)
    
        for j in range(0,pageSize):
            neuronId = dataDict[j]['neuron_id']
            pngUrl = dataDict[i]['png_url']
            name = dataDict[i]['neuron_name']
            urllib.request.urlretrieve(pngUrl,savePath+name+'.png')
            
            
        print(str(i)+'th page written!')
        
    print('type' + neuronType +  'done!')

