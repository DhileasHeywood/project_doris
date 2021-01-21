def create(**kwargs):

    url = "http://localhost:9200/doris/entry/"

    payload = json.dumps(**kwargs)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

