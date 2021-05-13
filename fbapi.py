
import requests
import pandas as pd

# Input
levelInput = "ad"
fieldInput = ["account_name","campaign_name","adset_name","ad_name","account_currency","reach","impressions","frequency","cpm","clicks","date_start","date_stop"]
url = "https://graph.facebook.com/v10.0/act_627895837771934/insights"
access_token = "EAACLELV0dZCMBAIS6Jmhd256FiDOyUndbs6j6HITe8XFlRCTCiDIqwImhkSFZCZBJJ64VsQmZBa302NTTAzcVYffhZB6o726sZBLA7Pjd3kK8xZCkSp8yNlHbewEj4EwEdomNfs6ECuqsXEZBnxPuqvQ1DAUCys3Chgo8prvQ6mVGhwhJAoK8wXH"

# Get
fields = ','.join(fieldInput)
params = {
    "level":levelInput,
    "fields":fields,
    "access_token": access_token,
}
x = requests.get(url,params)

# Save 
fileWrite = open("output.txt",'w')
fileWrite.write(x.text)
fileWrite.close()
fileRead = open("output.txt","r")
line = fileRead.readline()
fileRead.close()

# Xu ly
first = line.find('[') + 1
last = line.find(']')
data = line[first:last]
data += ','
data_line = [i[1:] for i in data.split('},')]
for i in range(len(data_line)):
    data_line[i] += ','

def find(string):
    ans = -1
    for i in range(len(string)):
        if string[i] == '"':
            ans = i+1
    return ans

lists = [[] for _ in range(len(fieldInput))]
for line in data_line:
    arr = line.split('",')
    for i in range(len(arr)-1):
        lists[i].append(arr[i][find(arr[i]):])

raw_data = {}
for i in range(len(fieldInput)):
    raw_data[fieldInput[i]] = lists[i]
df = pd.DataFrame(raw_data, columns=fieldInput)
df.to_csv('output.csv')
    
