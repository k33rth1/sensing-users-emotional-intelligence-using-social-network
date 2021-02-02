
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import numpy as np 
import pandas as pd 
import json
import os
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import math
from datetime import datetime
from sklearn.mixture import GaussianMixture
main = tkinter.Tk()
main.title("Sensing Users’ Emotional Intelligence in Social Networks") #designing main screen
main.geometry("1300x1200")

global filename

sid = SentimentIntensityAnalyzer()
global tweets_array
global follower_count,retweet_count,replies_count
global positive_emotion, negative_emotion, neutral_emotion
global awareness_arr,motivation_arr,relationship_arr,regulation_arr

def getSelfAwareness(sentence,average_sentiment):
    pos = []
    neg = []
    neu = []
    arr = sentence.split(' ')
    for i in range(len(arr)):
        word = arr[i].strip()
        if (sid.polarity_scores(word)['compound']) >= 0.5:
            pos.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.5:
            neg.append(word)
        else:
            neu.append(word)
    if len(pos) == 0:
        pos.append("a")
    if len(neg) == 0:
        neg.append("a")
    if average_sentiment == 0:
        average_sentiment = 0.2
    ws = len(pos)
    wn = len(arr)
    wi = len(pos) + len(neg)
    wc = len(neu)
    ws = ws / wn
    wi = wi / wc
    awareness = (ws + wi) * average_sentiment
    regulation = len(pos) / (len(pos) + len(neg))
    motivation = (len(pos) *  average_sentiment * 25) / (len(neg) *  average_sentiment)
                          
    return abs(awareness),abs(regulation),abs(motivation)/40      

def upload(): #function to upload tweeter profile
    global filename
    filename = filedialog.askdirectory(initialdir=".")
    pathlabel.config(text=filename)
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");


def tweetAnalysis(): #extract features from tweets
    global tweets_array
    global follower_count,retweet_count,replies_count
    tweets_array = []
    follower_count = []
    retweet_count = []
    replies_count = []
    text.delete('1.0', END)
    dataset = 'Favourites,Retweets,Following,Followers,Reputation,Hashtag,Fake,class\n'
    for root, dirs, files in os.walk(filename):
      for fdata in files:
        with open(root+"/"+fdata, "r") as file:
            data = json.load(file)
            textdata = data['text'].strip('\n')
            textdata = textdata.replace("\n"," ")
            textdata = re.sub('\W+',' ', textdata)
            retweet = data['retweet_count']
            followers = data['user']['followers_count']
            density = data['user']['listed_count']
            following = data['user']['friends_count']
            replies = data['user']['favourites_count']
            hashtag = data['user']['statuses_count']
            username = data['user']['screen_name']
            urls_count = data['user']['utc_offset']
            if urls_count == None:
                urls_count = 0
            else:
                urls_count = str(abs(int(urls_count)))
            if 'retweeted_status' in data:
                favourite = data['retweeted_status']['favorite_count']
            create_date = data['user']['created_at']
            strMnth    = create_date[4:7]
            day        = create_date[8:10]
            year       = create_date[26:30]
            if strMnth == 'Jan':
                strMnth = '01'
            if strMnth == 'Feb':
                strMnth = '02'
            if strMnth == 'Mar':
                strMnth = '03'
            if strMnth == 'Apr':
                strMnth = '04'
            if strMnth == 'May':
                strMnth = '05'
            if strMnth == 'Jun':
                strMnth = '06'
            if strMnth == 'Jul':
                strMnth = '07'
            if strMnth == 'Aug':
                strMnth = '08'    
            if strMnth == 'Sep':
                strMnth = '09'
            if strMnth == 'Oct':
                strMnth = '10'
            if strMnth == 'Nov':
                strMnth = '11'
            if strMnth == 'Dec':
                strMnth = '12'
            create_date = day+"/"+strMnth+"/"+year
            create_date = datetime.strptime(create_date,'%d/%m/%Y')
            today = datetime.today()
            age = today - create_date
            words = textdata.split(" ")
            text.insert(END,"Username : "+username+"\n");
            text.insert(END,"Tweet Text : "+textdata+"\n");
            text.insert(END,"Retweet Count : "+str(retweet)+"\n")
            text.insert(END,"Following : "+str(following)+"\n")
            text.insert(END,"Followers : "+str(followers)+"\n")
            text.insert(END,"Reputation : "+str(density)+"\n")
            text.insert(END,"Hashtag : "+str(hashtag)+"\n")
            text.insert(END,"Num Replies : "+str(replies)+"\n")
            text.insert(END,"Favourite Count : "+str(favourite)+"\n")
            text.insert(END,"Created Date : "+str(create_date)+" & Account Age : "+str(age)+"\n")
            text.insert(END,"URL's Count : "+str(urls_count)+"\n")
            text.insert(END,"Tweet Words Length : "+str(len(words))+"\n\n")
            tweets_array.append(textdata)
            if followers == 0:
                followers = 0.1
            if retweet == 0:
                retweet = 0.1
            if replies == 0:
                replies = 0.1    
            follower_count.append(followers)
            retweet_count.append(retweet)
            replies_count.append(replies)

                
