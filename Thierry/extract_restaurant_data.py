import requests
import json



def get_businesses(location, term, api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'

    data = []
    for offset in range(0, 1000, 50):
        params = {
            'limit': 50, 
            'location': location.replace(' ', '+'),
            'term': term.replace(' ', '+'),
            'offset': offset
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 400:
            print('400 Bad Request')
            break

    return data

data = get_businesses("Québec", "restaurants", "a7TB6FBUPiikTRx7EDqP8h5PgIEVxkpYfxwlqxozura1vpGWjO5Ab4M3zbop4Pm_ze7nqAlwJ-FvJxVU5F1o2Lcg5YL6RZ5gq2-qyHR2QfaqmMlbG77yTEWrixxKYXYx")
json = json.dumps(data)

print(len(data))

#with open("restaurant_data.json", "w") as f:
#    f.write(json)
