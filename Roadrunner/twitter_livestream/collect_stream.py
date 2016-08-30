from twitter import oauth_dance, read_token_file, TwitterStream, OAuth
import os
import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd

CONSUMER_KEY = 'uqiCSPB5CYtMXYN4wV2LUkwiL'
CONSUMER_SECRET = 'q3sSeTZNKKAc4eladDvyVlyDctL2066ht36wpwjYjpByLgWKQJ'

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("SentimentVisualizer", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
twitter_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

iterartor = twitter_stream.statuses.filter(track='weiner')

stop_list = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
exclude_words = ['hillary','trump','donald','about','&amp;','weiner','anthony']

style.use('fivethirtyeight')
fig = plt.figure(figsize=(10,10))
ax = plt.gca()
plt.ion()
fig.canvas.draw()

numwords = 8

df = pd.DataFrame()

print('Streaming...', end='\r')
words = dict()
j = 0
xi = 0
for tweet in iterartor:

    j += 1
    # Count words
    try:
        cleaned_list = list()
        word_list = tweet['text'].split(' ')
        for word in word_list:
            word = word.lower()
            if word in exclude_words:
                continue

            if word in stop_list:
                continue

            if "amp" in word:
                continue

            word = word.replace( ';', '')
            word = word.replace( ':', '')
            word = word.replace( '.', '')
            word = word.replace( ',', '')
            word = word.replace( '!', '')
            word = word.replace('\n', '')
            word = word.replace('\t', '')
            word = word.replace( '?', '')
            word = word.replace( '&', '')
            word = word.replace( '"', '')

            if word in exclude_words:
                continue

            if len(word) < 4:
                continue

            cleaned_list.append(word)
    except:
        pass