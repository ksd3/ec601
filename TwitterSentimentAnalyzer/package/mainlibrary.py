from ipywidgets.widgets.widget_box import VBox
import pandas as pd
from .twitter import *
from .google_api import *
from prettytable import PrettyTable
import ipywidgets as widgets
import time

#the main library


class topic:

    __POS='Positive'
    __NEUT='Neutral'
    __NEG='Negative'

   
    def __init__(self, topic_name): #the input argument is the topic string and generates a topic class for analysis
        self.topic_name=topic_name
        self.__analyzed_tweet_count=0
        self.__positive_tweet_count=0
        self.__negative_tweet_count=0
        self.__neutral_tweet_count=0
        self.__hours=0
        self.__start_time=None
        self.__end_time=None
        self.__examples=None
    
    
    def __str__(self):
        return '{}, tweets: {}, positive:{}, negative: {}, neutral: {}'.format(self.topic_name, self.tweet_counter(), self.positive_tweet_counter(), self.negative_tweet_counter(), self.netural_tweet_counter())

    def reset(self):
        self.__analyzed_tweet_count=0
        self.__positive_tweet_count=0
        self.__negative_tweet_count=0
        self.__neutral_tweet_count=0
        self.__hours=0
        self.__start_time=None
        self.__end_time=None
        self.__examples=None

    def tweet_counter(self):
        return self.__analyzed_tweet_count

    def positive_tweet_counter(self):
        return self.__positive_tweet_count
    
    def negative_tweet_counter(self):
        return self.__negative_tweet_count
    
    def netural_tweet_counter(self):
        return self.__neutral_tweet_count

    def start_time(self):
        neat_start=self.__start_time[11:16]+'-'+self.__start_time[8:10]+ '-'+ self.__start_time[5:7]+'-'+self.__start_time[0:4]
        return neat_start

    def end_time(self):
        neat_end=self.__end_time[11:16]+'-'+self.__end_time[8:10]+ '-'+ self.__end_time[5:7]+'-'+self.__end_time[0:4]
        return neat_end
    
    def show_stats(self): #function to show stats
        ppos=str(round((self.__positive_tweet_count/self.__analyzed_tweet_count)*100, 2))+'%'
        pneg=str(round((self.__negative_tweet_count/self.__analyzed_tweet_count)*100, 2))+'%'
        pneut=str(round((self.__neutral_tweet_count/self.__analyzed_tweet_count)*100, 2))+'%'

        table=PrettyTable()
        table.title='Statistic of sentiment for '+self.topic_name
        table.field_names=['Sentiment', 'Count', 'Percentage']
        table.add_row(['Pos', self.__positive_tweet_count, ppos])
        table.add_row(['Neg', self.__negative_tweet_count, pneg])
        table.add_row(['Neu', self.__neutral_tweet_count, pneut])

        print('_________________________')
        print('Results')
        print(table)
        print()
        print("{} total tweets in the last {} hours resulted in {} positive, {} negative, {} neutral".format(str(self.__analyzed_tweet_count), str(self.__hours), ppos, pneg, pneut))


    def __create_twitter_query(self, hours): #function to create the twitter query
        headers=create_headers()
        url=create_url(self.name)
        self.__end_time, self.__start_time=get_dates(hours)
        parameters=create_params(max_results=100, start_time=self.__start_time, end_time=self.__end_time)

        print("Query for twitter api: {}".format(url))

        return (url, headers, parameters)
    
    def __get_tweet_batch(self, url, headers, parameters, next_token={}, iteration=0):
        """Returns a batch of tweets and next token for continuation of analysis"""
        tweet_batch=connect_to_endpoint_twitter(url, headers, parameters, next_token=next_token)
        try:
            next=tweet_batch['meta']['next_token']
        except KeyError:
            next=None
        return (tweet_batch, next)


    def analyze_tweets(self, hour_count=1, max_time=30,  display=True):

        if hour_count <= 0:
            print("Hour count can't be negative or 0")
            return
        else:
            #prepare
            self.__hours=hour_count
            google_client=get_google_client()
            print("Google api client connection established...\n")

            url, headers, parameters=self.__create_twitter_query(hour_count)

            print("\nAnalyzing....\n")

            tweet_dict={'sentiment':[], 'text':[], 'score':[], 'like_count':[], 'date':[]}    #dictionary for examples
            next={}
            iteration=0

            #max time boundary for analysis
            time_max=time.time()+120*max_time
            valid=True

            try:
                while next!=None:

                    if time.time() > time_max:
                        print('You went beyond the maximum time!')
                        break

                    tweet_batch, next=self.__get_tweet_batch(url, headers, parameters, next_token=next, iteration=iteration)
                    
                    #check if batch is empty
                    if tweet_batch['meta']['result_count'] == 0:
                        print("No results for this query")
                        valid=False
                        break
                    
                    #prevent duplicates at end/beginning of batch
                    if iteration == 0:
                        data=tweet_batch['data']
                    else:
                        data=tweet_batch['data'][1:]

                    #analyze sentiment of batch
                    for response in data:
                        try:
                            tweet=Tweet(response)
                            tweet.clean_tweet()
                            tweet_dict['date'].append(tweet.get_date())
                            tweet_dict['like_count'].append(tweet.get_likes())
                            
                            text, feeling, score=analyze_tweet(tweet.text, google_client)
                            tweet_dict['text'].append(text)
                            tweet_dict['score'].append(round(float(score),2))

                            if feeling=='positive':
                                tweet_dict['sentiment'].append(self.__POS)
                                self.__positive_tweet_count+=1
                            elif feeling=='negative':
                                tweet_dict['sentiment'].append(self.__NEG)
                                self.__negative_tweet_count+=1
                            else:
                                tweet_dict['sentiment'].append(self.__NEUT)
                                self.__neutral_tweet_count+=1

                            self.__analyzed_tweet_count+=1
                            
                        except Exception as e:
                            print(e)

                    #go to next batch at beginning of loop
                    iteration += 1
                    print("Tweets looked at: {}".format(self.__analyzed_tweet_count))

            except KeyboardInterrupt:
                self.reset()
                print("You terminated the analysis!")
                return

        #create example dataframe
        if valid:
            self.__examples=pd.DataFrame(data=tweet_dict)
            self.__examples=self.__examples.drop_duplicates()
            self.__examples=self.__examples.sort_values(by='like_count', ascending=False).reset_index(drop=True)

            print()
            print("Completed Analysis")
            print()

            if display:
                self.show_stats()

    def summary(self): #shows summary
        pos=self.examples_positive()
        neg=self.examples_negative()
        neut=self.examples_neutral()
        self.show_stats()
        print('-------------------------------------')
        print('Example tweets')
        print()
        print('Positive')
        pos.next(header=False)
        print('-------------------------------------')
        print('Negative')
        neg.next(header=False)
        print('-------------------------------------')
        print('Neutral')
        neut.next(header=False)


    def examples_all(self, page_size=3): #returns an example object
        return Example(self.__examples, page_size=page_size)

    def examples_positive(self, page_size=3): #returns a positive example object
        positive=self.__examples[self.__examples['sentiment'] == self.__POS].reset_index(drop=True)
        return Example(positive, page_size=page_size, sentiment='Positive')

    def examples_negative(self, page_size=3): #returns an example negative object
        negative=self.__examples[self.__examples['sentiment'] == self.__NEG].reset_index(drop=True)
        return Example(negative, page_size=page_size, sentiment='Negative')

    def examples_neutral(self, page_size=3): #returns an example neutral object
        neutral=self.__examples[self.__examples['sentiment'] == self.__NEUT].reset_index(drop=True)
        return Example(neutral, page_size=page_size, sentiment='Neutral')



