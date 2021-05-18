import pandas as pd 
import requests
import json
import os, sys
import time

# Read input
Input1 = pd.read_csv("INPUT\input_id_token.csv")
Input2 = open('INPUT\input_field_time.txt','r')

# Clean input
lines = Input2.readlines()
time_sleep = int(lines[0][20:])
generalFields = lines[1][8:]
actionFields = lines[2][7:]

# Loop until Ctrl + C
times = 0
try:
    while True:
        times += 1
        for index in range(len(Input1.values)):

            id = Input1.values[index][0]
            url = 'https://graph.facebook.com/v10.0/{id}/insights'.format(id=id)
            access_token = Input1.values[index][1]

            # GENERAL
            levelInput = "ad"
            fieldInput = generalFields.split(',')
            date_presetInput = "maximum"

            # Get
            fields = ','.join(fieldInput)
            params = {
                "level":levelInput,
                "fields":fields,
                "date_preset":date_presetInput,
                "access_token": access_token,
            }
            x = requests.get(url,params)
            t = x.text
            start = 9
            end = len(t) - 59
            t = t[start:end]
            t = '[' + t + ']'

            # Save 
            fileWrite = open("general.json",'w', encoding="utf-8-sig")
            fileWrite.write(t)
            fileWrite.close()
            with open('general.json',encoding="utf-8-sig") as project_file:    
                data = json.load(project_file)  
            df = pd.json_normalize(data)
            df.to_csv(r'general.csv',encoding='utf-8-sig', index=False ,header=True)

            # ACTION
            levelInput = "ad"
            fieldInput = ["actions"]
            action_breakdowns = "action_reaction,action_type"

            # Get
            fields = ','.join(fieldInput)
            params = {
                "level":levelInput,
                "fields":fields,
                "date_preset":date_presetInput,
                "action_breakdowns":action_breakdowns,
                "access_token": access_token,
            }
            x = requests.get(url,params)
            t = x.text
            start = 9
            end = len(t) - 59
            t = t[start:end]
            arr = t.split('{"actions":[')
            for i in range(len(arr)):
                end = len(arr[i]) - 54
                arr[i] = arr[i][:end]
            arr[-1] += '}'

            # Save
            reactionList = actionFields.split(',')
            lists = [[] for _ in range(len(reactionList))]

            for i in range(1,len(arr)):
                for j in range(0,len(reactionList)):
                    if reactionList[j] in arr[i]:
                        vj = arr[i].find(reactionList[j])
                        while not arr[i][vj].isnumeric():
                            vj += 1
                        temp = ''
                        while arr[i][vj] != '"':
                            temp += arr[i][vj]
                            vj+=1
                        lists[j].append(temp)
                    else:
                        lists[j].append(" ")

            raw_data = {}
            for i in range(len(reactionList)):
                raw_data[reactionList[i]] = lists[i]
            df = pd.DataFrame(raw_data, columns=reactionList)
            df.to_csv('action.csv', encoding="utf-8-sig",index=False)

            # Merge General and Action
            df1 = pd.read_csv('general.csv')
            df2 = pd.read_csv('action.csv')
            key = df2.keys()
            for i in range(len(key)):
                df1.insert(37+i,key[i],df2.values[:,i])
            stt = []
            for i in range(1,len(df1.values)+1):
                stt.append(i)
            df1.insert(0,"stt",stt)
            if not os.path.exists('OUTPUT'):
                os.mkdir('OUTPUT')
            name = 'OUTPUT\data{index}.csv'.format(index=index+1)
            df1.to_csv(name,encoding="utf-8-sig",index=False)
            os.remove('general.json')
            os.remove('general.csv')
            os.remove('action.csv') 

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('Times {times} (at {now})'.format(times=times,now=current_time))
        time.sleep(time_sleep)
        
except KeyboardInterrupt:
    print('Done!')
    sys.exit(0)