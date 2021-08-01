import io
import requests
import json

port_number=8501

url = 'http://localhost:{}/v1/models/default:predict'.format(port_number)

f=open("/home/ubuntu/CCTV1-20190830235348.json","r")
if f.mode == 'r':
    json_value=f.read()
print(json_value)

#with open("/home/ubuntu/CCTV1-20190830235348.json",'r') as infile:
#    infile.read(json_value)
#    infile.close()

response = requests.post(url, data=json_value)
json_pred=response.json()
print(json_pred) 


