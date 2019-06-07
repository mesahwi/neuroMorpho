import requests
import csv

savePath = "../gdrive/My Drive/neuroMorpho/"

type1 = open(savePath+'type1.csv', 'w', encoding='utf-8')
wr = csv.writer(type1, delimiter=',')
wr.writerow(['neuron_name','neuron_id','surface','volume','n_bifs','n_branch','width','height',
             'depth','diameter','eucDistance','pathDistance','branch_Order','contraction',
             'fragmentation','partition_asymmetry','pk_classic','bif_ampl_local','fractal_Dim',
             'soma_Surface','n_stems', 'bif_ampl_remote','length',
             'age_classification', 'brain_region', 'physical_Integrity'])

#first, see number of pages
headers = {
    'Content-Type': 'application/json',
}
data = '{"species": ["drosophila melanogaster"], "cell_type": ["glutamatergic"], "archive": ["Chiang"]}'
response = requests.post('http://neuromorpho.org/api/neuron/select', headers=headers, data=data)
res = response.json()
dataDict = res['_embedded']['neuronResources']
pageNum = res['page']['totalPages']
pageSize = len(dataDict)


#take care of page0
for i in range(0,pageSize):
    neuronId = dataDict[i]['neuron_id']
    msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
    measurement = msrResponse.json()
    inputList = list(measurement.values())
    inputList.append(dataDict[i]['age_classification'])
    inputList.append(dataDict[i]['brain_region'][0])
    inputList.append(dataDict[i]['physical_Integrity'])
    wr.writerow(inputList)
        
print(str(0)+'th page written!')

#retrieve data from pages 1:pageNum
for i in range(1, pageNum):
    response = requests.post('http://neuromorpho.org/api/neuron/select?page='+str(i), headers=headers, data=data)
    resJson = response.json()
    dataDict = resJson['_embedded']['neuronResources']
    pageSize = len(dataDict)

    for j in range(0,pageSize):
        neuronId = dataDict[j]['neuron_id']
        msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
        measurement = msrResponse.json()
        inputList = list(measurement.values())
        inputList.append(dataDict[i]['age_classification'])
        inputList.append(dataDict[i]['brain_region'][0])
        inputList.append(dataDict[i]['physical_Integrity'])
        wr.writerow(inputList)
        
    print(str(i)+'th page written!')
    
    
type1.close()
print('type1 done!')


#============================#
#Same goes for types 2 and 3
print('type 2 : ')
type2 = open(savePath+'type2.csv', 'w', encoding='utf-8')
wr2 = csv.writer(type2, delimiter=',')
wr2.writerow(['neuron_name','neuron_id','surface','volume','n_bifs','n_branch','width','height',
             'depth','diameter','eucDistance','pathDistance','branch_Order','contraction',
             'fragmentation','partition_asymmetry','pk_classic','bif_ampl_local','fractal_Dim',
             'soma_Surface','n_stems', 'bif_ampl_remote','length',
             'age_classification', 'brain_region', 'physical_Integrity'])

#first, see number of pages
headers = {
    'Content-Type': 'application/json',
}
data = '{"species": ["drosophila melanogaster"], "cell_type": ["GABAergic"], "archive": ["Chiang"]}'
response = requests.post('http://neuromorpho.org/api/neuron/select', headers=headers, data=data)
res = response.json()
dataDict = res['_embedded']['neuronResources']
pageNum = res['page']['totalPages']
pageSize = len(dataDict)


#take care of page0
for i in range(0,pageSize):
    neuronId = dataDict[i]['neuron_id']
    msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
    measurement = msrResponse.json()
    inputList = list(measurement.values())
    inputList.append(dataDict[i]['age_classification'])
    inputList.append(dataDict[i]['brain_region'][0])
    inputList.append(dataDict[i]['physical_Integrity'])
    wr2.writerow(inputList)
        
print(str(0)+'th page written!')

#retrieve data from pages 1:pageNum
for i in range(1, pageNum):
    response = requests.post('http://neuromorpho.org/api/neuron/select?page='+str(i), headers=headers, data=data)
    resJson = response.json()
    dataDict = resJson['_embedded']['neuronResources']
    pageSize = len(dataDict)

    for j in range(0,pageSize):
        neuronId = dataDict[j]['neuron_id']
        msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
        measurement = msrResponse.json()
        inputList = list(measurement.values())
        inputList.append(dataDict[i]['age_classification'])
        inputList.append(dataDict[i]['brain_region'][0])
        inputList.append(dataDict[i]['physical_Integrity'])
        wr2.writerow(inputList)

        
    print(str(i)+'th page written!')
    
    
type2.close()
print('type2 done!')


####

print('type 3 : ')
type3 = open(savePath+'type3.csv', 'w', encoding='utf-8')
wr3 = csv.writer(type3, delimiter=',')
wr3.writerow(['neuron_name','neuron_id','surface','volume','n_bifs','n_branch','width','height',
             'depth','diameter','eucDistance','pathDistance','branch_Order','contraction',
             'fragmentation','partition_asymmetry','pk_classic','bif_ampl_local','fractal_Dim',
             'soma_Surface','n_stems', 'bif_ampl_remote','length',
             'age_classification', 'brain_region', 'physical_Integrity'])

#first, see number of pages
headers = {
    'Content-Type': 'application/json',
}
data = '{"species": ["drosophila melanogaster"], "cell_type": ["cholinergic"], "archive": ["Chiang"]}'
response = requests.post('http://neuromorpho.org/api/neuron/select', headers=headers, data=data)
res = response.json()
dataDict = res['_embedded']['neuronResources']
pageNum = res['page']['totalPages']
pageSize = len(dataDict)


#take care of page0
for i in range(0,pageSize):
    neuronId = dataDict[i]['neuron_id']
    msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
    measurement = msrResponse.json()
    inputList = list(measurement.values())
    inputList.append(dataDict[i]['age_classification'])
    inputList.append(dataDict[i]['brain_region'][0])
    inputList.append(dataDict[i]['physical_Integrity'])
    wr3.writerow(inputList)
        
print(str(0)+'th page written!')

#retrieve data from pages 1:pageNum
for i in range(1, pageNum):
    response = requests.post('http://neuromorpho.org/api/neuron/select?page='+str(i), headers=headers, data=data)
    resJson = response.json()
    dataDict = resJson['_embedded']['neuronResources']
    pageSize = len(dataDict)

    for j in range(0,pageSize):
        neuronId = dataDict[j]['neuron_id']
        msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
        measurement = msrResponse.json()
        inputList = list(measurement.values())
        inputList.append(dataDict[i]['age_classification'])
        inputList.append(dataDict[i]['brain_region'][0])
        inputList.append(dataDict[i]['physical_Integrity'])
        wr3.writerow(inputList)
        
    print(str(i)+'th page written!')
    
    
type3.close()
print('type3 done!')


