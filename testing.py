import json

cust_response = open("output_http_server.json","r")
data = json.load(cust_response)

tanggal = 2

data_custom = data[tanggal-1]['tanggal']
print(data_custom)