def calculateEIDimension():
    global awareness_arr,motivation_arr,relationship_arr,regulation_arr
    global positive_emotion, negative_emotion, neutral_emotion
    positive_emotion = 0
    negative_emotion = 0
    neutral_emotion = 0
    awareness_arr = []
    motivation_arr = []
    relationship_arr = []
    regulation_arr = []
    text.delete('1.0', END)
    for i in range(len(tweets_array)):
        sentiment_dict = sid.polarity_scores(tweets_array[i])
        average_sentiment = sentiment_dict['compound']
        awareness,regulation,motivation = getSelfAwareness(tweets_array[i],average_sentiment)
        print(str(follower_count[i])+" "+str(retweet_count[i])+" "+str(replies_count[i]))
        relationship = abs((follower_count[i] * retweet_count[i]) / replies_count[i])
        if relationship > 100:
            relationship = relationship / 100
        negative = sentiment_dict['neg']
        positive = sentiment_dict['pos']
        neutral = sentiment_dict['neu']
        compound = sentiment_dict['compound']
        text.insert(END,"Input Sentence : "+tweets_array[i]+"\n")
        text.insert(END,"Positive : "+str(positive)+"\n")
        text.insert(END,"Negative : "+str(negative)+"\n")
        text.insert(END,"Neutral : "+str(neutral)+"\n")
        text.insert(END,"Compound : "+str(compound)+"\n")
        result = ''
        if compound >= 0.05 : 
            result = 'Positive' 
            positive_emotion = positive_emotion + 1  
        elif compound <= - 0.05 :
            negative_emotion = negative_emotion + 1
            result = 'Negative'
        else :
            result = 'Neutral'
            neutral_emotion = neutral_emotion + 1
        text.insert(END,'Sentiment Result     :'+result+"\n\n")
        text.insert(END,'Self-Awareness       : '+str(awareness)+"\n")
        text.insert(END,'Self-Regulation      : '+str(regulation)+"\n")
        text.insert(END,'Self-Motivation      : '+str(motivation)+"\n")
        text.insert(END,'Social Relationships : '+str(relationship)+"\n")
        awareness_arr.append(awareness)
        motivation_arr.append(motivation)
        relationship_arr.append(relationship)
        regulation_arr.append(regulation)
        if motivation > 0.5:
            text.insert(END,'User is in depressed state\n')
        else:
            text.insert(END,"user is not in depressed stated\n")
        if relationship > 0.2:
            text.insert(END,'User mood swinging detected\n')
        else:
            text.insert(END,'User mood swinging not detected\n')
        text.insert(END,'\n\n')    
    
def graph():
    height = [positive_emotion,negative_emotion,neutral_emotion]
    bars = ('Positive Emotions', 'Negative Emotion','Neutral Emotion')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

def EIGraph():
    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Item ID')
    plt.ylabel('True Ranking')
    plt.plot(awareness_arr, 'ro-', color = 'indigo')
    plt.plot(motivation_arr, 'ro-', color = 'green')
    plt.plot(relationship_arr, 'ro-', color = 'blue')
    plt.plot(regulation_arr, 'ro-', color = 'orange')
    plt.legend(['Awareness', 'Motivation','Regulation','Social Relationship'], loc='upper left')
    #plt.xticks(wordloss.index)
    plt.title('Distribution of the four dimensions of EI Graph')
    plt.show()

def GMMClustering():
    X = [[awareness_arr],[motivation_arr],[relationship_arr],[regulation_arr]]
    X = np.asarray(X)
    print(X.shape)
    X = X.reshape((X.shape[0]*X.shape[1]), X.shape[2])
    X = X.transpose()
    print(X.shape)
    gmm = GaussianMixture(n_components=4).fit(X)
    labels = gmm.predict(X)
    plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');
    plt.show()

    
font = ('times', 16, 'bold')
title = Label(main, text='Sensing Users’ Emotional Intelligence in Social Networks')
title.config(bg='brown', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
uploadButton = Button(main, text="Upload Twitter Dataset", command=upload)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='brown', fg='white')  
pathlabel.config(font=font1)           
pathlabel.place(x=470,y=100)

analysisButton = Button(main, text="Tweets Analysis", command=tweetAnalysis)
analysisButton.place(x=50,y=150)
analysisButton.config(font=font1) 

EIButton = Button(main, text="Calculate EI Four Dimensions", command=calculateEIDimension)
EIButton.place(x=250,y=150)
EIButton.config(font=font1) 

graphButton = Button(main, text="Emotion Occurence Graph", command=graph)
graphButton.place(x=550,y=150)
graphButton.config(font=font1) 

EIgraphButton = Button(main, text="Emotion Four Dimension EI Graph", command=EIGraph)
EIgraphButton.place(x=50,y=200)
EIgraphButton.config(font=font1)

clusteringButton = Button(main, text="GMM Clustering", command=GMMClustering)
clusteringButton.place(x=400,y=200)
clusteringButton.config(font=font1) 


font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=250)
text.config(font=font1)


main.config(bg='brown')
main.mainloop()
