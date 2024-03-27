import json
import random
from datetime import datetime

def generate_data():
    # Random Data generator .....
    data_list = []
    for i in range(10):
        data = {"id": i+1,
                "status":random.choice(["delivered","cancelled","order placed"]),
                "amount":round(random.uniform(10,100),2),
                "date":((datetime.now().date()).strftime("%Y-%m-%d"))}
        data_list.append(data)
    return data_list

data_to_save=generate_data()
file_name = ((datetime.now().date()).strftime("%Y-%m-%d"))+"-"+"raw_input.json"
with open(file_name,'w') as json_file:
    json.dump(data_to_save,json_file,indent=4)
