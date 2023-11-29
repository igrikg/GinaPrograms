import requests
import json

def get_config(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Failed to fetch config. Status code: {response.status_code}")

if __name__ == '__main__':
    print(get_config('http://localhost:30000'))