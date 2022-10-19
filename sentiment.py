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


#load data
def load_data():
    with open('C:/Users/T/Downloads/tweets_uber.json') as f:
        data = json.load(f)
    return data

def wordcloud(text):
    plt.figure(figsize=(10, 7))
    fig, ax = plt.subplots()
    plt.axis('off')
    wordcloud = WordCloud(background_color='white', width=800, height=500, random_state=21, max_font_size=110).generate(text)
    ax.imshow(wordcloud, interpolation="bilinear")
    st.pyplot(fig)

st.title('👍 Is your entreprise doing well?')
st.header("Let's check the sentiment of your business on twitter!")

company = st.text_input('Enter the name of your entreprise')

st.markdown('---')

if company:
    st.write('## Sentiment of tweets about ' + company)

data = load_data()

sia = SentimentIntensityAnalyzer()
for tweet in data:
    tweet['scores'] = sia.polarity_scores(tweet['full_text'])
    tweet['compound'] = tweet['scores']['compound']
    tweet['neg'] = tweet['scores']['neg']
    tweet['neu'] = tweet['scores']['neu']
    tweet['pos'] = tweet['scores']['pos']


df = pd.DataFrame.from_dict(data)

col1, col2, col3 = st.columns(3)
col1.metric("Number of Positive Tweets", df[df['compound'] > 0.05].shape[0])
col2.metric("Number of Negative Tweets", df[df['compound'] < -0.05].shape[0])
col3.metric("Number of Neutral Tweets", df[(df['compound'] >= -0.05) & (df['compound'] <= 0.05)].shape[0])

st.header('Sentiment Polarity of Uber Tweets')
fig = px.scatter(df, x='neg', y='pos', color='compound')
st.plotly_chart(fig, use_container_width=True)

st.header('Sentiment Distribution of Uber Tweets')
labels = ['Negative', 'Neutral', 'Positive']
values = [df['neg'].count(), df['neu'].count(), df['pos'].count()]
colors = ['#FEBFB3', '#E1396C', '#96D38C']
fig = px.pie(df, values=values, names=labels, color=labels, color_discrete_sequence=colors)
st.plotly_chart(fig, use_container_width=True)

st.header('Most Negative Tweets')
st.write(df.sort_values('compound')['full_text'].head())

st.header('Most Positive Tweets')
st.write(df.sort_values('compound', ascending=False)['full_text'].head())


def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [word for word in tokens if word not in stopwords.words('english')]
    return text

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



