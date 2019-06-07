import requests
import csv

type1 = open('../gdrive/My Drive/neuroMorpho/type1.csv', 'w', encoding='utf-8')
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


#take care of page0
dataDict = res['_embedded']['neuronResources']
for i in range(0,50):
    neuronId = dataDict[i]['neuron_id']
    msrResponse = requests.get('http://neuromorpho.org/api/morphometry/id/'+ str(neuronId))
    measurement = msrResponse.json()
    wr.writerow(list(measurement.values()))
    print(str(i)+'th measurement written!')
    
    
type1.close()
