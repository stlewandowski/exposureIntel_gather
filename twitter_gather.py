import time
import configparser
import requests
from requests.auth import AuthBase
import datetime
import json

# config parser
config = configparser.ConfigParser()
config.read('conf.ini')
consumer_key = config['Twitter']['consumer_key']
consumer_secret = config['Twitter']['consumer_secret']

stream_url = "https://api.twitter.com/labs/1/tweets/stream/filter"
rules_url = "https://api.twitter.com/labs/1/tweets/stream/filter/rules"

sample_rules = [
    {'value': 'dog has:images', 'tag': 'dog pictures'},
    {'value': 'cat has:images -grumpy', 'tag': 'cat pictures'},
]


# Gets a bearer token
class BearerTokenAuth(AuthBase):
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={'grant_type': 'client_credentials'},
            headers={'User-Agent': 'TwitterDevFilteredStreamQuickStartPython'})

        if response.status_code is not 200:
            raise Exception(f"Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

        body = response.json()
        return body['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
        r.headers['User-Agent'] = 'TwitterDevFilteredStreamQuickStartPython'
        return r


'''
def get_all_rules(auth):
  response = requests.get(rules_url, auth=auth)

  if response.status_code is not 200:
    raise Exception(f"Cannot get rules (HTTP %d): %s" % (response.status_code, response.text))

  return response.json()


def delete_all_rules(rules, auth):
  if rules is None or 'data' not in rules:
    return None

  ids = list(map(lambda rule: rule['id'], rules['data']))

  payload = {
    'delete': {
      'ids': ids
    }
  }

  response = requests.post(rules_url, auth=auth, json=payload)

  if response.status_code is not 200:
    raise Exception(f"Cannot delete rules (HTTP %d): %s" % (response.status_code, response.text))

def set_rules(rules, auth):
  if rules is None:
    return

  payload = {
    'add': rules
  }

  response = requests.post(rules_url, auth=auth, json=payload)

  if response.status_code is not 201:
    raise Exception(f"Cannot create rules (HTTP %d): %s" % (response.status_code, response.text))

def stream_connect(auth):
  response = requests.get(stream_url, auth=auth, stream=True)
  for response_line in response.iter_lines():
    if response_line:
      pprint(json.loads(response_line))
'''
bearer_token = BearerTokenAuth(consumer_key, consumer_secret)
print(bearer_token)
url = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json'
url2 = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=MarketWatch&count=50'
dt_now = datetime.datetime.now()
dt_now_str = dt_now.strftime('%Y%m%d%H%M')
six_hr = dt_now - datetime.timedelta(hours=12)
six_hr_str = six_hr.strftime('%Y%m%d%H%M')
payload1 = {"query": "#databreach -RT", "maxResults": 100, "fromDate": six_hr_str, "toDate": dt_now_str}
payload2 = {"query": "#leak -RT", "maxResults": 100, "fromDate": six_hr_str, "toDate": dt_now_str}
payload3 = {"query": "#dataleak -RT", "maxResults": 100, "fromDate": six_hr_str, "toDate": dt_now_str}
payload4 = {"query": "#ghostbin -RT", "maxResults": 100, "fromDate": six_hr_str, "toDate": dt_now_str}
payload5 = {"query": "#pastebin -RT", "maxResults": 100, "fromDate": six_hr_str, "toDate": dt_now_str}
timelinePayload = {"screen_name": "MarketWatch", "count": 50}
#response = requests.post(url2, auth=bearer_token, json=timelinePayload)
#response = requests.get(url2, auth=bearer_token)

#tfile = r"c:\users\slewa\Downloads\twitter_test_databreach_{}.txt".format(dt_now_str)
#tfile = r"c:\users\slewa\Downloads\twitter_test_marketwatch_{}.txt".format(dt_now_str)
#wt = open(tfile, 'w', encoding='utf-8')
tweetList = ["MarketWatch", "SeekingAlpha", "CNBC", "Benzinga", "WSJmarkets", "Stocktwits"]
logfile = r"c:\users\slewa\Downloads\twitter_timeline_status.log"
runNum = 0
while True:
    for account in tweetList:
        lf = open(logfile, 'a')
        dt_now_str2 = dt_now.strftime('%Y%m%d%H%M')
        print("="*75)
        lf.write("="*75)
        lf.write('\n')
        lf.write(f"Run: {str(runNum)}")
        lf.write('\n')
        print(f"Starting run: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lf.write(f"Starting run: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        url2 = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=50".format(account)
        response = requests.get(url2, auth=bearer_token)
        print(response.status_code)
        lf.write(str(response.status_code) + '\n')
        print(type(response))
        lf.write(str(type(response)))
        lf.write("\n")
        #wt.write(str(response.status_code) + '\n')
        #wt.write(str(response) + '\n')
        res = response.json()
        #print(len(res['results']))
        #wt.write("Result #: {}".format(len(res['results'])))
        #wt.write('\n')
        for item in res:
            print("=" * 50)
            #wt.write("=" * 50 + '\n')
            #wt.write(item['text'])
            #wt.write('\n')
            print(item['text'])
            #print(str(item['entities']))
            if len(item['entities']['hashtags']) > 0:
                print(str(item['entities']['hashtags']))
            print(f"Retweet count: {str(item['retweet_count'])}")
            try:
                print(f"URLs: {item['entities']['urls'][0]['expanded_url']}")
            except IndexError:
                print("URLs: None")
                pass
        jfile = r"c:\users\slewa\Downloads\twitter_test_{}_{}.json".format(account, dt_now_str2)
        with open(jfile, 'w', encoding='utf-8') as wj:
            json.dump(res, wj)
        print(f"Finished {account} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lf.write(f"Finished {account} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lf.close()
        runNum += 1
        time.sleep(6)

#print(res)
#jfile = r"c:\users\slewa\Downloads\twitter_test_marketwatch_{}.json".format(dt_now_str)
#with open(jfile, 'w', encoding='utf-8') as wj:
#    json.dump(res, wj)
'''
# this will print the original URL from the tweets:
# requests.get("https://t.co/GSnsMHSzGT").url
# expanded URL is in 'urls'[0]['expanded_url']
# get URLs, follow them, screenshot the data maybe

def setup_rules(auth):
  current_rules = get_all_rules(auth)
  delete_all_rules(current_rules, auth)
  set_rules(sample_rules, auth)


# Comment this line if you already setup rules and want to keep them
setup_rules(bearer_token)

# Listen to the stream.
# This reconnection logic will attempt to reconnect when a disconnection is detected.
# To avoid rate limites, this logic implements exponential backoff, so the wait time
# will increase if the client cannot reconnect to the stream.
timeout = 0
while True:
  stream_connect(bearer_token)
  sleep(2 ** timeout)
  timeout += 1
'''
