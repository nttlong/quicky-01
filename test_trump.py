# -*- coding: utf-8 -*-
"""
To evaluate the good or bad score of a tweet, we first split our tweet.
We then associate each word with positive and negative values, respectively, using a dictionary.
Finally, we caculate the average word weight of a tweet, and decide if it's a good or bad one
based on that.
"""

# Break down a string into words
def get_words(str):
    return str.split()

# Iterate through the words in the tweet string
word_weights = {"Thanks": 1.0, "historic": 0.5, "paychecks": 0.8, "taxes": -1.0,"good":0.6}

# Calculate the average value of words in list_of_words
def get_average_word_weight(list_of_words):
    number_of_words = len(list_of_words)
    sum_of_word_weights = 0.0
    for w in list_of_words:
        if w in word_weights:
            sum_of_word_weights += word_weights[w]

    return sum_of_word_weights / number_of_words

tweet_string = " smile at Senators and others talking about how good free trade is for the U.S. What they don’t say is that we lose Jobs and over 800 Billion Dollars a year on really dumb Trade Deals....and these same countries Tariff us to death. These lawmakers are just fine with this!"
words = get_words(tweet_string)
avg_tweet_weight = get_average_word_weight(words)

print ("There weight of the tweet is " + str(avg_tweet_weight))

if avg_tweet_weight > 0:
    print ("What a presidential thing to say! HUGE!")
else:
    print ("Surely you're joking, Mr. Trump! SAD!")