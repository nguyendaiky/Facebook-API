import pandas as pd
import mysql.connector
import requests
import json
import os, sys
import time

# Read input
Input1 = pd.read_csv("INPUT\input_id_token.csv")
Input2 = open('INPUT\input_field_time.txt','r')

# Connect to Database
mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='fbapi'
)
mycursor = mydb.cursor()

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

        # Create table
        mycursor.execute('DROP TABLE IF EXISTS data')
        sql = 'CREATE TABLE data (account_id varchar(70),account_name varchar(70),campaign_id varchar(70),campaign_name varchar(70),adset_id varchar(70),adset_name varchar(70),ad_id varchar(70),ad_name varchar(70),spend varchar(70),account_currency varchar(70),social_spend varchar(70),buying_type varchar(70),frequency varchar(70),reach varchar(70),cpp varchar(70),impressions varchar(70),cpm varchar(70),clicks varchar(70),cpc varchar(70),ctr varchar(70),unique_clicks varchar(70),unique_ctr varchar(70),unique_inline_link_click_ctr varchar(70),unique_inline_link_clicks varchar(70),unique_link_clicks_ctr varchar(70),cost_per_inline_link_click varchar(70),cost_per_inline_post_engagement varchar(70),cost_per_unique_click varchar(70),cost_per_unique_inline_link_click varchar(70),engagement_rate_ranking varchar(70),conversion_rate_ranking varchar(70),inline_link_clicks varchar(70),inline_link_click_ctr varchar(70),inline_post_engagement varchar(70),objective varchar(70),optimization_goal varchar(70),quality_ranking varchar(70),post_like varchar(70),love varchar(70),care varchar(70),haha varchar(70),wow varchar(70),sad varchar(70),angry varchar(70),comment varchar(70),checkin varchar(70),credit_spent varchar(70),landing_page_view varchar(70),onsite_conversion_post_save varchar(70),post varchar(70),rsvp varchar(70),contact_total varchar(70),contact_website varchar(70),contact_mobile_app varchar(70),contact_offline varchar(70),flow_complete varchar(70),messaging_block varchar(70),messaging_conversation_started_7d varchar(70),messaging_first_reply varchar(70),onsite_conversion_purchase varchar(70),outbound_click varchar(70),post_reaction varchar(70),photo_view varchar(70),video_view varchar(70),post_engagement varchar(70),page_engagement varchar(70),fb_pixel_add_payment_info varchar(70),fb_pixel_add_to_cart varchar(70),fb_pixel_add_to_wishlist varchar(70),fb_pixel_complete_registration varchar(70),fb_pixel_custom varchar(70),fb_pixel_initiate_checkout varchar(70),fb_pixel_lead varchar(70),fb_pixel_purchase varchar(70),fb_pixel_search varchar(70),fb_pixel_view_content varchar(70),fb_mobile_achievement_unlocked varchar(70),fb_mobile_activate_app varchar(70),fb_mobile_add_payment_info varchar(70),fb_mobile_add_to_cart varchar(70),fb_mobile_add_to_wishlist varchar(70),fb_mobile_complete_registration varchar(70),fb_mobile_content_view varchar(70),fb_mobile_initiated_checkout varchar(70),fb_mobile_level_achieved varchar(70),fb_mobile_purchase varchar(70),fb_mobile_rate varchar(70),fb_mobile_search varchar(70),fb_mobile_spent_credits varchar(70),fb_mobile_tutorial_completion varchar(70),omni_app_install varchar(70),omni_purchase varchar(70),omni_add_to_cart varchar(70),omni_complete_registration varchar(70),omni_view_content varchar(70),omni_search varchar(70),omni_initiated_checkout varchar(70),omni_achievement_unlocked varchar(70),omni_activate_app varchar(70),omni_level_achieved varchar(70),omni_rate varchar(70),omni_spend_credits varchar(70),omni_tutorial_completion varchar(70),omni_custom varchar(70),customize_product_total varchar(70),customize_product_website varchar(70),customize_product_mobile_app varchar(70),customize_product_offline varchar(70),find_location_total varchar(70),find_location_website varchar(70),find_location_mobile_app varchar(70),find_location_offline varchar(70),donate_total varchar(70),donate_website varchar(70),donate_on_facebook varchar(70),donate_mobile_app varchar(70),donate_offline varchar(70),schedule_total varchar(70),schedule_website varchar(70),schedule_mobile_app varchar(70),schedule_offline varchar(70),start_trial_total varchar(70),start_trial_website varchar(70),start_trial_mobile_app varchar(70),start_trial_offline varchar(70),submit_application_total varchar(70),submit_application_website varchar(70),submit_application_mobile_app varchar(70),submit_application_offline varchar(70),submit_application_on_facebook varchar(70),subscribe_total varchar(70),subscribe_website varchar(70),subscribe_mobile_app varchar(70),subscribe_offline varchar(70),recurring_subscription_payment_total varchar(70),recurring_subscription_payment_website varchar(70),recurring_subscription_payment_mobile_app varchar(70),recurring_subscription_payment_offline varchar(70),cancel_subscription_total varchar(70),cancel_subscription_website varchar(70),cancel_subscription_mobile_app varchar(70),cancel_subscription_offline varchar(70),ad_click_mobile_app varchar(70),ad_impression_mobile_app varchar(70),click_to_call_call_confirm varchar(70),date_start varchar(70),date_stop varchar(70))'
        mycursor.execute(sql)

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
            if not os.path.exists('OUTPUT'):
                os.mkdir('OUTPUT')
            name = 'OUTPUT\data{index}.csv'.format(index=index+1)
            df1.to_csv(name,encoding="utf-8-sig",index=False)
            os.remove('general.json')
            os.remove('general.csv')
            os.remove('action.csv') 
            
            # Save to Database
            df = pd.read_csv('OUTPUT\data{index}.csv'.format(index=index+1))
            sql = "INSERT INTO data (account_id,account_name,campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,spend,account_currency,social_spend,buying_type,frequency,reach,cpp,impressions,cpm,clicks,cpc,ctr,unique_clicks,unique_ctr,unique_inline_link_click_ctr,unique_inline_link_clicks,unique_link_clicks_ctr,cost_per_inline_link_click,cost_per_inline_post_engagement,cost_per_unique_click,cost_per_unique_inline_link_click,engagement_rate_ranking,conversion_rate_ranking,inline_link_clicks,inline_link_click_ctr,inline_post_engagement,objective,optimization_goal,quality_ranking,post_like,love,care,haha,wow,sad,angry,comment,checkin,credit_spent,landing_page_view,onsite_conversion_post_save,post,rsvp,contact_total,contact_website,contact_mobile_app,contact_offline,flow_complete,messaging_block,messaging_conversation_started_7d,messaging_first_reply,onsite_conversion_purchase,outbound_click,post_reaction,photo_view,video_view,post_engagement,page_engagement,fb_pixel_add_payment_info,fb_pixel_add_to_cart,fb_pixel_add_to_wishlist,fb_pixel_complete_registration,fb_pixel_custom,fb_pixel_initiate_checkout,fb_pixel_lead,fb_pixel_purchase,fb_pixel_search,fb_pixel_view_content,fb_mobile_achievement_unlocked,fb_mobile_activate_app,fb_mobile_add_payment_info,fb_mobile_add_to_cart,fb_mobile_add_to_wishlist,fb_mobile_complete_registration,fb_mobile_content_view,fb_mobile_initiated_checkout,fb_mobile_level_achieved,fb_mobile_purchase,fb_mobile_rate,fb_mobile_search,fb_mobile_spent_credits,fb_mobile_tutorial_completion,omni_app_install,omni_purchase,omni_add_to_cart,omni_complete_registration,omni_view_content,omni_search,omni_initiated_checkout,omni_achievement_unlocked,omni_activate_app,omni_level_achieved,omni_rate,omni_spend_credits,omni_tutorial_completion,omni_custom,customize_product_total,customize_product_website,customize_product_mobile_app,customize_product_offline,find_location_total,find_location_website,find_location_mobile_app,find_location_offline,donate_total,donate_website,donate_on_facebook,donate_mobile_app,donate_offline,schedule_total,schedule_website,schedule_mobile_app,schedule_offline,start_trial_total,start_trial_website,start_trial_mobile_app,start_trial_offline,submit_application_total,submit_application_website,submit_application_mobile_app,submit_application_offline,submit_application_on_facebook,subscribe_total,subscribe_website,subscribe_mobile_app,subscribe_offline,recurring_subscription_payment_total,recurring_subscription_payment_website,recurring_subscription_payment_mobile_app,recurring_subscription_payment_offline,cancel_subscription_total,cancel_subscription_website,cancel_subscription_mobile_app,cancel_subscription_offline,ad_click_mobile_app,ad_impression_mobile_app,click_to_call_call_confirm,date_start,date_stop) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            for i in range(0,len(df.values)):
                val = [str(i) for i in df.values[i]]
                mycursor.execute(sql, val)
            mydb.commit()

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('Times {times} (at {now})'.format(times=times,now=current_time))
        time.sleep(time_sleep)
        
except KeyboardInterrupt:
    print('Done!')
    sys.exit(0)