import http.client
import json

HOST = 'v3.football.api-sports.io'
HEADER = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "52baf279811d2f16e0303bb8ba1a73f1"
}

def get_fixtures():
    conn = http.client.HTTPSConnection(HOST)
    conn.request('GET', '/fixtures?league=4&season=2020', headers=HEADER)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))