from req_lib import getAllUndergrads
import json
from sys import stderr

if __name__ == "__main__":
    
    try: 
        req = getAllUndergrads()
        if req.ok:
            print(req.json())
            # print(undergradList)
            # undergradList = json.loads(req.json())
            # for dictionary in undergradList:
            #     del dictionary['first_name']
            #     del dictionary['last_name']
            #     del dictionary['photo_base64']
            #     del dictionary['hometown']
            #     del dictionary['dorm_lat']
            #     del dictionary['dorm_lng']
            #     del dictionary['dorm_building']
            #     del dictionary['dorm_number']
            #     del dictionary['class_year']
            #     del dictionary['athletics_raw']
            #     del dictionary['athletics_url_raw']
            #     del dictionary['major_type']
            #     del dictionary['home_lng']
            #     del dictionary['home_lat']
            #     del dictionary['res_college']
            #     del dictionary['hometown']
            #     del dictionary['photo_link']
            #     del dictionary['phone_raw']
            #     del dictionary['mailbox']
            #     del dictionary['organization_raw']
            # final = json.dumps(undergradList, indent=2)
            # print(final)
    except Exception as ex:
        print(ex, file=stderr)