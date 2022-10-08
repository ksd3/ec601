from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt


def percentage(part, whole):
    return((part/whole)*100)

consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

auth = tweepy.OAuthHandler(consumer_key = consumerKey, consumer_secret = consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

searchTerm = input("Enter the keywords or hashtag: ")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))
tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(noOfSearchTerms)
positive = 0
negative = 0
neutral = 0
polarity =0

for tweet in tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print("polarity of sentiment analysis is " + str(analysis.sentiment.polarity))
    polarity += analysis.sentiment.polarity

    if(analysis.sentiment.polarity == 0):
        neutral += 1
    elif(analysis.sentiment.polarity < 0):
        negative += 1
    elif(analysis.sentiment.polarity > 0):
        positive +=1

print("positive % is ",positive)
print("negative % is ",negative)
print("neutral % is ",neutral)

positive = percentage(positive, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)

positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')


print("How people are reacting on " + searchTerm + " by analyzing " +  str(noOfSearchTerms) + " tweets ")
print(polarity)
if(polarity == 0):
    print("Neutral")
elif(polarity < 0):
    print("Negative")
elif(polarity > 0):
    print("Positive")

labels = ['Positive [' + str(positive) + '%]', 'Negative [' + str(negative) + '%]', 'Neutral [' + str(neutral) + '%]']
sizes = [positive, negative, neutral]
colors = ["yellowgreen", "gold", "red"]
patches, texts = plt.pie(sizes, colors=colors, startangle = 90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reaction on "+searchTerm+ " by analyzing "+ str(noOfSearchTerms)+ " Tweets ")
plt.axis("equal")
plt.tight_layout()
plt.show()
