import requests
import yaml
import json
import re
from datetime import datetime, timedelta

bearer_path="REPLACE THIS WITH THE PATH TO YOUR YAML FILE" #make this the yaml format:
# twitter_api:
#       bearer_token: <your token>
#       api_key: <your api key> and so on

def get_bearer_token(): #function that gets the bearer token from the yaml file
    with open(bearer_path) as file:
        other_keys=yaml.safe_load(file)
    return other_keys['twitter_api']['bearer_token']

def create_headers(): #function that makes a header to request the api to give access
    bearer_token=get_bearer_token()
    headers={}
    headers["Authorization"]="Bearer {}".format(bearer_token)
    return headers

def topic_to_query(topic): #transforms a topic into a format for querying twitter - the topic should in general be something like 'Pennsylvania Avenue', separated by spaces
    list_of_topics=topic.split()
    query=''
    for t in list_of_topics:
        query+=t+'%20'
    return query

def url_creator(name, additional_stuff_to_search=''): #this function returns the url to pass to the twitter api for the request
    url_template='https://api.twitter.com/2/tweets/search/recent?query='
    name_url=topic_to_query(name)
    query_parameter_setter='lang%3Aen%20-is%3Aretweet%20-is%3Areply'
    return url_template+name_url+query_parameter_setter+additional_stuff_to_search

def get_date(number_of_hours): #the input is the number of hours to get
    if number_of_hours <= 0:
        return 'Your hour count cannot be a non-positive number'
    time_right_now=datetime.today()
    time_to_gmt=timedelta(4/24-(1/60)/24)
    time_right_now=time_right_now+time_to_gmt
    time_in_the_past=timedelta(number_of_hours/24)
    date_to_return=time_right_now-time_in_the_past
    return (time_right_now.strftime('%Y-%m-%dT%H:%M:%S.000Z'),date_to_return.strftime('%Y-%m-%dT%H:%M:%S.000Z'))

def parameter_creator_function(maximum_numer_of_results=1000,starting_time={},ending_time={}): #to probe tweets you gotta start with this
    parameters={
            'starting_time': starting_time,
            'ending_time': ending_time,
            'maximum_numer_of_results' : maximum_numer_of_results,
            'tweet.fields': 'created_at,public_metrics',
        }
    return parameters

def connect_to_twitter_endpoint(url,headers,params=None,next_token={}): #this is where you actually generate the parameters
    params['next_token']=next_token
    response=requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_the_next_token(api_response):
    return api_response['meta']['next_token']

def show_tweets(api_response): #for convenience
    print(json.dumps(api_response['data'], indent= 4, sort_keys=True))
    

class Tweet: #headache saver
    def __init__(self, json_tweet):
        self.date=json_tweet['created_at'][0:10]
        self.time=json_tweet['created_at'][11:16]
        self.text=json_tweet['text']
        self.like_count=json_tweet['public_metrics']['like_count']
        self.retweet_count=json_tweet['public_metrics']['retweet_count']
    
    def get_date(self):
        return self.time+'-'+self.date

    def get_likes(self):
        return self.like_count

    def clean_tweet(self):
        '''Clean up the text of the tweet. Get rid of https links at the end. And, make time logic format dd-mm-yyyy'''
        self.text=re.sub(r"http\S+", "", self.text)
        self.date=self.date[8:10]+'-'+self.date[5:7]+'-'+self.date[0:4]
    
    def __str__(self):
        ret_str="{}\n".format(self.text)
        ret_str+="Number of Likes: {} Number of Retweets:{}\n".format(str(self.like_count), str(self.retweet_count))
        ret_str+="Date: {} Time: {}\n".format(self.date, self.time)
        return ret_str
