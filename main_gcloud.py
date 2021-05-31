import pandas as pd
import requests
import io,os
import datetime
import json
from google.cloud import storage
from google.cloud import bigquery

def fbapi_function(request):

    bucket_name = 'fbapi-bucket'
    blob_txt_name = 'input_field_time.txt'
    blob_csv_name = 'input_id_token.csv'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob_csv = bucket.blob(blob_csv_name)
    blob_csv = blob_csv.download_as_string()
    s = str(blob_csv,"utf-8-sig")
    s = io.StringIO(s)
    Input1 = pd.read_csv(s)

    blob_txt = bucket.blob(blob_txt_name)
    blob_txt = blob_txt.download_as_string()
    s = str(blob_txt,"utf-8-sig")
    Input2 = io.StringIO(s)

    # Clean input
    lines = Input2.readlines()
    generalFields = lines[1][8:]
    actionFields = lines[2][7:]

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
        end = t.find(',"paging":')
        t = t[start:end]
        t = '[' + t
        fileData = json.loads(t)
        df1 = pd.json_normalize(fileData)

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

    bucket.blob('OUTPUT/data({}).csv'.format(datetime.datetime.now().strftime('%d-%m-%Y'))).upload_from_string(result.to_csv(index=False), 'text/csv')

    # BigQuery
    client = bigquery.Client('potent-howl-314215')
    table_id = 'potent-howl-314215.fbapi.fbapi_data'
    client.delete_table(table_id, not_found_ok=True)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )
    blob = bucket.get_blob('OUTPUT/data({}).csv'.format(datetime.datetime.now().strftime('%d-%m-%Y')))
    with blob.open("rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    job.result()