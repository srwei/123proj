import json
import requests as req


words = set(['politic'])

types = {'Person':'PERSON', 'Event':'EVENT', 'Organization':'ORG', 'Place':'LOC'}

def is_political(ent_text, ent_type):

    api_key = 'AIzaSyAMSkyNxAUbhtlvfWOKGJAO8w1hbj2WXC0'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = [
        ('query', ent_text),
        ('limit', 5),
        ('indent', True),
        ('key', api_key)
    ]


    page = req.get(url = service_url, params = params)
    data = json.loads(page.text)
    out = None
    score = 0
    for item in data['itemListElement']:
        description = None
        try:
            description = item['result']['detailedDescription']['articleBody'] + ' ' + item['result']['name']

        except:
            description = item['result']['description']

        political = sum([word in description for word in words])
        right_type = sum([types[t] == ent_type for t in item['result']['@type'] if t in types.keys()])

        if political and right_type:
            if political > score:
                out = (item['result']['@id'], item['result']['name'])
                score = political
    return out
