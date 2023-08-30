import pprint

import requests
import json

def api_request(*args):
    if len(args) == 2:
        api_type = args[0]
        args_url = args[1]
        body = []
    elif len(args) == 3:
        api_type = args[0]
        args_url = args[1]
        body = args[2]

    body = json.dumps(body, ensure_ascii=False, indent="\t")
    # print(body)
    base_url = "http://0.0.0.0/******"
    url = base_url + args_url
    # headers = def_make_header.get_header()
    headers = {
        "Content-type": "application/json"
    }

    print('-----def_api_req-----')
    print(f'URI : {url}')
    print(f'headers : {headers}')
    print(f'body : {body}')

    try:

        if api_type == 'get':
            response = requests.get(url, headers=headers, data=body)
        elif api_type == 'post':
            response = requests.post(url, headers=headers, data=body)
        elif api_type == 'put':
            response = requests.put(url, headers=headers, data=body)
        elif api_type == 'delete':
            response = requests.delete(url, headers=headers, data=body)

        if response.status_code == 200:
            print(response.status_code, 'Request OK')
        elif response.status_code == 204:
            print(response.status_code, 'Error:[204], No Content')
        elif response.status_code == 201:
            print(response.status_code, 'Request OK No Response [POST]')
        elif response.status_code == 400:
            print(response.status_code, 'Error:[400], Bad Request')
        elif response.status_code == 401:
            print(response.status_code, 'Error:[401], Unauthorized')
        elif response.status_code == 403:
            print(response.status_code, 'Error:[403], Forbidden')
        elif response.status_code == 405:
            print(response.status_code, 'Error:[405], Method Not Allowed')
        elif response.status_code == 406:
            print(response.status_code, 'Error:[406], Not Acceptable')
        elif response.status_code == 408:
            print(response.status_code, 'Error:[408], Request Time out, Server Busy')
        elif response.status_code == 503:
            print(response.status_code, 'Error:[503], Service Unavaliable, Cannot Connect with server/API')


        else:
            print(response.status_code, 'Request Fail')

        if response.text:

            # print(f'response : {response}')
            contents = response.text
            # print(f'contents  = {contents}')
            json_ob = json.loads(contents)
            # print(f'json_ob = {json_ob}')
            print('---------------------')
        else:
            json_ob = ''


    except requests.exceptions.Timeout as errd:
        print("Timeout Error : ", errd)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting : ", errc)

    except requests.exceptions.HTTPError as errb:
        print("Http Error : ", errb)

    # Any Error except upper exception
    except requests.exceptions.RequestException as erra:
        print("AnyException : ", erra)

    return json_ob
