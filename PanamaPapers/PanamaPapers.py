import csv
import json
import requests


# define function to send POST request to IP Street Basic Data Feed endpoint
def search_by_owner(entity_name):
    endpoint = 'https://api.ipstreet.com/v1/data/patent'
    headers = {'x-api-key': "whIz2NmpUf8rGvR2h5oMs9RnPW0byrPG685qAl6e"}
    payload = json.dumps({'q': {"owner": entity_name}})
    r = requests.post(endpoint, headers=headers, data=payload)

    return r


if __name__ == '__main__':

    # Download ICIJ nodes.csv file and save to local disk
    print("Downloading ICIJ nodes file...")
    nodes = requests.get('https://archive.org/download/OffshoreLeaksDatabase/nodes.csv')
    with open('nodes.csv', 'wb') as file:
        file.write(nodes.content)

    # Read nodes.csv file into usable lists
    print("Transforming nodes file...")
    with open('nodes.csv', 'r', encoding="utf-8") as raw:
        reader = csv.reader(raw, delimiter=";")
        entities_raw = list(reader)

    # create empty list for for names only
    entities_name_only = []

    # append names of "ENTITY" nodes to entities_name_only list
    print("Extracting names from raw file...")
    for entity in entities_raw:
        if entity[1] == "ENTITY":
            entities_name_only.append(entity[2])

    print("Beginning to send API calls to IP Street...")
    for name in entities_name_only:
        response = search_by_owner(name)
        print("Patents owned by" + str(name))
        print(response.text)
