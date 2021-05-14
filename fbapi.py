
from numpy import dtype
import requests
import pandas as pd
import unicodedata2

# Input
levelInput = "ad"
fieldInput = ["account_name","campaign_id","campaign_name","adset_name","ad_name","account_currency","reach","impressions","frequency","cpm","clicks","date_start","date_stop"]
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
t = x.text.encode().decode("unicode-escape")

# Save 
fileWrite = open("output1.txt",'w', encoding="utf-8")
fileWrite.write(t)
fileWrite.close()
fileRead = open("output1.txt","r", encoding="utf-8")
line = fileRead.readline()
fileRead.close()

params2 = {
    "level":"ad",
    "fields":"actions,date_start,date_stop",
    "access_token":access_token,
}
y = requests.get(url,params2)
k = y.text

def find(string,t):
    ans = -1
    for i in range(len(string)):
        if string[i] == t:
            ans = i+1
    return ans

fileWrite = open("output2.txt",'w', encoding="utf-8")
fileWrite.write(k)
fileWrite.close()
fileRead = open("output2.txt","r", encoding="utf-8")
line2 = fileRead.readline()
fileRead.close()
start = 9
end = len(line2)-60
line2 = line2[start:end]
line2 = line2.split(',{"actions":[')
s1 = '"like","value"'
s2 = '"comment","value"'
s3 = '"link_click","value"'
a1 = []
a2 = []
a3 = []
for i in range(len(line2)):
    if s1 in line2[i]:
        v1 = line2[i].find(s1) + len(s1) + 2
        temp = ''
        while line2[i][v1] != '"':
            temp += line2[i][v1]
            v1+=1
        a1.append(temp)
    else:
        a1.append(0)
    if s2 in line2[i]:
        v2 = line2[i].find(s2) + len(s2) + 2
        temp = ''
        while line2[i][v2] != '"':
            temp += line2[i][v2]
            v2+=1
        a2.append(temp)
    else:
        a2.append(0)
    if s3 in line2[i]:
        v3 = line2[i].find(s3) + len(s3) + 2
        temp = ''
        while line2[i][v3] != '"':
            temp += line2[i][v3]
            v3+=1
        a3.append(temp)
    else:
        a3.append(0)

# Xu ly
first = line.find('[') + 1
last = line.find(']')
data = line[first:last]
data += ','
data_line = [i[1:] for i in data.split('},')]
for i in range(len(data_line)):
    data_line[i] += ','

lists = [[] for _ in range(len(fieldInput))]
for line in data_line:
    arr = line.split('",')
    for i in range(len(arr)-1):
        lists[i].append(arr[i][find(arr[i],'"'):])
lists.insert(10,a1)
lists.insert(11,a2)
# lists.insert(12,a3)
fieldInput.insert(10,'like')
fieldInput.insert(11,'comment')
# fieldInput.insert(12,'link_click')

raw_data = {}
for i in range(len(fieldInput)):
    raw_data[fieldInput[i]] = lists[i]
df = pd.DataFrame(raw_data, columns=fieldInput)
df.to_csv('output.csv', encoding="utf-8")
    
