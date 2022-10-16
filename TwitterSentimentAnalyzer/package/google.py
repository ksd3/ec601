import os
from google.cloud import language_v1
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account

path_to_credential="YOUR JSON FILE PATH" #path to your json file 

def get_google_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=path_to_credential
    google_client=language_v1.LanguageServiceClient.from_service_account_json()
    return google_client

def classify_sentiment(score): #split them into ranges
    s=float(score)
    if s>0.5:
        return "very positive"
    elif s>=0.3 and s<=0.5:
        return "positive"
    elif s<-0.3 and s>=-0.3:
        return "netural"
    elif s<-0.3 and s>=-0.5:
        return "negative"
    else:
        return "very negative"

def analyze_tweet(tweet_text, client): #the function that analyzes the tweets
    document=types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)
    sentiment_analysis=google_client.analyze_sentiment(document=document)
    score=sentiment_analysis.document_sentiment.score
    sentiment=classify_sentiment(score)
    return(tweet_text, sentiment, score)
