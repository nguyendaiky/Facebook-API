import pandas as pd
import requests

import json
import os, sys
import time
from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'INPUT\potent-howl-314215-ce6ba743b25f.json'
client = bigquery.Client('potent-howl-314215')
table_id = 'potent-howl-314215.fbapi.fbapi_data'

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
        result = pd.DataFrame()
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
            data = eval(t)
            df1 = pd.json_normalize(data)


            # Save 
            # fileWrite = open("general.json",'w', encoding="utf-8-sig")
            # fileWrite.write(t)
            # fileWrite.close()
            # with open('general.json',encoding="utf-8-sig") as project_file:    
            #     data = json.load(project_file)  
            # df1 = pd.json_normalize(data)

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
            df2 = pd.DataFrame(raw_data, columns=reactionList)

            # Merge General and Action
            key = df2.keys()
            for i in range(len(key)):
                df1.insert(37+i,key[i],df2.values[:,i])

            if index == 0:
                result = df1.copy(deep=True)
            else:
                result = [result,df1]
                result = pd.concat(result,ignore_index=True)

        # client = bigquery.Client('potent-howl-314215')
        # table_id = 'potent-howl-314215.fbapi.fbapi_data'
        # client.delete_table(table_id, not_found_ok=True)
        # job_config = bigquery.LoadJobConfig(
        #     source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
        # )
        # job = client.load_table_from_file(result, table_id, job_config=job_config)
        # job.result()
        # table = client.get_table(table_id)
            
        result.to_csv('OUTPUT\data.csv',encoding="utf-8-sig",index=False)

        # BigQuery
        client.delete_table(table_id, not_found_ok=True)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
        )
        file_path = 'OUTPUT\data.csv'
        with open(file_path, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        job.result()
        table = client.get_table(table_id)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('Times {times} (at {now})'.format(times=times,now=current_time))
        # print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), table_id))
        time.sleep(time_sleep)
        
except KeyboardInterrupt:
    print('Done!')
    sys.exit(0)
