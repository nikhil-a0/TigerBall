import json

with open('undergrad_list.json', 'rw') as file:
    json_object = json.load(file)
    undergradList = json.loads(json_object)

    for dictionary in undergradList:
                del dictionary['last_name']
                del dictionary['class_year']
                del dictionary['res_college']
                del dictionary['hometown']
                del dictionary['home_lat']
                del dictionary['home_lng']
                del dictionary['dorm_number']
                del dictionary['dorm_building']
                del dictionary['dorm_lat']
                del dictionary['dorm_lng']
                del dictionary['major_type']
                del dictionary['major_raw']
                del dictionary['major_code']
                del dictionary['photo_link']
                del dictionary['phone_raw']
                del dictionary['mailbox']
                del dictionary['organization_raw']
                del dictionary['athletics_raw']
                del dictionary['athletics_url_raw']
                del dictionary['alias']
                del dictionary['photo_base64']

    final = json.dumps(undergradList, indent=2)
    print(final)
    
                
                
                

