"""
CLIENT: ADVANCE LEVEL

This is the client, remember to execute the server to be able to execute the client. This client will make different
requests to the server, two per endpoint:

1. Without json=1 parameter: to obtain HTML response
2. With json=1 parameter: to obtain JSON response

You can also check to obtain the same output using the browser with the url's below.

"""

import requests

print()
print("WELCOME TO THE CHECK PROGRAM")
print()

print("http://localhost:8000/listSpecies check HTML:")
print()
resp_1 = requests.get("http://localhost:8000/listSpecies")
print(resp_1.text)
print()

print("http://localhost:8000/listSpecies&json=1 check JSON:")
print()
resp_2 = requests.get("http://localhost:8000/listSpecies&json=1")
print(resp_2.json())
print()

print("http://localhost:8000/listSpecies?limit= check HTML (no limit selected):")
print()
resp_3 = requests.get("http://localhost:8000/listSpecies?limit=")
print(resp_3.text)
print()

print("http://localhost:8000/listSpecies?limit=&json=1 check JSON (no limit selected):")
print()
resp_4 = requests.get("http://localhost:8000/listSpecies?limit=&json=1")
print(resp_4.json())
print()

print("http://localhost:8000/listSpecies?limit=3 check HTML (limit=3):")
print()
resp_5 = requests.get("http://localhost:8000/listSpecies?limit=3")
print(resp_5.text)
print()

print("http://localhost:8000/listSpecies?limit=3&json=1 check JSON (limit=3):")
print()
resp_6 = requests.get("http://localhost:8000/listSpecies?limit=3&json=1")
print(resp_6.json())
print()

print("http://localhost:8000/karyotype?specie=cat check HTML:")
print()
resp_7 = requests.get("http://localhost:8000/karyotype?specie=cat")
print(resp_7.text)
print()

print("http://localhost:8000/karyotype?specie=cat&json=1 check JSON:")
print()
resp_8 = requests.get("http://localhost:8000/karyotype?specie=cat&json=1")
print(resp_8.json())
print()

print("http://localhost:8000/chromosomeLength?specie=cat&chromo=b2 check HTML:")
print()
resp_9 = requests.get("http://localhost:8000/chromosomeLength?specie=cat&chromo=b2")
print(resp_9.text)
print()

print("http://localhost:8000/chromosomeLength?specie=cat&chromo=b2&json=1 check JSON:")
print()
resp_10 = requests.get("http://localhost:8000/chromosomeLength?specie=cat&chromo=b2&json=1")
print(resp_10.json())
print()

print("http://localhost:8000/geneSeq?gene=FRAT2 check HTML:")
print()
resp_11 = requests.get("http://localhost:8000/geneSeq?gene=FRAT2")
print(resp_11.text)
print()

print("http://localhost:8000/geneSeq?gene=FRAT2&json=1 check JSON:")
print()
resp_12 = requests.get("http://localhost:8000/geneSeq?gene=FRAT2&json=1")
print(resp_12.json())
print()

print("http://localhost:8000/geneInfo?gene=tnf check HTML")
print()
resp_13 = requests.get("http://localhost:8000/geneInfo?gene=tnf")
print(resp_13.text)
print()

print("http://localhost:8000/geneInfo?gene=tnf&json=1 check JSON")
print()
resp_14 = requests.get("http://localhost:8000/geneInfo?gene=tnf&json=1")
print(resp_14.json())
print()

print("http://localhost:8000/geneCalc?gene=frat1 check HTML")
print()
resp_15 = requests.get("http://localhost:8000/geneCalc?gene=frat1")
print(resp_15.text)
print()

print("http://localhost:8000/geneCalc?gene=frat1&json=1 check JSON")
print()
resp_16 = requests.get("http://localhost:8000/geneCalc?gene=frat1&json=1")
print(resp_16.json())
print()

print("http://localhost:8000/geneList?chromo=7&start=140424943&end=140624564 check HTML")
print()
resp_17 = requests.get("http://localhost:8000/geneList?chromo=7&start=140424943&end=140624564")
print(resp_17.text)
print()

print("http://localhost:8000/geneList?chromo=7&start=140424943&end=140624564&json=1 check JSON")
print()
resp_18 = requests.get("http://localhost:8000/geneList?chromo=7&start=140424943&end=140624564&json=1")
print(resp_18.json())
print()