import requests

BASE = "http://127.0.0.1:5000/"
physics =  [{'name': 'Tijani Jamiu','age':23,'gp':5,'gender':'M'},
            {'name': 'Sagbo Sajiro','age':22,'gp':1,'gender':'M'},
            {'name': 'Onosaya Zulfah','age':23,'gp':4,'gender':'F'},
            {'name': 'Oyinda Sth','age':22,'gp':4,'gender':'F'},
            {'name': 'Lawal Rianat','age':26,'gp':3,'gender':'F'},
            {'name': 'Rasak Moses','age':24,'gp':4,'gender':'M'}]

for i in range(len(physics)):
    id = i+2
    response = requests.put(BASE + f"department/{id}",physics[i])
    print(response.json())