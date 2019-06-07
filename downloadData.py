import requests
import csv

type1 = open('type1.csv', 'w', encoding='utf-8')
wr = csv.writer(type1, delimiter=',')
wr.writerow(['neuron_name','neuron_id','surface','volume','n_bifs','n_branch','width','height',
             'depth','diameter','eucDistance','pathDistance','branch_Order','contraction',
             'fragmentation','partition_asymmetry','pk_classic','bif_ampl_local','fractal_Dim',
             'soma_Surface','n_stems', 'bif_ampl_remote','length'])

#first, see number of pages
headers = {
    'Content-Type': 'application/json',
}
data = '{"species": ["drosophila melanogaster"], "cell_type": ["glutamatergic"], "archive": ["Chiang"]}'
response = requests.post('http://neuromorpho.org/api/neuron/select', headers=headers, data=data)
res = response.json()
pageNum = res['page']['totalPages']
pageSize = res['page']['size']


#take care of page0
dataDict = res['_embedded']['neuronResources']
for i in range(0,pageSize):
    neuronId = dataDict[i]['neuron_id']
    msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
    measurement = msrResponse.json()
    wr.writerow(list(measurement.values()))
        
print(str(0)+'th page written!')

#retrieve data from pages 1:pageNum
for i in range(1, pageNum):
    response = requests.post('http://neuromorpho.org/api/neuron/select?page='+str(i), headers=headers, data=data)
    resJson = response.json()
    pageSize = resJson['page']['size']
    dataDict = resJson['_embedded']['neuronResources']

    for j in range(0,pageSize):
        neuronId = dataDict[j]['neuron_id']
        msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
        measurement = msrResponse.json()
        wr.writerow(list(measurement.values()))
        
    print(str(i)+'th page written!')
    
    
type1.close()
print('type1 done!')
    


