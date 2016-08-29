from twitter import oauth_dance, read_token_file, TwitterStream, OAuth
import os
import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd
import time
from math import log, fabs, nan, acos, sin, cos, pi, inf

CONSUMER_KEY = 'uqiCSPB5CYtMXYN4wV2LUkwiL'
CONSUMER_SECRET = 'q3sSeTZNKKAc4eladDvyVlyDctL2066ht36wpwjYjpByLgWKQJ'

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("SentimentVisualizer", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
twitter_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

iterartor = twitter_stream.statuses.filter(track='trump')

stop_list = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
exclude_words = ['hillary','trump','donald','about','&amp;']

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

        for word in cleaned_list:
            temp_df = pd.DataFrame(index=[pd.datetime.now()], columns=[word], data=1)
            df = df.append(temp_df)

            if word in words:

                words[word]['count'] += 1
            else:
                words[word] = dict()
                words[word]['count'] = 1

            for word2 in cleaned_list:
                word2 = word2.lower()
                if word == word2:
                    continue

                try:
                    words[word]['intersect'][word2] += 1
                except:
                    if 'intersect' not in words[word]:
                        words[word]['intersect'] = dict()
                    words[word]['intersect'][word2] = 1

    except:
        pass




    if j % 500 == 0:
        j = 0
        words = dict()

    if j > 20:

        df = df.resample('S').sum().replace(nan, 0)
        df_rolling = df.rolling(360, min_periods=3).sum().T.sort_values(df.resample('S').index.values[-1])

        # Order words by count
        # vect = sorted([(word, subdict['count'], subdict['intersect']) for word, subdict in words.items() if 'intersect' in subdict], key=lambda x: -x[1])
        # strout = ''
        # for k in range(numwords):
        #     strout += '{0}: {1}  '.format(vect[k][0], vect[k][1])
        # print(strout, end='\r')
        #
        # # Calculate distances of top 10 words
        # distance_map = dict()
        # for k in range(10):
        #     v = vect[k]
        #     distance_map[v[0]] = dict()
        #     for word, count in v[2].items():
        #         try:
        #             distance = fabs(1/log(count))
        #             distance_map[v[0]][word] = distance
        #         except:
        #             distance = nan

        # Plot time-series
        df_plot = df_rolling.tail(numwords).T
        df_plot.plot(ax=ax, legend=False)

        # try:
        #     for t in ax.texts:
        #         t.remove()
        #         t.set_visible(False)
        # except:
        #     pass

        if len(df.index.values) % 20 == 0:
            li = 0
            for line in ax.lines:
                try:
                    x = ax.get_axes().dataLim._get_max()[0]
                    y = df_plot.ix[-1,li]
                    s = df_plot.columns.values[li]
                    li += 1
                    if y != nan:
                        if x != inf:
                            ax.text(x,y,s)
                except:
                    pass

        ax.relim()
        ax.autoscale_view(True, True, True)
        plt.pause((0.01))

        # Convert distance to XY coordinates
        continue
        coords = dict()
        for centroid, words_dict in distance_map.items():
            coords[centroid] = dict()
            coords[centroid][centroid] = (0,0) # the centroid word is at the center of it's own relative coordinate system
            for word, distance in words_dict.items(): # distance between centroid and word
                if len(coords[centroid]) == 1: # if this is the first non-centroid word
                    coords[centroid][word] = (distance, 0.0) # separate on x-axis
                for word2, distance2 in words_dict.items(): # distance between word2 and centroid
                    if word == word2:
                        continue
                    else:
                        d_ac = distance
                        d_ab = distance2
                        try:
                            d_cb = fabs(1/log(words[word]['intersect'][word2]))
                        except:
                            d_cb = 2.0

                        angle_a = acos((d_ac**2.+d_ab**2.-d_cb**2.)/(2.*d_ac*d_ab))
                        coords[centroid][word2] = ( d_ac*sin((pi/2.)-angle_a), d_ac*cos((pi/2.)-angle_a) )

    else:
        print('Buffering... {0}/20 | {1}'.format(j, len(words)), end='\r')
        ### chcp 65001


