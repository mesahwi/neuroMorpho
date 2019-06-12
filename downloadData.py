import requests
import csv


testIdx = []
f = open('../gdrive/Team Drives/neuroMorpho/testIdx.csv','r')
rdr = csv.reader(f)
for line in rdr:
    try:
        testIdx.append(int(line[1]))
    except:
        print('header: '+line[1])
f.close()

totalNum = 3000
#first, see number of pages
for neuronType in range(1, 4):
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
    
    savePathTrain = "../gdrive/Team Drives/neuroMorpho/measurements/train/"
    savePathTest = "../gdrive/Team Drives/neuroMorpho/measurements/test/"

    
    fileTrain = open(savePathTrain+'type'+str(neuronType)+'.csv', 'w', encoding='utf-8')
    fileTest = open(savePathTest+'type'+str(neuronType)+'.csv', 'w', encoding='utf-8')
    wrTrain = csv.writer(fileTrain, delimiter=',')
    wrTest = csv.writer(fileTest, delimiter=',')
    wrTrain.writerow(['neuron_name','neuron_id','surface','volume','n_bifs','n_branch','width','height',
                 'depth','diameter','eucDistance','pathDistance','branch_Order','contraction',
                 'fragmentation','partition_asymmetry','pk_classic','bif_ampl_local','fractal_Dim',
                 'soma_Surface','n_stems', 'bif_ampl_remote','length',
                 'age_classification', 'brain_region', 'physical_Integrity'])
    wrTest.writerow(['neuron_name','neuron_id','surface','volume','n_bifs','n_branch','width','height',
                 'depth','diameter','eucDistance','pathDistance','branch_Order','contraction',
                 'fragmentation','partition_asymmetry','pk_classic','bif_ampl_local','fractal_Dim',
                 'soma_Surface','n_stems', 'bif_ampl_remote','length',
                 'age_classification', 'brain_region', 'physical_Integrity'])
    
    
    idx = 0
    isDone= False
    #take care of page0
    for i in range(0,pageSize):
        if idx >= totalNum:
            isDone = True
            idx = 0
            break

        neuronId = dataDict[i]['neuron_id']
        msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
        measurement = msrResponse.json()
        inputList = list(measurement.values())
        inputList.append(dataDict[i]['age_classification'])
        inputList.append(dataDict[i]['brain_region'][0])
        inputList.append(dataDict[i]['physical_Integrity'])
        
        if idx in testIdx:
            wrTest.writerow(inputList)
        else:
            wrTrain.writerow(inputList)
        
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
            if idx >= totalNum:
                isDone = True
                idx = 0
                break
            
            neuronId = dataDict[j]['neuron_id']
            msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
            measurement = msrResponse.json()
            inputList = list(measurement.values())
            inputList.append(dataDict[j]['age_classification'])
            inputList.append(dataDict[j]['brain_region'][0])
            inputList.append(dataDict[j]['physical_Integrity'])
            
            if idx in testIdx:
                wrTest.writerow(inputList)
            else:
                wrTrain.writerow(inputList)
                
            idx= idx+1
            
        print(str(i)+'th page written!')
        
        
    fileTrain.close()
    fileTest.close()
    print('type'+str(i)+ 'done!')


