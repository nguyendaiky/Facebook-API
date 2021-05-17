import pandas as pd 
import requests
import json
import os, sys
import time

Input = pd.read_csv("INPUT\input.csv")

times = 0
try:
    while True:

        times += 1

        for index in range(len(Input.values)):

            id = Input.values[index][0]
            url = 'https://graph.facebook.com/v10.0/{id}/insights'.format(id=id)
            access_token = Input.values[index][1]

            # GENERAL
            levelInput = "ad"
            fieldInput = ["account_name","campaign_id","campaign_name","adset_id","adset_name","ad_id","ad_name","spend","account_currency","frequency","reach","cpp","impressions","cpm","clicks","cpc","ctr","canvas_avg_view_time","engagement_rate_ranking","date_start","date_stop"]
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

            # REACTION
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
            t = x.text.encode().decode("unicode-escape")
            start = 9
            end = len(t) - 59
            t = t[start:end]
            arr = t.split('{"actions":[')
            for i in range(len(arr)):
                end = len(arr[i]) - 54
                arr[i] = arr[i][:end]
            arr[-1] += '}'

            reactionList = ["like","love","care","haha","wow","sad","angry","comment","onsite_conversion","post_reaction","post_engagement","page_engagement"]
            lists = [[] for _ in range(len(reactionList))]

            for i in range(1,len(arr)):

                if reactionList[0] in arr[i]:
                    v0 = arr[i].find(reactionList[0])
                    while not arr[i][v0].isnumeric():
                        v0 += 1
                    temp = ''
                    while arr[i][v0] != '"':
                        temp += arr[i][v0]
                        v0+=1
                    lists[0].append(temp)
                else:
                    lists[0].append(" ")

                if reactionList[1] in arr[i]:
                    v1 = arr[i].find(reactionList[1])
                    while not arr[i][v1].isnumeric():
                        v1 += 1
                    temp = ''
                    while arr[i][v1] != '"':
                        temp += arr[i][v1]
                        v1+=1
                    lists[1].append(temp)
                else:
                    lists[1].append(" ")

                if reactionList[2] in arr[i]:
                    v2 = arr[i].find(reactionList[2])
                    while not arr[i][v2].isnumeric():
                        v2 += 1
                    temp = ''
                    while arr[i][v2] != '"':
                        temp += arr[i][v2]
                        v2+=1
                    lists[2].append(temp)
                else:
                    lists[2].append(" ")

                if reactionList[3] in arr[i]:
                    v3 = arr[i].find(reactionList[3])
                    while not arr[i][v3].isnumeric():
                        v3 += 1
                    temp = ''
                    while arr[i][v3] != '"':
                        temp += arr[i][v3]
                        v3+=1
                    lists[3].append(temp)
                else:
                    lists[3].append(" ")

                if reactionList[4] in arr[i]:
                    v4 = arr[i].find(reactionList[4])
                    while not arr[i][v4].isnumeric():
                        v4 += 1
                    temp = ''
                    while arr[i][v4] != '"':
                        temp += arr[i][v4]
                        v4+=1
                    lists[4].append(temp)
                else:
                    lists[4].append(" ")

                if reactionList[5] in arr[i]:
                    v5 = arr[i].find(reactionList[5])
                    while not arr[i][v5].isnumeric():
                        v5 += 1
                    temp = ''
                    while arr[i][v5] != '"':
                        temp += arr[i][v5]
                        v5+=1
                    lists[5].append(temp)
                else:
                    lists[5].append(" ")

                if reactionList[6] in arr[i]:
                    v6 = arr[i].find(reactionList[6])
                    while not arr[i][v6].isnumeric():
                        v6 += 1
                    temp = ''
                    while arr[i][v6] != '"':
                        temp += arr[i][v6]
                        v6+=1
                    lists[6].append(temp)
                else:
                    lists[6].append(" ")

                if reactionList[7] in arr[i]:
                    v7 = arr[i].find(reactionList[7])
                    while not arr[i][v7].isnumeric():
                        v7 += 1
                    temp = ''
                    while arr[i][v7] != '"':
                        temp += arr[i][v7]
                        v7+=1
                    lists[7].append(temp)
                else:
                    lists[7].append(" ")

                if reactionList[8] in arr[i]:
                    v8 = arr[i].find(reactionList[8])
                    while not arr[i][v8].isnumeric():
                        v8 += 1
                    temp = ''
                    while arr[i][v8] != '"':
                        temp += arr[i][v8]
                        v8+=1
                    lists[8].append(temp)
                else:
                    lists[8].append(" ")

                if reactionList[9] in arr[i]:
                    v9 = arr[i].find(reactionList[9])
                    while not arr[i][v9].isnumeric():
                        v9 += 1
                    temp = ''
                    while arr[i][v9] != '"':
                        temp += arr[i][v9]
                        v9+=1
                    lists[9].append(temp)
                else:
                    lists[9].append(" ")

                if reactionList[10] in arr[i]:
                    v10 = arr[i].find(reactionList[10])
                    while not arr[i][v10].isnumeric():
                        v10 += 1
                    temp = ''
                    while arr[i][v10] != '"':
                        temp += arr[i][v10]
                        v10+=1
                    lists[10].append(temp)
                else:
                    lists[10].append(" ")

                if reactionList[11] in arr[i]:
                    v11 = arr[i].find(reactionList[11])
                    while not arr[i][v11].isnumeric():
                        v11 += 1
                    temp = ''
                    while arr[i][v11] != '"':
                        temp += arr[i][v11]
                        v11+=1
                    lists[11].append(temp)
                else:
                    lists[11].append(" ")

            raw_data = {}
            for i in range(len(reactionList)):
                raw_data[reactionList[i]] = lists[i]
            df = pd.DataFrame(raw_data, columns=reactionList)
            df.to_csv('reaction.csv', encoding="utf-8-sig",index=False)

            df1 = pd.read_csv('general.csv')
            df2 = pd.read_csv('reaction.csv')
            key = df2.keys()
            for i in range(len(key)):
                df1.insert(16+i,key[i],df2.values[:,i])
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
            os.remove('reaction.csv') 

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('Times {times} (at {now})'.format(times=times,now=current_time))
        time.sleep(Input.values[index][2])
        
except KeyboardInterrupt:
    print('Done!')
    sys.exit(0)