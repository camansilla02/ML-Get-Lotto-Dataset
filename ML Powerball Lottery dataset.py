## Fetch api data and transform it to json and convert to data frame

import pandas as pd, os, requests,re,numpy,json
from sklearn import tree

def filter_list(date_pattern,data:list):
    new_lst =[]
    for l in data:
        if re.match(date_pattern,l['draw_date']):
           new_lst.append(l)
    
    
    return new_lst
             
          

def parse_api_data(api_url):
    date_pattern = "^([0-9]|1[0-2])\\/([1-9]|[12][0-9]|3[01])\\/[0-9]{4}$"
    win_nums_patt = "^(?:[0-9]|[1-9][0-9])(?:,(?:[0-9]|[1-9][0-9])){4}$"
    pb_patt = "^[0-9]|[1-9][0-9]$"
    get_lotto_api = requests.get(url=api_url)
    arr_of_obj_str='''{"lotto_hist":[]}'''
    data = json.loads(arr_of_obj_str)
    if get_lotto_api.status_code == 200:
        lotto_hist= get_lotto_api.text[23:]
        for l in  lotto_hist.split():
            #Let's look at historical August powerball winning numbers
                #date match (draw_date,winning_nums,pb) 
            #print(l)
            if re.match(date_pattern, l.strip(';')):
                    draw_date=l.strip(';')

            elif re.match(win_nums_patt,l.strip(';')):

                 #list(zip(*l.strip(';').splitlines()))
                 winning_nums = l.strip(';').split(',')
                 num_one, num_two,num_three,num_four,num_five= winning_nums
                 #print(num_one, num_two,num_three,num_four,num_five)
                         
                       
                           

            elif re.match(pb_patt,l.strip(';')):
                    pb=l.strip(';')
            
            
                    new_obj=dict(draw_date=draw_date,winning_num_one=int(num_one),winning_num_two=int(num_two),winning_num_three=int(num_three), winning_num_four=int(num_four),winning_num_five=int(num_five), pb=int(pb))

                    #print(draw_date,num_one, num_two,num_three,num_four,num_five,pb) 
                    data['lotto_hist'].append(new_obj)
    return  data

          

data_set_result= parse_api_data(api_url="https://www.valottery.com/api/v1/downloadall?gameid=20")

lotto_hist=data_set_result['lotto_hist'] 

#october data
filter_date_pattern= "^[1][0]\\/([1-9]|[12][0-9]|3[01])\\/202[3-4]$"
filtered_results= filter_list(filter_date_pattern,lotto_hist)


df= pd.DataFrame(filtered_results)
df.head(20)
