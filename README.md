# EC601 Project 02 - Twitter Sentiment Analyzer

## IMAGES AVAILABLE IN PYTHON NOTEBOOKS IN THE TEST FOLDER!

# Part 1 A) The Twitter API

The Twitter API gives you access to tweets and lets you pull tweets from the website for analysis. The API is well documented. It requires you to run every command through a terminal and each command has complicated syntax. Because of this, it is easier to use a wrapper to analyze tweets. For this purpose, we use Tweepy, the best wrapper available to the public. 

To get access to the API, you need to make a Twitter Developer Account. You then need to create a new project and a new application inside that project. You are initially given Essential access to Twitter, but you can apply for Elevated access (which is what is needed for Tweepy to work.) You also need to give the app permission to post, reply, retweet, follow, and so on. You're essentially using Twitter from a terminal rather than a webpage or app. Once you have granted permission, you should regenerate your API keys and save them. In general, your API keys should be protected, but this project does not protect them for convenience. You import them with a YAML file.

To install the latest version of Tweepy, I ran <code>pip install git+https://github.com/tweepy/tweepy.git</code> to get the latest version of Tweepy. This is required because tutorials online are generally available for Tweepy versions 3.x while the default documentation is for Tweepy version 4.x.

I then created a Jupyter Notebook to test Tweepy. I made a new Twitter account and did the following:
1. I was able to get my timeline (which consisted entirely of Bloomberg tweets). 
2. I was able to post tweets (this is where I realized that the initial API key was read-only and needed to be regenerated). I also realized that this prevented me from posting the same tweet twice.
3. I was able to get the last 20 followers of a public Twitter user. (Tarik 'tarik' Celik). I suspect that this method does not work on private accounts unless they accept your follow request as well. I was also able to get tarik's display name, description, and location.
4. I was able to follow and unfollow users with the <code>create\_friendship()</code> and <code>destroy\_friendship()</code> functions.
5. I was able to block and unblock users with the <code>create\_block()</code> and <code>destroy\_block()</code> functions.
6. I was able to like my own tweets.
7. When a user was not found, I was able to get a Tweepy error. However I did not get any error code, which may be a feature of the environment I set up.
8. During my probing, I never had an instance where Twitter was rate limited or down, so I simply ignored these cases. However there are functions to avoid this that change names with the documentation.
9. I was able to pull tweets from a user. However tyhe Twitter API itself does not allow you to pull private tweets. 
10. I was able to see trends by specifying a latitude and longitude.
11. I then used the <code>Cursor()</code> function in Tweepy to actually pull tweets and save them to a pandas dataframe. I could search for tweets featuring a certain keyword and pull the most recent 300, 500, and so on. However this never used my quota of 2 million tweets, which is surprising.

# Part 1 B) The Google NLP API

The Google NLP API gives you access to Google's powerful closed-source NLP tools. You could use these tools for sentiment analysis. However it turned out that setting up the API took way more effort than what it was worth in the end. You register for the Google API and generate a new key that downloads a JSON file which you then use to gain access.

I pulled tweets from tarik and performed sentiment analysis on them with the API. To pull the tweets I used Tweepy. I also cleaned up the tweets of numbers, emojis, links, and unncessary whitespaces with Regex. I was able to get sentiment scores per tweet. The results of my work with the API are available in a Jupyter Notebook

# Part 1 C) Botometer

The Botometer API is interesting and allows you to determine whether a user was a bot or not. I tested it on tarik and accounts from botwiki.org. The API was able to confirm that tarik was not a bot and FotosElPopular was a bot. The API also returned what kind of bot they were (political, reposting, and so on) which was interesting. While I didn't end up using this in my final package it was still an interesting exercise. 

# Part 2) Product Mission

The aim of this project is to provide a way to analyze Tweets for a given top, seeing how the sentiment of a topic changed historically.

# User Stories

As a politician, I want to see whether my voter base likes or dislikes a topic more compared to the past.

As a marketer, I want to know whether a test product is well-received or not compared to other products.

As a psychologist, I want to investigate whether mental states have changed over time.

As an urban planner, I want to know the opinion of a certain area.

As a researcher, I want to see how my own algorithms compare to state-of-the-art systems..

# The MVP:

A package that gets tweets about a certain topic and some visualizations about how it is received.

# Trying to make your own NLP

I tried to make my own Sentiment Analyzer to compare its results with those provided by the Google NLP. I used the ST140 dataset provided by Stanford university. There are 1.6 million tweets in this dataset categorized according to their sentiment. I then loaded these tweets into a pandas dataframe and tokenized them using the <code>nltk</code> library. I found that the library struggled with emojis so I had to use the latin-1 typeset in order to correctly read the data. Unfortunately, trying to read the entire dataset crashed the system and so I tried it with smaller pieces of the data. However, this resulted in very low accuracies and therefore I do not think this is the correct solution. More computing power is the requirement but the SCC does not have the package versions I need and I do not know how what would happen if my function resulted in infinite loops. 

For the algorithms, I used linear regression, logistic regression, random forest, naive bayes, and LinearSVC. Out of these, linear regression failed isntantl as it did not like floats, which are needed to classify the sentiment. The other four managed to work but were not particularly accurate, as they were trained on a limited amount of tweets. I ended up overcorrecting every time I modified a program. There is scope for improvement here but at the moment the Google NLP classifier is the best. The confusion matrice images are available in the notebooks.



