import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json
import nltk
nltk.download('all')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from wordcloud import WordCloud
import string
from collections import Counter

# Twitter API
import tweepy

# import time
import time

# Azure 
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import asyncio

# load data from a json file (test prupose only)
def load_data():
    with open('./tweets_uber.json') as f:
        data = json.load(f)
    return data

# Load data from our Azure Cosmos server
def load_data_azure(company , nbr_of_tweets):
    # <add_uri_and_key>
    with open('./venv/keys.json') as f:
        keys = json.load(f)
    endpoint = keys['endpoint']
    key = keys['key']

    # <define_database_and_container_name>
    database_name = 'DataCampCOS'
    container_name = 'Tweets'

    # <create_cosmos_client>
    client = CosmosClient(endpoint, key)


# Function to load the data from twitter API
@st.cache
def get_data_twitterAPI(company,nbr_of_tweets):
    # get keys from keys.json
    with open('./venv/keys.json') as f:
        keys = json.load(f)

    # get the keys from the dictionary
    consumer_key = keys['consumer_key']
    consumer_secret = keys['consumer_secret']
    access_token = keys['access_token']
    access_token_secret = keys['access_token_secret']

    # authentification to twitter with twitter api v2
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    i= 0
    tweets_json = []
    while i < nbr_of_tweets/100:
        tweets = api.search_tweets(q=company + " -RT -giveaway -win -gift", count = 100,tweet_mode="extended",lang="en")
        for tweet in tweets:
            tweets_json.append(tweet._json)
        i += 1 
    return tweets_json

def load_data_twitter(company,nbr_of_tweets):
    data = get_data_twitterAPI(company,nbr_of_tweets)
    succes = st.success("{} Tweets loaded".format(nbr_of_tweets))
    return data

# 
def wordcloud(text):
    plt.figure(figsize=(10, 7))
    fig, ax = plt.subplots()
    plt.axis('off')
    wordcloud = WordCloud(background_color='white', width=800, height=500, random_state=21, max_font_size=110).generate(text)
    ax.imshow(wordcloud, interpolation="bilinear")
    st.pyplot(fig)

# 
def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [word for word in tokens if word not in stopwords.words('english')]
    return text

def delete_same_tweets(data):
    removed = 0
    tweets = []
    for tweet in data:
        if tweet['full_text'] not in tweets:
            tweets.append(tweet)
        else:
            removed += 1
    # print the number of tweets deleted
    if removed > 0:
        msg_deleted_tweets = st.warning("{} tweets deleted".format(removed))
        time.sleep(4)
        msg_deleted_tweets.empty()
    return tweets

# Function to do all the analysis
def dataAnalyse(data,company):
    # We use this function to delete same tweets
    data = delete_same_tweets(data)

    sia = SentimentIntensityAnalyzer()
    for tweet in data:
        tweet['scores'] = sia.polarity_scores(tweet['full_text'])
        tweet['compound'] = tweet['scores']['compound']
        tweet['neg'] = tweet['scores']['neg']
        tweet['neu'] = tweet['scores']['neu']
        tweet['pos'] = tweet['scores']['pos']

    if data:
        df = pd.DataFrame.from_dict(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Positive Tweets", df[df['compound'] > 0.05].shape[0])
    col2.metric("Number of Negative Tweets", df[df['compound'] < -0.05].shape[0])
    col3.metric("Number of Neutral Tweets", df[(df['compound'] >= -0.05) & (df['compound'] <= 0.05)].shape[0])

    st.header('Sentiment Polarity of ' + company + ' Tweets')
    fig = px.scatter(df, x='neg', y='pos', color='compound')
    st.plotly_chart(fig, use_container_width=True)

    st.header('Sentiment Distribution of ' + company + ' Tweets')
    labels = ['Negative', 'Neutral', 'Positive']
    values = [df['neg'].count(), df['neu'].count(), df['pos'].count()]
    colors = ['#FEBFB3', '#E1396C', '#96D38C']
    fig = px.pie(df, values=values, names=labels, color=labels, color_discrete_sequence=colors)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Most Negative Tweets')
    st.write(df.sort_values('compound')['full_text'].head())

    st.header('Most Positive Tweets')
    st.write(df.sort_values('compound', ascending=False)['full_text'].head())

    st.header('Word Cloud of Most Negative Tweets')
    wordcloud(" ".join(clean_text(df.sort_values('compound')['full_text'].head())))

    st.header('Word Cloud of Most Positive Tweets')
    wordcloud(" ".join(clean_text(df.sort_values('compound', ascending=False)['full_text'].head())))

    st.header('Word Cloud of All Tweets')
    wordcloud(" ".join(clean_text(df['full_text'])))

    st.header('Word Frequency of All Tweets')
    word_freq = Counter(clean_text(df['full_text']))
    common_words = word_freq.most_common(10)
    df_common_words = pd.DataFrame(common_words, columns=['word', 'count'])
    fig = px.bar(df_common_words, x='word', y='count', color='count', color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')


def main():
    st.title('👍 Is your entreprise doing well? 👎')
    st.header("Let's check the sentiment of your business on twitter!")
    st.markdown("*more social medias to be added in the future*")

    # We ask the user basic infos
    company = st.text_input('Enter the name of your entreprise', 'Your company ...')
    nbr_of_tweets = st.slider('Number of tweets to load', 100, 2000, 100, 100)

    st.markdown('---')

    st.write('## Sentiment of tweets about ***' + company + '***')

    # DATA IMPORT
    # add a button to import data
    if st.button('Load data'):
        if company == 'Your company ...':
            st.error('Please enter a company name !')
        else:
            data = load_data_twitter(company, nbr_of_tweets)
            dataAnalyse(data,company)
    

if __name__ == '__main__':
    main()