class Example: #ipywidget is used to make the objects easy to flip through

    def __init__(self, data, page_size, sentiment=''):
        self.__example=data
        self.__current_index=0
        self.__sentiment=sentiment
        self.__page_size=page_size
        self.__example_viewer=widgets.Output(layout={'border': '1px solid black'})

    def clear(self): #annoying viewer resetter
       self.__example_viewer=widgets.Output(layout={'border': '1px solid black'})
       self.__current_index=0

    def next(self, header=True): #next example shower
        if header:
            self.__example_viewer.append_display_data(widgets.HTML('<b>Example '+self.__sentiment+' Tweets</b>'))

        #creating viewer content
        for i in range(self.__current_index, self.__current_index+self.__page_size):
            try:
                tweet=widgets.HTML(" <i>'{}'</i><br>".format(self.__example.at[i,'text']))
                tweet_feel=self.__example.at[i,'sentiment']
                sentiment=widgets.HTML("<b>{}</b> ({}) | ".format(tweet_feel, str(self.__example.at[i,'score'])))
                likes=widgets.HTML('{} likes | '.format(str(self.__example.at[i,'like_count'])))
                date=widgets.HTML('{}'.format(self.__example.at[i,'date']))
                metrics=widgets.HBox([sentiment, likes, date])
                info=VBox([tweet, metrics])
                self.__example_viewer.append_display_data(info)
            except KeyError:
                break
        #update index for next call
        self.__current_index += self.__page_size


def compare(topic1, topic2): #comparitive statistics for two topics
    ppos1=str(round((topic1.positive_tweet_counter()/topic1.tweet_counter())*100, 2))+'%'
    pneg1=str(round((topic1.negative_tweet_counter()/topic1.tweet_counter())*100, 2))+'%'
    pneut1=str(round((topic1.netural_tweet_counter()/topic1.tweet_counter())*100, 2))+'%'

    ppos2=str(round((topic2.positive_tweet_counter()/topic2.tweet_counter())*100, 2))+'%'
    pneg2=str(round((topic2.negative_tweet_counter()/topic2.tweet_counter())*100, 2))+'%'
    pneut2=str(round((topic2.netural_tweet_counter()/topic2.tweet_counter())*100, 2))+'%'

    table=PrettyTable()
    table.title='Statistic of sentiment for '+topic1.name+' vs. '+topic2.name
    table.field_names=['Sentiment', 'Percentage '+topic1.name, 'Percentage '+topic2.name ]
    table.add_row(['Positive', ppos1, ppos2])
    table.add_row(['Negaitve', pneg1, pneg2])
    table.add_row(['Neutral', pneut1, pneut2])

    print('-------------------------------------')
    print('RESULTS')
    print(table)
    print()
    print("Of {} tweets on {} from {} to {}, {} were positive, {} were negative, {} were neutral".format(str(topic1.tweet_counter()), topic1.name,str(topic1.start_time()), str(topic1.end_time()), ppos1, pneg1, pneut1))
    print("Of {} tweets on {} from {} to {}, {} were positive, {} were negative, {} were neutral".format(str(topic2.tweet_counter()), topic2.name, str(topic2.start_time()), str(topic2.end_time()), ppos2, pneg2, pneut2))
