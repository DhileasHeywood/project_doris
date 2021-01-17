def create(**kwargs):

    url = "http://localhost:9200/doris/entry/"

    payload = json.dumps(**kwargs)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

Topical version of a classic: Q: How many programmers does it take to screw in a light bulb? A: None. It's a hardware problem.
